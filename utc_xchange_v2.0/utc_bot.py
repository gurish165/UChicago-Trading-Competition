#!/usr/bin/env python
# utc_bot.py - A parent class for all bots that trade on the live exchange for
# the 2022 UChicago Trading Competition

import argparse
import asyncio
import random
import sys
import os
import warnings
from datetime import datetime


from typing import Type, Dict, Any, Callable, Optional
import betterproto

from grpclib.client import Channel
from grpclib.exceptions import StreamTerminatedError

import proto.utc_bot as pb


class XChangeWarning(Warning):
    pass


def panic_exc_handler(
    cleanup: Callable[[], None],
) -> Callable[[asyncio.AbstractEventLoop, Dict[str, Any]], Any]:
    """Creates function that can handle exceptions raised by asyncio tasks."""

    def handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]):

        if "exception" in context:
            if isinstance(context["exception"], StreamTerminatedError):
                print(" > Connection to server terminated, shutting down...")
            elif "future" in context and isinstance(context["future"], asyncio.Task):  # type: ignore
                context["future"].print_stack()
            else:
                print(context["exception"])

        cleanup()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(-1)  # type: ignore

    return handler


class UTCBot:
    """
    A bot that will trade in the 2021 UChicago Trading Competition. Should be
    subclassed by competitors when creating their bots.
    """

    def __init__(self, username: str, key: str, host: str, port: int):
        """
        Initializes the bot for trading in the 2021 UTC

        Args:
            username (str): The username to use when registering the bot
            key (str): The private key used to identify the competitor
            host (str): The IP Address or URL used to locate the exchange
            port (int): The port that the exchange is running on
        """
        if username == "":
            username = f"{type(self).__name__}_{random.randrange(0, 10000):04}"
            print(f" > No username provided, using {username}")

        self.creds = pb.Credentials(username, key)
        self.__channel = Channel(host, port)
        self.__service_stub = pb.ExchangeServiceStub(self.__channel)
        self.__time_differential: "Optional[float]" = None

    async def place_order(
        self,
        asset_code: str,
        order_type: pb.OrderSpecType,
        order_side: pb.OrderSpecSide,
        qty: int,
        px: "Optional[float]" = None,
    ) -> pb.PlaceOrderResponse:
        """
        Place an order on the exchange

        Args:
            asset_code (str): The code of the asset to place an order for
            order_type (pb.OrderSpecType): The type of order this is
            order_side (pb.OrderSpecSide): The side of the order
            qty (int): The # of lots of the asset to buy
            px (Optional[float]): The price to buy/sell at. Not required if this
            is a market order.

        Returns:
            pb.PlaceOrderResponse The response from the exchange
        """

        if order_type != pb.OrderSpecType.MARKET and px is None:
            raise Exception(
                f"Error placing order: order type was {order_type.name} but price was not specified"
            )

        resp = await self.__service_stub.place_order(
            creds=self.creds,
            order=pb.OrderSpec(
                type=order_type,
                side=order_side,
                asset=asset_code,
                quantity=qty,
                price=f"{px:.8f}" if px is not None else "",
            ),
        )

        return resp

    async def modify_order(
        self,
        order_id: str,
        asset_code: str,
        order_type: pb.OrderSpecType,
        order_side: pb.OrderSpecSide,
        qty: int,
        px: "Optional[float]" = None,
    ) -> pb.ModifyOrderResponse:
        """
        Modify an order that you've already placed (equivalent to atomic cancel + place)

        Args:
            order_id (str): The ID of the order to replace
            asset_code (str): The code of the asset
            order_type (pb.OrderSpecType): The type of order this is
            order_side (pb.OrderSpecSide): The side of the order
            qty (int): The # of lots of the asset to buy
            px (Optional[float]): The price to buy/sell at. Not required if this
            is a market order.

        Returns:
            pb.ModifyOrderResponse Whether the modify was successful and the full response
        """

        if order_type != pb.OrderSpecType.MARKET and px is None:
            raise Exception(
                f"Error modifying order: order type was {order_type.name} but price was not specified"
            )

        resp = await self.__service_stub.modify_order(
            creds=self.creds,
            order_id=order_id,
            new_order=pb.OrderSpec(
                type=order_type,
                side=order_side,
                asset=asset_code,
                quantity=qty,
                price=f"{px:.8f}" if px is not None else "",
            ),
        )
        return resp

    async def cancel_order(self, order_id: str) -> pb.CancelOrderResponse:
        """
        Cancel an order

        Args:
            order_id (str): The ID of the order to cancel

        Returns:
            pb.CancelOrderResponse The response sent back from the exchange
        """

        resp = await self.__service_stub.cancel_order(
            creds=self.creds, order_id=order_id
        )

        return resp

    async def handle_exchange_update(self, update: pb.FeedMessage):
        """Handle updates coming from the exchange"""
        # TODO when you subclass this bot, you should implement this
        pass

    async def handle_round_started(self):
        """Handle a round being started. Is only called if registration was successful"""
        # TODO when you subclass this bot, you should implement this
        pass

    async def start(self):
        """
        Registers the client with the exchange as a competitor (if not
        registered already), waits for the case to start, and starts streaming
        exchange updates once the round starts
        """

        # Register the competitor on the exchange
        while True:
            try:
                reg_resp = await self.__service_stub.register(creds=self.creds)
                break
            except OSError:
                print(" > Unable to connect to exchange... Trying again in 5s")
                await asyncio.sleep(5)

        if not reg_resp.ok:
            print(" > Invalid registration attempt: " + reg_resp.message)
            sys.exit(-1)
            return

        print(" > Registration successful. Waiting for trading to start...")

        # Wait for the case to start
        # TODO: is it necessary to add a timeout here? Needs to be tested
        start_resp = await self.__service_stub.await_trading_start(creds=self.creds)
        if not start_resp.started:
            print(
                " > Unable to await case start: likely due to request timeout or round ending"
            )
            sys.exit(-2)

        print(" > Trading has begun. Starting to handle exchange updates...")

        # Call the competitor's startup hook
        await self.handle_round_started()
        await self.main_loop()

    async def main_loop(self):
        # Request and update stream from the exchange
        update_stream = self.__service_stub.stream_messages(creds=self.creds)
        async for update in update_stream:
            self.preprocess_message(update)
            await self.handle_exchange_update(update)

    def preprocess_message(self, update: pb.FeedMessage):
        """
        Check if the message is something concerning. If it is, print out a warning to the console
        to let competitors know
        """
        msg_type, _ = betterproto.which_one_of(update, "msg")
        if msg_type == "request_failed_msg":
            warnings.warn(
                "REQUEST_DENIED: " + update.request_failed_msg.message,
                XChangeWarning,
            )
        if msg_type == "liquidation_msg":
            warnings.warn(
                "LIQUIDATION: " + update.liquidation_msg.message,
                XChangeWarning,
            )
        if msg_type == "generic_msg":
            event_type = update.generic_msg.event_type
            if event_type != pb.GenericMessageType.MESSAGE:
                warnings.warn(
                    f"{pb.GenericMessageType(event_type).name}: {update.generic_msg.message}",
                    XChangeWarning,
                )
        if msg_type == "market_snapshot_msg":
            ts_time = datetime.fromisoformat(update.market_snapshot_msg.timestamp)
            diff = datetime.now().timestamp() - ts_time.timestamp()

            if self.__time_differential is None:
                self.__time_differential = diff
            elif diff - self.__time_differential > 2:
                warnings.warn(
                    f"DESYNC: bot is receiving messages faster than it is processing them ({int(diff - self.__time_differential)}s behind)",
                    XChangeWarning,
                )

            self.__time_differential = min(self.__time_differential, diff)

    def cleanup(self):
        """Cleans up any loose ends"""
        self.__channel.close()


