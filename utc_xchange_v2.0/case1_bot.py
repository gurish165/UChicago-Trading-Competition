#!/usr/bin/env python
'''
prelim bot for case 1

bid: sellers price
ask: buyers price

Test with local exchange:
python3 case1_bot.py

./xchange_mac case1

for comp:

(venv) python {your_bot_name.py} {your desired username on display} -t {AWS IP address}
python3 case1_bot.py test007 -t 44.203.25.210
'''

from collections import defaultdict
from gettext import find

from numpy import double
from utc_bot import UTCBot, start_bot
import proto.utc_bot as pb
import betterproto

import asyncio
import params

from dataclasses import dataclass

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
        if self.id_to_qty[id] == 0:
            self.num_open_orders -= 1
            price = self.id_to_price[id]
            del self.id_to_price[id]
            del self.price_to_id[price]
            del self.id_to_qty[id]


    # adding the order to the price_to_id dict if we don't already have any id in this price
    def add_order(self, price, id, qty):
        if not price in self.price_to_id:
            self.price_to_id[price] = id
            self.num_open_orders += 1
        if not id in self.id_to_qty:
            self.id_to_qty[id] = qty
        if not id in self.id_to_price:
            self.id_to_price[id] = price


    # getting the quantity based on the price
    def get_qty(self, price):
        p_id = self.price_to_id[price]
        return self.id_to_qty[p_id]

    def get_id(self, price):
        return self.price_to_id[price]


CONTRACTS = ["LBSJ","LBSM", "LBSQ", "LBSV", "LBSZ"]
ORDER_SIZE = 50

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

        self.rain = []

        self.fairs = {}
        self.order_book = {}

        self.pos = {}

        self.order_ids = {}

        self.spread = params.SLACK

        self.id_to_contract = {}

        self.order_names = [] # names of different orders (currently have set amount)

        self.open_orders = {}

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


            self.order_names.append(month+' bid')
            self.order_names.append(month+' ask')

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
        '''
        # TODO should we price the further away contracts more?

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
            if ( self.rain ):
                self.update_fairs()

                for contract in CONTRACTS:
                    penny_ask_price = self.order_book[contract]["Best Ask"]["Price"] - .01
                    penny_bid_price = self.order_book[contract]["Best Bid"]["Price"] + .01

                    if (self.order_book[contract]["Best Ask"]["Price"] == 0 or self.order_book[contract]["Best Bid"]["Price"] == 0):
                        penny_ask_price = params.START_ASK
                        penny_bid_price = params.START_BID

                    if ( penny_bid_price - penny_ask_price ) <= 0 :

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

                        self.open_orders[contract].add_order(round(penny_bid_price, 2),bid_response.order_id,ORDER_SIZE )


                        assert ask_response.ok
                        self.order_ids[contract+' ask'] = ask_response.order_id
                        self.open_orders[contract].add_order(round(penny_ask_price, 2),ask_response.order_id,ORDER_SIZE )

                        # levels 1
                        bid_response = await self.modify_order(
                            self.order_ids[contract+' l1 bid'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.BID,
                            25,
                            round(penny_bid_price - 0.20, 2))

                        ask_response = await self.modify_order(
                            self.order_ids[contract+' l1 ask'],
                            contract,
                            pb.OrderSpecType.LIMIT,
                            pb.OrderSpecSide.ASK,
                            25,
                            round(penny_ask_price + 0.20, 2))

                        #assert bid_response.ok
                        self.order_ids[contract+' l1 bid'] = bid_response.order_id
                        self.open_orders[contract].add_order(round(penny_bid_price - 0.20, 2),bid_response.order_id,ORDER_SIZE )


                        #assert ask_response.ok
                        self.order_ids[contract+' l1 ask'] = ask_response.order_id
                        self.open_orders[contract].add_order(round(penny_ask_price + 0.20, 2),ask_response.order_id,ORDER_SIZE )


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
            print('Realized pnl:', update.pnl_msg.realized_pnl)
            print("M2M pnl:", update.pnl_msg.m2m_pnl)

        elif kind == "market_snapshot_msg":
        # Updates your record of the Best Bids and Best Asks in the market
            for contract in CONTRACTS:
                book = update.market_snapshot_msg.books[contract]

                # remove our orders from boo TODO
                for price in self.open_orders[contract].price_to_id.keys():
                    quantity = self.open_orders[contract].get_qty(price)
                    if (quantity > 0): # long
                        for i in range (len(book.bids)):
                            if (book.bids[i].px == price):
                                book.bids[i].qty -= quantity
                                if (book.bids[i].qty == 0):
                                    book.bids.pop(i)
                                break
                    else: # short
                        for i in range (len(book.asks)):
                            if (book.asks[i].px == price):
                                book.asks[i].qty += quantity
                                if (book.asks[i].qty == 0):
                                    book.asks.pop(i)
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
            params.book_prices(book,update)

        elif kind == "fill_msg":
            # When you hear about a fill you had, update your positions
            fill_msg = update.fill_msg

            if fill_msg.order_side == pb.FillMessageSide.BUY:

                for order_key in self.open_orders.keys():
                    if fill_msg.order_id in self.open_orders[order_key].id_to_qty.keys():
                        self.open_orders[order_key].adjust_qty(fill_msg.order_id, fill_msg.filled_qty)
                        break

                self.pos[fill_msg.asset] += update.fill_msg.filled_qty

                print("\t\t","asset\t","price\t","fill qty\t","remain qty")
                print("BOUGHT: ",fill_msg.asset,"\t",fill_msg.price,"\t", fill_msg.filled_qty,"\t", fill_msg.remaining_qty)
            else:

                for order_key in self.open_orders.keys():
                    if fill_msg.order_id in self.open_orders[order_key].id_to_qty.keys():
                        self.open_orders[order_key].adjust_qty(fill_msg.order_id, -1*fill_msg.filled_qty)
                        break

                self.pos[fill_msg.asset] -= update.fill_msg.filled_qty

                print("\t\t","asset\t","price\t","fill qty\t","remain qty")
                print("SOLD: ",fill_msg.asset,"\t",fill_msg.price,"\t", fill_msg.filled_qty,"\t", fill_msg.remaining_qty)


            print("pos:", self.pos)


        elif kind == "generic_msg":
            # Saves the predicted rainfall
            try:
                pred = float(update.generic_msg.message)
                self.rain.append(pred)

                # TODO debug purposes
                print("rain:",self.rain)

            # Prints the Risk Limit message
            except ValueError:
                print(update.generic_msg.message)


        #elif kind == "trade_msg":
            # do something




if __name__ == "__main__":
    start_bot(Case1Bot)