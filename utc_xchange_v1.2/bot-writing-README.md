## Writing Your First Bot Tutorial
##### by the xchange dev team

Confused about how to get started writing a bot for the UTC cases? Here's a quick simple rundown on how to get a basic bot running and trading on the exchange with our example case. 

***

#### First Steps
First, lets start creating our bot by subclassing the UTCBot. Remember to also import the necessary libraries / files



```
from utc_bot import UTCBot, start_bot
import proto.utc_bot as pb
import betterproto

class ExampleBot(UTCBot):
```



This gives our bot access to the functions such as placing / modifying and cancelling orders on the exchange. Taking a look at utc_bot.py we see that there are key class functions we have to implement: ```handle_round_started``` and ```handle_exchange_update```.

&nbsp;
***

#### Handling Round Start
Let's first handle what our bot does when the round starts. One way to do this is to set a START_PRICE our bot trades at, and declare a ```fair_value``` variable in our bot to hold this start price value. 

```
async def handle_round_started(self):
        self.fair_value = <START_PRICE>
```

Similarly, we also initialize the bid_order_id and ask_order_id variables which will be useful for modifying or cancelling the orders later. You can choose other data structures to store these values if so you require, or not at all. 
```
async def handle_round_started(self):
        self.fair_value = <START_PRICE>
        self.bid_order_id = ""
        self.ask_order_id = ""
```

Now, let's create a function to update quotes that are currently on the market. We can call this function update_quotes. We will update quotes with these following simple rules. Note that we also have several variables which are in \<arrow brackets\> to indicate that these variables which affect the performance of the bot we are creating to an extent beyond basic interaction functionality with the exchange.



```
async def update_quotes(self):
```
Let's now use a simple calculation for the bid and ask price for our limit orders. 
```
        bid_price = round(self.fair_value - <QUOTER_WIDTH> / 2)
        ask_price = round(self.fair_value + <QUOTER_WIDTH> / 2)
        print("Quoting : ", (bid_price, ask_price))
```
If the previous bid order we sent is still on the market, MODIFY it to have a new price. If it is no longer on the market, then PLACE a new order
```
        resp = await self.modify_order(
            self.bid_order_id,
            "RNDO",
            pb.OrderSpecType.LIMIT,
            pb.OrderSpecSide.BID,
            <QUOTE_AMOUNT>,
            bid_price,
        )
        self.bid_order_id = resp.order_id

```


We do the same thing for the ask side. 
```

        resp = await self.modify_order(
            self.ask_order_id,
            "RNDO",
            pb.OrderSpecType.LIMIT,
            pb.OrderSpecSide.ASK,
            <QUOTE_AMOUNT> ,
            ask_price,
        )
        self.ask_order_id = resp.order_id
```

Great! Now we have an update quotes function, which we can add to the bottom of our ```handle_round_started``` function. 

&nbsp;
***

#### Handling Exchange Updates
Next, we go on to the second function which we have to implement, which is the ```handle_exchange_update``` function. This function is called when the bot receives an update from the platform. These updates
provide you with information about what is going on in the markets, what has happened to the orders you have placed, what your PnL is, and information about the announcements. In the provided code, the bot will:    
- Use fill information to check whether its quotes have been fully traded against    
- Update its fair value based on announcements    
- Print out it's PnL (marked to market)

You can easily extend this code to take advantage of the other pieces of information that you receive from the exchange.

```
async def handle_exchange_update(self, update: pb.FeedMessage):
```
We now want to check the type of message we are receiving. Let's figure out by using the ```which_one_of``` function.

```
        kind, _ = betterproto.which_one_of(update, "msg")
```

From here, you can see the class FeedMessage in the competitor's documentation to see the difference kinds of messages aailable. 
For the purposes of this example bot, we will be handling just a few of these cases. We do so by using a if-else loop. The following is an example of how to run such a bot, and should not be lifted for competition purposes since it is specific to an example trading case. 

```
        # Contains messages that have information about fills that this bot has participated in.
        if kind == "fill_msg":
            _ = update.fill_msg

        # Received the announcement data from the platform and use that to adjust your fair value
        elif kind == "generic_msg":
            generic_msg = update.generic_msg

            # Check if this is a message relevant to the competition
            if generic_msg.event_type == pb.GenericMessageType.MESSAGE:
                self.fair_value = float(generic_msg.message)
                print("New fair:", self.fair_value)
                await self.update_quotes()
            else:
                print("Generic Message :", generic_msg)

        # If a request to place an order fails, a message of this kind will be sent
        elif kind == "request_failed_msg":
            print("request failed :", update.request_failed_msg)

        # Print out your PnL
        elif kind == "pnl_msg":
            print("PnL :", update.pnl_msg.m2m_pnl)

        # Don't do anything if your receive information about a trade that occurred in the market or
        # a full market snapshot. Feel free to start using this data--there may be hidden
        # information you can find by doing so.
        elif kind == "trade_msg" or kind == "market_snapshot_msg":
            pass
```

Note that currently we are only updating our fair value (and also quotes) based on the generic message received by our bot from the exchange, which is relevant for our example trading game. Do note that you have to implement your own methods of pricing the asset(s) depending on the specific cases.  

Great! If you have followed our documentation, we are mostly done with creating your very first bot!

All that is left to do is to start the bot when the script is run with the following:
```
if __name__ == "__main__":
    start_bot(ExampleBot)
```

&nbsp;
***

#### Running Your Bot & Connecting to the Exchange
When the exchange is running, you should connect by running your bot as such 
```
python3  example_bot.py <username> -k <key> -t 18.221.92.203
```
replacing username and key (arrow brackets included) with the username and key that we have given you for the competition. 

