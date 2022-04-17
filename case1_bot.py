#!/usr/bin/env python
'''
prelim bot for case 1

bid: sellers price
ask: buyers price

Test with local exchange:
python3 case1_bot.py

./xchange_mac -pricepath=2019 case1

for comp:

(venv) python {your_bot_name.py} {your desired username on display} -t {AWS IP address}
python3 case1_bot.py test007 -t 44.203.25.210


TODO:
current issues: unfilled orders are not keeping track exactly of real orders
- main issue when change the price of the order, we are not updating that price in the OpenOrders
rather we are creating a new openOrder with a different price but the same id
Solution instead of

'''

from utc_bot import UTCBot, start_bot
import proto.utc_bot as pb
import betterproto

import asyncio
import params

class OpenOrders:
    def __init__(self, contract):
        self.contract_name = contract
        self.num_open_orders = 0
        self.price_to_id = {} # price to id dict

        self.id_to_price = {} # id to price dict

        self.id_to_qty = {} # id to qty dict

    # adjusting the quantity based on the id - remove order from OpenOrders if quantity is now 0.
    def adjust_qty(self, id, adj):
        self.id_to_qty[id] += adj

        # deleting order
        if self.id_to_qty[id] == 0:
            self.num_open_orders -= 1
            price = self.id_to_price[id]

            try:
                del self.id_to_price[id]
                del self.price_to_id[price]
                del self.id_to_qty[id]
            except Exception as e:
                print("Error (0) deleting filled order: ",e)


    # adding the order to the price_to_id dict if we don't already have any id in this price
    # NOT USED
    def add_order(self, price, id, qty):
        if not price in self.price_to_id:
            self.price_to_id[price] = id
            self.num_open_orders += 1
        if not id in self.id_to_qty:
            self.id_to_qty[id] = qty
        if not id in self.id_to_price:
            self.id_to_price[id] = price

    def modify_order(self,price,qty,old_id,new_id):
        # create order (if there is no order with matching ID)
        if (old_id == new_id):
            if not old_id in self.id_to_price:
                self.id_to_price[old_id] = price
                self.price_to_id[price] = old_id
                self.id_to_qty[old_id] = qty
                self.num_open_orders += 1
            # update order
            else:
                # delete old price to data
                try:
                    del self.price_to_id[self.id_to_price[old_id]]
                except Exception as e:
                    print("Error (1) deleting filled order: ",e)

                # add new price to id
                self.price_to_id[price] = old_id
                self.id_to_price[old_id] = price
                self.id_to_qty[old_id] = qty
        else:
            if not old_id in self.id_to_price:
                self.id_to_price[new_id] = price
                self.price_to_id[price] = new_id
                self.id_to_qty[new_id] = qty
                self.num_open_orders += 1
            else:
                # old order still exists so delete and then update with new values

                # delete old price, id, and qty
                try:
                    del self.price_to_id[self.id_to_price[old_id]] # error is no price in price_to_id for old price
                    del self.id_to_price[old_id]
                    del self.id_to_qty[old_id]
                except Exception as e:
                    print("Error (2) deleting filled order: ",e)

                # add new price to new id
                self.price_to_id[price] = new_id
                self.id_to_price[new_id] = price
                self.id_to_qty[new_id] = qty


    # getting the quantity based on the price
    def get_qty(self, price):
        p_id = self.price_to_id[price]
        return self.id_to_qty[p_id]

    def get_id(self, price):
        return self.price_to_id[price]

CONTRACTS = ["LBSJ","LBSM", "LBSQ", "LBSV", "LBSZ"]

ORDER_SIZE = 65 # 50

ORDER_L1 = 15 # 25
ORDER_L2 = 10 # 10
ORDER_L3 = 5 # 5

L1_SPREAD = 0.02
L2_SPREAD = L1_SPREAD*2
L3_SPREAD = L1_SPREAD*3
L4_SPREAD = L1_SPREAD*4