def __formatwarning(message, category, filename, lineno, line=None):
    return f"[{category.__name__}] {message}\n"


def start_bot(bot_type: Type[UTCBot]):
    """
    Parse command-line arguments in the standard way and start the provided bot
    """

    # Tune this in your own bot files to have the warnings issued by the UTC bots do different
    # things. If you want to be confident that your bot runs without any errors or strange behavior,
    # you can even try having them raise Exceptions, though I wouldn't recommend doing this on the
    # day of the competition (because there isn't a way to catch these exceptions)
    warnings.filterwarnings("always", category=XChangeWarning)
    warnings.formatwarning = __formatwarning

    parser = argparse.ArgumentParser(
        description=bot_type.__doc__
        or "Fill out the docstring of your bot to provide a description for this help text"
    )

    parser.add_argument(
        "username",
        metavar="USERNAME",
        type=str,
        help="The username of the competitor (defaults to randomly generated)",
        default="",
        nargs="?",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        help="The key used to authenticate the competitor (prevents other bots from placing order on your behalf. Defaults to 'password')",
        default="password",
    )
    parser.add_argument(
        "-t",
        "--host",
        type=str,
        default="localhost",
        help="The URL of the host (defaults to localhost)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=9090,
        help="The port of the competitor gRPC server (defaults to 9090)",
    )

    args = parser.parse_args()
    bot = bot_type(args.username, args.key, args.host, args.port)

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(panic_exc_handler(bot.cleanup))
    try:
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        print(" > Keyboard interrupt received, terminating...")
    except StreamTerminatedError:
        pass
    finally:
        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == "__main__":
    start_bot(UTCBot)
