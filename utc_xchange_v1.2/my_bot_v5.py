#!/usr/bin/env python

from dataclasses import astuple
from datetime import datetime
from utc_bot import UTCBot, start_bot
from black_scholes_volatility import black_scholes as my_bs
import proto.utc_bot as pb
import betterproto
import numpy as np
import asyncio
# import matplotlib.pyplot as plt
# from greeks import delta, gamma, theta, vega

option_strikes = [90, 95, 100, 105, 110]


class Case2(UTCBot):
    """
    An example bot for Case 2 of the 2021 UChicago Trading Competition. We recommend that you start
    by reading through this bot and understanding how it works. Then, make a copy of this file and
    start trying to write your own bot!
    """

    async def handle_round_started(self):
        """
        This function is called when the round is started. You should do your setup here, and
        start any tasks that should be running for the rest of the round.
        """

        # This variable will be a map from asset names to positions. We start out by initializing it
        # to zero for every asset.
        self.positions = {}

        self.positions["UC"] = 0
        for strike in option_strikes:
            for flag in ["C", "P"]:
                self.positions[f"UC{strike}{flag}"] = 0

        # Stores the current day (starting from 0 and ending at 5). This is a floating point number,
        # meaning that it includes information about partial days
        self.current_day = 0

        # Stores the current value of the underlying asset
        self.underlying_price = 100
        self.time_tick = 0
        self.pnls = [0.0] * 1000
        self.price_path = []
        self.puts100 = []
        self.calls100 = []
        self.vols = []
        self.C100_price = 0
        self.greek_limits = {
            "delta": 2000,
            "gamma": 5000,
            "theta": 50000,
            "vega": 1000000
        }
        self.my_greek_limits = {
            "delta": 0,
            "gamma": 0,
            "theta": 0,
            "vega": 0
        }
        self.books={}
        self.safe_buy = 0
        self.max_contracts_left = 0


    # def compute_vol_estimate(self) -> float:
    #     """
    #     This function is used to provide an estimate of underlying's volatility. Because this is
    #     an example bot, we just use a placeholder value here. We recommend that you look into
    #     different ways of finding what the true volatility of the underlying is.
    #     """

    #     if(len(self.price_path) <= 20):
    #         return 0.2
    #     else:
    #         stdev = np.std(self.price_path[-100:])
    #         # volatility = 0.9* np.log(stdev/2.5 + 0.375) + 0.9
    #         volatility = (stdev+0.1)**(1/3)-0.5
    #         return volatility
    

    # def compute_options_price(
    #     self,
    #     flag: str,
    #     underlying_px: float,
    #     strike_px: float,
    #     time_to_expiry: float,
    #     volatility: float,
    # ) -> float:
    #     """
    #     This function should compute the price of an option given the provided parameters. Some
    #     important questions you may want to think about are:
    #         - What are the units associated with each of these quantities?
    #         - What formula should you use to compute the price of the option?
    #         - Are there tricks you can use to do this more quickly?
    #     You may want to look into the py_vollib library, which is installed by default in your
    #     virtual environment.
    #     """
    #     per_share_val = 0
    #     if(flag == 'C' or flag == 'c'):
    #         per_share_val = my_bs('c', underlying_px, strike_px, time_to_expiry, 0.00, volatility)
    #     elif(flag == 'P' or flag == 'p'):
    #         per_share_val = my_bs('p', underlying_px, strike_px, time_to_expiry, 0.00, volatility)
    #     if (per_share_val < 0.1):
    #         per_share_val = 0.1
    #     return np.round(per_share_val, 1)

    def add_trades(self):
        requests = []
        count = 0
        # if "UC" in self.books:
        #     requests.append(
        #             self.modify_order(
        #                 "UCSELL",
        #                 "UC",
        #                 pb.OrderSpecType.LIMIT,
        #                 pb.OrderSpecSide.ASK,
        #                 10000,
        #                 round(float(self.books["UC"].asks[0].px), 2) - 0.01
        #             )
        #         )
        #     requests.append(
        #         self.modify_order(
        #             "UCBUY",
        #             "UC",
        #             pb.OrderSpecType.LIMIT,
        #             pb.OrderSpecSide.BID,
        #             10000,
        #             round(float(self.books["UC"].bids[0].px), 2) + 0.01
        #         )
        #     )
        for strike in option_strikes:
            for flag in ["C", "P"]:
                asset = f"UC{strike}{flag}"
                if asset in self.books and len(self.books[asset].asks) > 0:
                    # print("making")
                    penny_in_ask = float(self.books[asset].asks[0].px) - 0.1
                    penny_in_bid = float(self.books[asset].bids[0].px) + 0.1
                    if (penny_in_ask - penny_in_bid > 0.1): # as long as we didn't cross
                        requests.append(
                            self.modify_order(
                                f"{asset}",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.ASK,
                                10,
                                penny_in_ask
                            )
                        )
                        
                        requests.append(
                            self.modify_order(
                                f"{asset}",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.BID,
                                10,
                                penny_in_bid
                            )
                        )
                        for num in range(self.positions[asset] // 15):
                            requests.append(
                                self.modify_order(
                                    f"{asset}{num}",
                                    asset,
                                    pb.OrderSpecType.LIMIT,
                                    pb.OrderSpecSide.ASK,
                                    3,
                                    penny_in_ask
                                )
                            )
                        
                        ladder1_ask = float(self.books[asset].asks[0].px) + 0.5
                        ladder1_bid = float(self.books[asset].bids[0].px) - 0.5
                        requests.append(
                            self.modify_order(
                                f"{asset}_l1",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.ASK,
                                8,
                                ladder1_ask
                            )
                        )
                        requests.append(
                            self.modify_order(
                                f"{asset}_l1",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.BID,
                                6,
                                ladder1_bid
                            )
                        )
                        count += 1
                        ladder2_ask = float(self.books[asset].asks[0].px) + 1
                        ladder2_bid = float(self.books[asset].bids[0].px) - 1
                        requests.append(
                            self.modify_order(
                                f"{asset}_l2",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.ASK,
                                6,
                                ladder2_ask
                            )
                        )
                        requests.append(
                            self.modify_order(
                                f"{asset}_l2",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.BID,
                                4,
                                ladder2_bid
                            )
                        )
                        ladder3_ask = float(self.books[asset].asks[0].px) + 1.5
                        ladder3_bid = float(self.books[asset].bids[0].px) - 1.5
                        requests.append(
                            self.modify_order(
                                f"{asset}_l3",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.ASK,
                                4,
                                ladder3_ask
                            )
                        )
                        requests.append(
                            self.modify_order(
                                f"{asset}_l3",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.BID,
                                3,
                                ladder3_bid
                            )
                        )
                        ladder4_ask = float(self.books[asset].asks[0].px) + 2.5
                        ladder4_bid = float(self.books[asset].bids[0].px) - 2.5
                        requests.append(
                            self.modify_order(
                                f"{asset}_l4",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.ASK,
                                3,
                                ladder4_ask
                            )
                        )
                        requests.append(
                            self.modify_order(
                                f"{asset}_l4",
                                asset,
                                pb.OrderSpecType.LIMIT,
                                pb.OrderSpecSide.BID,
                                2,
                                ladder4_bid
                            )
                        )
            
        return requests

    async def update_options_quotes(self):
        """
        This function will update the quotes that the bot has currently put into the market.

        In this example bot, the bot won't bother pulling old quotes, and will instead just set new
        quotes at the new theoretical price every time a price update happens. We don't recommend
        that you do this in the actual competition
        """
        
        # What should this value actually be?
        # vol = self.compute_vol_estimate()
        # self.vols.append(vol)
        # print(f"DTE: {dte}")
        # print(f"Vol: {vol}")

        requests = self.add_trades()

        # day = np.floor(self.current_day)
        # dte = 26-day
        # time_to_expiry = dte / 252
        # for strike in [100]:
        #     for flag in ["C"]: # removed "P"
        #         asset_name = f"UC{strike}{flag}"
        #         theo = self.compute_options_price(flag, self.underlying_price, strike, time_to_expiry, vol)
        #         print(f"{asset_name}: {theo} per share")
        #         if strike == 100:
        #             self.calls100.append(theo*100)
        # for strike in [100]:
        #     for flag in ["P"]: # removed "C"
        #         asset_name = f"UC{strike}{flag}"
        #         theo = self.compute_options_price(flag, self.underlying_price, strike, time_to_expiry, vol)
        #         print(f"{asset_name}: {theo} per share")
        #         if strike == 100:
        #             self.puts100.append(theo*100)
        # optimization trick -- use asyncio.gather to send a group of requests at the same time
        # instead of sending them one-by-one
        responses = await asyncio.gather(*requests)
        for resp in responses:
            assert resp.ok

    # def market_closed(self):
    #     # graph price path
    #     # plt.rcParams["figure.autolayout"] = True
    #     fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex = True)
    #     y = self.price_path
    #     ax1.plot(y)
    #     ax2.plot(self.calls100)
    #     ax3.plot(self.puts100)
    #     ax4.plot(self.pnls)
    #     plt.savefig('price_path_test_9.png')


    async def handle_exchange_update(self, update: pb.FeedMessage):
        kind, _ = betterproto.which_one_of(update, "msg")

        if kind == "pnl_msg":
            # When you hear from the exchange about your PnL, print it out
            print("My PnL:", update.pnl_msg.m2m_pnl)
            print(f"Positions: {self.positions}")
            # index = self.time_tick
            # self.pnls[index] = float(update.pnl_msg.m2m_pnl)
            # for _ in range(3):
            #     if index != 999:
            #         index += 1
            #         self.pnls[index] = float(update.pnl_msg.m2m_pnl)

        elif kind == "fill_msg":
            # When you hear about a fill you had, update your positions
            fill_msg = update.fill_msg

            if fill_msg.order_side == pb.FillMessageSide.BUY:
                self.positions[fill_msg.asset] += update.fill_msg.filled_qty
            else:
                self.positions[fill_msg.asset] -= update.fill_msg.filled_qty

        elif kind == "market_snapshot_msg":
            # When we receive a snapshot of what's going on in the market, update our information
            # about the underlying price.
            self.books["UC"] = update.market_snapshot_msg.books["UC"]
            self.books["UC90C"] = update.market_snapshot_msg.books["UC90C"]
            self.books["UC95C"] = update.market_snapshot_msg.books["UC95C"]
            self.books["UC100C"] = update.market_snapshot_msg.books["UC100C"]
            self.books["UC105C"] = update.market_snapshot_msg.books["UC105C"]
            self.books["UC110C"] = update.market_snapshot_msg.books["UC110C"]
            self.books["UC90P"] = update.market_snapshot_msg.books["UC90P"]
            self.books["UC95P"] = update.market_snapshot_msg.books["UC95P"]
            self.books["UC100P"] = update.market_snapshot_msg.books["UC100P"]
            self.books["UC105P"] = update.market_snapshot_msg.books["UC105P"]
            self.books["UC110P"] = update.market_snapshot_msg.books["UC110P"]
            book = update.market_snapshot_msg.books["UC"]

            # Compute the mid price of the market and store it
            if(len(book.bids) > 0):
                self.underlying_price = (
                    float(book.bids[0].px) + float(book.asks[0].px)
                ) / 2           
            if (self.current_day != 4.995):
                await self.update_options_quotes()
            # self.update_greek_limits()
            # print(self.positions)

        elif (
            kind == "generic_msg"
            and update.generic_msg.event_type == pb.GenericMessageType.MESSAGE
        ):
            # The platform will regularly send out what day it currently is (starting from day 0 at
            # the start of the case) 
            # print(f"Positions: {self.positions}")
            self.current_day = float(update.generic_msg.message)
            self.time_tick += 1
            self.price_path.append(self.underlying_price)
            print(f"Day: {self.current_day}")
            print(f"New Price: {self.underlying_price}")
            
            # print("Underlying ", self.underlying_price)
            if (self.current_day == 4.995):
                # self.market_closed()
                pass


if __name__ == "__main__":
    start_bot(Case2)