class Case1Bot(UTCBot):
    '''
    Bot for 2022 Uchi Trading comp
    '''

    async def handle_round_started(self):
        '''
        This function is called when the round is started. You should do your setup here, and
        start any tasks that should be running for the rest of the round.

        TODO:
        - start ML running (separate thread?) and
            send in price data along with past price data (window size) and rain amount of mount
        - other tasks if there are others needed (perhaps config panel where we can adjust params on the fly)
        '''

        # starting fair price (get spot value from model later?)
        start_fair = params.START_FAIR

        # trading day (0-251)
        self.day = 0
        self.rain = []
        self.fairs = {}
        self.order_book = {}
        self.pos = {}
        self.order_ids = {}

        self.open_orders = {}

        # UNUSED
        self.spread = params.SLACK


        for month in CONTRACTS:
            # TODO make other (for different levels of orders)
            self.order_ids[month+' bid'] = ''
            self.order_ids[month+' ask'] = ''

            self.order_ids[month+' l1 bid'] = ''
            self.order_ids[month+' l1 ask'] = ''

            self.order_ids[month+' l2 bid'] = ''
            self.order_ids[month+' l2 ask'] = ''

            self.order_ids[month+' l3 bid'] = ''
            self.order_ids[month+' l3 ask'] = ''

            self.order_ids[month+' l4 bid'] = ''
            self.order_ids[month+' l4 ask'] = ''


            self.fairs[month] = start_fair

            self.order_book[month] = {
                'Best Bid':{'Price':0,'Quantity':0},
                'Best Ask':{'Price':0,'Quantity':0}
                }

            self.pos[month] = 0

            self.open_orders[month] = OpenOrders(month)

        asyncio.create_task(self.update_quotes())

    def update_fairs(self):
        '''
        You should implement this function to update the fair value of each asset as the
        round progresses.
        TODO: this is where we contact ML model and send input
        while it takes time to compute (or we don't have data)
        trade on the last known price (be that historical or predicted)
        # TODO should we price the further away contracts more?
        '''

        # currently settings fairs to mark price (of last Best Bid and Best Ask)
        for month in CONTRACTS:

            fair = (self.order_book[month]["Best Bid"]["Price"] + self.order_book[month]["Best Ask"]["Price"]) / 2.0

            self.fairs[month] = fair if fair > 0 else params.START_FAIR

    async def update_quotes(self):
        '''
        This function updates the quotes at each time step. In this sample implementation we
        are always quoting symetrically about our predicted fair prices, without consideration
        for our current positions. We don't reccomend that you do this for the actual competition.
        TODO: determine strat + read blog for what was used
        '''
        while True:
            # if we have seen a rain report then trade (change later)
            #if ( self.rain ):

            # update fairs UNUSED
            #self.update_fairs()

            for contract in CONTRACTS:
                penny_ask_price = self.order_book[contract]["Best Ask"]["Price"] - .01
                penny_bid_price = self.order_book[contract]["Best Bid"]["Price"] + .01

                if (self.order_book[contract]["Best Ask"]["Price"] == 0 or self.order_book[contract]["Best Bid"]["Price"] == 0):
                    penny_ask_price = params.START_ASK
                    penny_bid_price = params.START_BID

                if ( penny_ask_price - penny_bid_price ) > 0 :

                    old_bid_id = self.order_ids[contract+' bid']
                    old_ask_id = self.order_ids[contract+' ask']
                    # penny bid/ask
                    bid_response = await self.modify_order(
                        self.order_ids[contract+' bid'],
                        contract,
                        pb.OrderSpecType.LIMIT,
                        pb.OrderSpecSide.BID,
                        ORDER_SIZE,
                        round(penny_bid_price, 2))

                    ask_response = await self.modify_order(
                        self.order_ids[contract+' ask'],
                        contract,
                        pb.OrderSpecType.LIMIT,
                        pb.OrderSpecSide.ASK,
                        ORDER_SIZE,
                        round(penny_ask_price, 2))

                    assert bid_response.ok
                    self.order_ids[contract+' bid'] = bid_response.order_id

                    self.open_orders[contract].modify_order(round(penny_bid_price, 2),ORDER_SIZE,old_bid_id, bid_response.order_id )


                    assert ask_response.ok
                    self.order_ids[contract+' ask'] = ask_response.order_id
                    self.open_orders[contract].modify_order(round(penny_ask_price, 2), -ORDER_SIZE, old_ask_id, ask_response.order_id )

                    # levels 1
                    if (penny_bid_price - L1_SPREAD) > 0:
                        old_bid_id = self.order_ids[contract+' l1 bid']
                        old_ask_id = self.order_ids[contract+' l1 ask']

                        bid_response = await self.modify_order(
                            self.order_ids[contract+' l1 bid'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.BID,
                            ORDER_L1,
                            round(penny_bid_price - L1_SPREAD, 2))

                        ask_response = await self.modify_order(
                            self.order_ids[contract+' l1 ask'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.ASK,
                            ORDER_L1,
                            round(penny_ask_price + L1_SPREAD, 2))

                        #assert bid_response.ok
                        self.order_ids[contract+' l1 bid'] = bid_response.order_id
                        self.open_orders[contract].modify_order(round(penny_bid_price - L1_SPREAD, 2),ORDER_L1, old_bid_id,bid_response.order_id )


                        #assert ask_response.ok
                        self.order_ids[contract+' l1 ask'] = ask_response.order_id
                        self.open_orders[contract].modify_order(round(penny_ask_price + L1_SPREAD, 2),-ORDER_L1, old_ask_id,ask_response.order_id )

                    # levels 2
                    if (penny_bid_price - L2_SPREAD) > 0:
                        old_bid_id = self.order_ids[contract+' l2 bid']
                        old_ask_id = self.order_ids[contract+' l2 ask']

                        bid_response = await self.modify_order(
                            self.order_ids[contract+' l2 bid'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.BID,
                            ORDER_L2,
                            round(penny_bid_price - L2_SPREAD, 2))

                        ask_response = await self.modify_order(
                            self.order_ids[contract+' l2 ask'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.ASK,
                            ORDER_L2,
                            round(penny_ask_price + L2_SPREAD, 2))

                        #assert bid_response.ok
                        self.order_ids[contract+' l2 bid'] = bid_response.order_id
                        self.open_orders[contract].modify_order(round(penny_bid_price - L2_SPREAD, 2),ORDER_L2, old_bid_id,bid_response.order_id )


                        #assert ask_response.ok
                        self.order_ids[contract+' l2 ask'] = ask_response.order_id
                        self.open_orders[contract].modify_order(round(penny_ask_price + L2_SPREAD, 2),-ORDER_L2, old_ask_id,ask_response.order_id )


                    # levels 3
                    if (penny_bid_price - L3_SPREAD) > 0:
                        old_bid_id = self.order_ids[contract+' l3 bid']
                        old_ask_id = self.order_ids[contract+' l3 ask']

                        bid_response = await self.modify_order(
                            self.order_ids[contract+' l3 bid'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.BID,
                            ORDER_L3,
                            round(penny_bid_price - L3_SPREAD, 2))

                        ask_response = await self.modify_order(
                            self.order_ids[contract+' l3 ask'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.ASK,
                            ORDER_L3,
                            round(penny_ask_price + L3_SPREAD, 2))

                        #assert bid_response.ok
                        self.order_ids[contract+' l3 bid'] = bid_response.order_id
                        self.open_orders[contract].modify_order(round(penny_bid_price - L3_SPREAD, 2),ORDER_L3, old_bid_id,bid_response.order_id )


                        #assert ask_response.ok
                        self.order_ids[contract+' l3 ask'] = ask_response.order_id
                        self.open_orders[contract].modify_order(round(penny_ask_price + L3_SPREAD, 2),-ORDER_L3, old_ask_id,ask_response.order_id )


            await asyncio.sleep(1)

    async def handle_exchange_update(self, update: pb.FeedMessage):
        '''
        This function receives messages from the exchange. You are encouraged to read through
        the documentation for the exachange to understand what types of messages you may receive
        from the exchange and how they may be useful to you.

        Note that monthly rainfall predictions are sent through Generic Message.
        '''
        kind, _ = betterproto.which_one_of(update, "msg")

        if kind == "pnl_msg":
            self.day += 1
            print('Realized pnl:', update.pnl_msg.realized_pnl)
            print("M2M pnl:", update.pnl_msg.m2m_pnl)

        elif kind == "market_snapshot_msg":
        # Updates your record of the Best Bids and Best Asks in the market
            for contract in CONTRACTS:
                book = update.market_snapshot_msg.books[contract]

                # remove our orders from boo TODO
                for price in self.open_orders[contract].price_to_id.keys():
                    quantity = self.open_orders[contract].get_qty(price)

                    #print("open order price: ", price, contract, quantity, self.open_orders[contract].price_to_id[price])

                    if (quantity > 0): # long
                        #print("book bid: ",end="")
                        for i in range (len(book.bids)):
                            #print(book.bids[i].px, " ",end="")
                            if (round(float(book.bids[i].px), 2) < price):
                                break
                            if (round(float(book.bids[i].px), 2) == price):
                                book.bids[i].qty -= quantity
                                if (book.bids[i].qty == 0):
                                    book.bids.pop(i)
                                #print("BOOK changed")
                                break
                    else: # short
                        #print("book ask: ",end="")
                        for i in range (len(book.asks)):
                            #print(book.asks[i].px," ",end="")
                            if (round(float(book.asks[i].px), 2) > price):
                                break
                            if (round(float(book.asks[i].px), 2) == price):
                                book.asks[i].qty += quantity
                                if (book.asks[i].qty == 0):
                                    book.asks.pop(i)
                                #print("BOOK changed")
                                break


                if len(book.bids) != 0:
                    best_bid = book.bids[0]
                    self.order_book[contract]['Best Bid']['Price'] = float(best_bid.px)
                    self.order_book[contract]['Best Bid']['Quantity'] = best_bid.qty

                if len(book.asks) != 0:
                    best_ask = book.asks[0]
                    self.order_book[contract]['Best Ask']['Price'] = float(best_ask.px)
                    self.order_book[contract]['Best Ask']['Quantity'] = best_ask.qty

            # TODO debug purposes
            #params.book_prices(book,update)

        elif kind == "fill_msg":
            # When you hear about a fill you had, update your positions
            fill_msg = update.fill_msg

            if fill_msg.order_side == pb.FillMessageSide.BUY:

                for order_key in self.open_orders.keys():
                    if fill_msg.order_id in self.open_orders[order_key].id_to_qty.keys():
                        self.open_orders[order_key].adjust_qty(fill_msg.order_id, -1*fill_msg.filled_qty)
                        break

                self.pos[fill_msg.asset] += update.fill_msg.filled_qty

                #print("\t\t","asset\t","price\t","fill qty\t","remain qty")
                #print("BOUGHT: ",fill_msg.asset,"\t",fill_msg.price,"\t", fill_msg.filled_qty,"\t", fill_msg.remaining_qty)
            else:

                for order_key in self.open_orders.keys():
                    if fill_msg.order_id in self.open_orders[order_key].id_to_qty.keys():
                        self.open_orders[order_key].adjust_qty(fill_msg.order_id, fill_msg.filled_qty)
                        break

                self.pos[fill_msg.asset] -= update.fill_msg.filled_qty

                #print("\t\t","asset\t","price\t","fill qty\t","remain qty")
                #print("SOLD: ",fill_msg.asset,"\t",fill_msg.price,"\t", fill_msg.filled_qty,"\t", fill_msg.remaining_qty)


            # UNCOMMENT FOR DEBUGGING
            #print("pos:", self.pos)


        elif kind == "generic_msg":
            # Saves the predicted rainfall
            try:
                pred = float(update.generic_msg.message)
                self.rain.append(pred)

                # TODO debug purposes
                #print("rain:",self.rain)

            # Prints the Risk Limit message
            except ValueError:
                print(update.generic_msg.message)


        #elif kind == "trade_msg":
            # do something
            #trade_msg = update.trade_msg

            #print("trade: ", trade_msg.asset,trade_msg.price,trade_msg.qty)



if __name__ == "__main__":
    start_bot(Case1Bot)