# xChange Python API Reference
## Important Functions 
<code>**place_order(** *self*, *asset_code*, *order_type*, *order_side*, *qty*, *px* **)**</code>
> Places an order on the exchange
> 
> **Arguments**:<br/>
>`asset_code` (<code style="color:#147a62">str</code>)
The code of the asset to place an order for<br/>
>`order_type` (<code style="color:#147a62">pb.OrderSpecType</code>)
The type of order (e.g. limit order, market order, etc.)<br/>
>`order_side` (<code style="color:#147a62">pb.OrderSpecSide</code>)
The side of the order<br/>
>`qty` (<code style="color:#147a62">int</code>)
The # of lots of the asset to buy/sell<br/>
>`px` (<code style="color:#147a62">Optional[float]</code>)
The price to buy/sell at. Not required if this is a market order.
> 
> **Returns** (<code style="color:#147a62">pb.PlaceOrderResponse</code>):
The response from the exchange

<br/>

<code>**modify_order(** *self*, *order_id*, *asset_code*, *order_type*, *order_side*, *qty*, *px* **)**</code>
> Modify an order that you've already placed. If no order corresponding to the specified `order_id`
> exists, this will place the new order anyway. This makes this function particularly useful for
> maintaining quotes on a book
>
>`order_id` (<code style="color:#147a62">str</code>)
The ID of the order to replace<br/>
>`asset_code` (<code style="color:#147a62">str</code>)
The code of the asset to modify<br/>
>`order_type` (<code style="color:#147a62">pb.OrderSpecType</code>)
The type of order (e.g. limit order, market order, etc.)<br/>
>`order_side` (<code style="color:#147a62">pb.OrderSpecSide</code>)
The side of the order<br/>
>`qty` (<code style="color:#147a62">int</code>)
The # of lots of the asset to buy/sell<br/>
>`px` (<code style="color:#147a62">Optional[float]</code>)
The price to buy/sell at. Not required if this is a market order.
>
> **Returns** (<code style="color:#147a62">pb.ModifyOrderResponse</code>):
The response from the exchange

<br/>

<code>**cancel_order(** *self*, *order_id* **)**</code>
> Cancel the order with the specified id
>
>`order_id` (<code style="color:#147a62">str</code>)
The ID of the order to cancel<br/>
>
> **Returns** (<code style="color:#147a62">pb.CancelOrderResponse</code>):
The response from the exchange

<br/>

***
<!-- Insert a page break because the stuff above happens to be just the right length -->
<div style="page-break-after: always"></div> 

## Important Classes
<code>class pb.**PlaceOrderResponse**</code>
> A response to a request to place an order
>
> **Fields**:<br/>
>`ok` (<span style="color:#147a62">bool</span>)
>Whether the request was successful
> - If `True`, the order has been scheduled for creation. It may still be rejected with a
>   `RequestFailedMessage'
> - if `False`, request failed and no order will be placed
>
>`order_id` (<span style="color:#147a62">str</span>)
>If `ok=True`, this is the ID of the order that was scheduled for creation<br/>
>`message` (<span style="color:#147a62">str</span>)
>Message about why the request to place an order may have failed<br/>

<br/>

<code>class pb.**ModifyOrderResponse**</code>
>A response to a request to modify an order
>
> **Fields**:<br/>
>`ok` (<span style="color:#147a62">bool</span>)
>Whether the request was successful<br/>
> - If `True`, the order has been scheduled for modification. It may still be rejected with a
>   `RequestFailedMessage'
> - if `False`, request failed and no order will be modified
>
>`order_id` (<span style="color:#147a62">str</span>)
>If `ok=True`, this is the ID of the order that was scheduled for creation<br/>
>`message` (<span style="color:#147a62">str</span>)
>Message about why the request to modify an order may have failed<br/>

<br/>


<code>class pb.**CancelOrderResponse**</code>
>A response to a request to cancel an order
>
> **Fields**:<br/>
>`ok` (<span style="color:#147a62">bool</span>)
>Whether the request was successful<br/>
> - If `True`, the order has been scheduled for cancellation. It may still be rejected with a
>   `RequestFailedMessage'
> - if `False`, request failed and no order will be cancelled
>
>`message` (<span style="color:#147a62">str</span>)
>Message about why the request to cancel the order may have failed<br/>

<br/>

<code>class pb.**FeedMessage**</code>
> A message sent from the exchange to the competitor that can be processed in the
> `handle_exchange_update` method of your bot. Exactly one of the following fields will actually be
> populated. To find out which one, you can call
> ```python
>   kind, _ = betterproto.which_one_of(feed_message, "msg")
> ```
> After this, kind will be a string containing the name of the populated field (e.g.
> `kind=="pnl_msg"` if and only if `feed_message.pnl_msg` is populated). See the example bots for
> more details.
>
> **Fields**:<br/>
>`request_failed_msg` (<span style="color:#147a62">pb.RequestFailedMessage</span>)
> A message that tells you that your request to place/modify/cancel an order has failed<br/>
>`pnl_msg` (<span style="color:#147a62">pb.PnLMessage</span>)
> An update containing PnL information for the competitor<br/>
>`trade_msg` (<span style="color:#147a62">pb.TradeMessage</span>)
> A message containing info about a recent trade that occurred<br/>
>`fill_msg` (<span style="color:#147a62">pb.FillMessage</span>)
> A message that tells you about an order of yours that filled.<br/>
>`market_snapshot_msg` (<span style="color:#147a62">pb.MarketSnapshotMessage</span>)
> A message containing a snapshot of the order books for every asset<br/>
>`liquidation_msg` (<span style="color:#147a62">pb.LiquidationMessage</span>)
> (*irrelevant for this year's competition*)<br/>
>`order_cancelled_msg` (<span style="color:#147a62">pb.OrderCancelledMessage</span>)
> A message indicating that orders have been cancelled (can occur intentionally or unintentionally)
> <br/>
>`generic_msg` (<span style="color:#147a62">pb.GenericMessage</span>)
> A miscellaneous message sent through the update stream. Watch this for important information updates
> from the exchange about the case.<br/>

<br/>

<code>class pb.**RequestFailedMessage**</code>
> Response sent when a request to place an order has failed. If this message is received, then the
> request corresponding to the provided order IDs could not be completed
>
> **Fields**:<br/>
>`type` (<code style="color:#147a62">pb.RequestFailedMessageType</code>)
> The type of the failed request that was sent (i.e. whether it was to place/modify/cancel an order)<br/>
>`place_order_id` (<code style="color:#147a62">str</code>)
> The ID of the order that was unsuccessfully placed (or used to replace an old order), if any<br/>
>`cancel_order_id` (<code style="color:#147a62">str</code>)
> The ID of the order that was unsuccessfully cancelled (or replaced), if any<br/>
>`message` (<code style="color:#147a62">str</code>)
> The message associated with the failed request<br/>
>`asset` (<code style="color:#147a62">str</code>)
> Asset code that the request was sent for<br>
>`timestamp` (<code style="color:#147a62">str</code>)
> Timestamp that the failure was noted<br/>

<br/>

<code>enum pb.**RequestFailedMessageType**</code>
> Represents the type of request that failed in a `pb.RequestFailedMessage`.
>
> **Members**: `PLACE`, `MODIFY`, `CANCEL`

<br/>

<code>class pb.**PnlMessage**</code>
> An update containing PnL information for the competitor
>
> **Fields**:<br/>
>`realized_pnl` (<code style="color:#147a62">str</code>)
> The PnL of the competitor<br/> 
>`m2m_pnl` (<code style="color:#147a62">str</code>)
> Marked to Market PnL (a more accurate measure of your performance)<br/>
>`timestamp` (<code style="color:#147a62">str</code>)
> The timestamp when this update was created<br/>

<br/>

<code>class pb.**TradeMessage**</code>
>A message containing info about a recent trade that occurred
>
> **Fields**:<br/>
>`asset` (<code style="color:#147a62">str</code>)
> The asset that the trade occurred in<br/>
>`price` (<code style="color:#147a62">str</code>)
> The price that the trade occurred at<br/>
>`qty` (<code style="color:#147a62">int</code>)
> The quantity of the trade<br/>
>`timestamp` (<code style="color:#147a62">str</code>)
> The timestamp at which this trade occurred<br/>

<br/>

<code>class pb.**FillMessage**</code>
>An update containing info about a recent order fill that occurred. **These messages are only sent
>to the users affected by the fill**
>
> **Fields**:<br/>
>`order_id` (<span style="color:#147a62">str</span>) 
> The ID of the order that was filled<br/>
>`asset` (<span style="color:#147a62">str</span>) 
> The asset that was filled<br/>
>`order_side` (<span style="color:#147a62">pb.FillMessageSide</span>) 
> The side that the competitor was on.
> - If `order_side==BUY`, then this fill resulted in you buying the asset
> - If `order_side==SELL`, then this fill resulted in you selling the asset
>
>`price` (<span style="color:#147a62">str</span>) 
> The price level that was filled at<br/>
>`filled_qty` (<span style="color:#147a62">int</span>) 
> The quantity that was filled<br/>
>`remaining_qty` (<span style="color:#147a62">int</span>) 
> The remaining quantity in the order<br/>
>```timestamp``` / <span style="color:#147a62">str</span>: 
> The timestamp at which the fill was processed<br/>

<br/>

<code>enum pb.**FillMessageSide**</code> 
>Contains information about the side that fill occurred on
> 
> **Members**: `BUY`, `SELL`

<br/>

<code>class pb.**MarketSnapshotMessage**</code>
>Update containing information on books for every asset
>
> **Fields**:<br/>
>`books` (<span style="color:#147a62">Dict[str, pb.MarketSnapshotMessageBook]</span>) 
> map from asset code to a snapshot of the order book associated with that asset<br/>
>`timestamp` (<span style="color:#147a62">str</span>) 
> The time at which the market info was found<br/>

<br/>

<code>class pb.**MarketSnapshotMessageBook**</code>
>Information for individual asset within whole book update
>
> **Fields**:<br/>
>`asset` (<span style="color:#147a62">str</span>) 
> The asset associated with the book<br/>
>`bids` (<span style="color:#147a62">List[pb.MarketSnapshotMessageBookPriceLevel]</span>) 
> The bid price levels<br/>
>`asks` (<span style="color:#147a62">List[pb.MarketSnapshotMessageBookPriceLevel]</span>) 
> The ask price levels containing qty and px<br/>

<br/>

<code>class pb.**MarketSnapshotMessageBookPriceLevel**</code>
> Quantities at each Price Level 
>
> **Fields**:<br/>
>`px` (<span style="color:#147a62">str</span>) 
> The price associated with this level. Note that this stored as a string in order to preserve precision<br/>
>`qty` (<span style="color:#147a62">int</span>) 
> The total quantity associated with this price level on the book<br/>

<br/>

<code>class pb.**GenericMessage**</code>
>A misc. event sent through the update stream. The `event_type` can be used to interpret the context
>surrounding the `message` text
>
> **Fields**:<br/>
>`event_type` (<span style="color:#147a62">pb.GenericMessageType</span>) 
> The type of exchange event that was sent through the feed<br/>
>`message` (<span style="color:#147a62">str</span>) 
> The message text associated with that event<br/>

<br/>

<code>enum pb.**GenericMessageType**</code>
> Represents the type of a generic message sent over the data feed
>
> **Members:** `MESSAGE`, `MESSAGE`, `INTERNAL_ERROR`, `COMPETITOR_DEACTIVATED`, `CHANNEL_REPLACED`, `ROUND_ENDED`, `RISK_LIMIT_BROKEN`

<code>class pb.**LiquidationMessage**</code>
> _not relevant for this year's competition_
<!-- >Response containing status of order request
>
>`message` (<span style="color:#147a62">str</span>) 
> The message associated with the liquidation<br/>
>`order_id` (<span style="color:#147a62">str</span>) 
> The order ID associated with the market order (so they can match fill to risk violation)<br/>
>`asset` (<span style="color:#147a62">str</span>) 
> Asset code of order<br/>
>`timestamp` (<span style="color:#147a62">str</span>) 
> Timestamp that market order was *initiated*<br/> -->

<code>class pb.**OrderCancelledMessage** (**NEW IN v1.0.4**)</code>
> A message sent to competitors when some of their orders were cancelled. This can happen for two main
reasons:
>  - The competitor sent in a request to cancel the specified order and this request went through
>  - The competitor's order was cancelled automatically by the exchange when the competitor went
>    over risk limits
>
>`order_ids` (<span style="color:#147a62">List[str]</span>) 
> The order IDs of the orders that was cancelled<br/>
>`asset` (<span style="color:#147a62">str</span>) 
> Asset code of order that was cancelled<br/>
>`intentional` (<span style="color:#147a62">bool</span>)
> Whether the cancellation was intentional on the part of the competitor (i.e. a result of a
> cancellation request) or not (i.e the competitor's order was cancelled automatically)
>`message` (<span style="color:#147a62">str</span>)
> If the cancellation was unintentional, a message explaining the reason for cancellation
>`timestamp` (<span style="color:#147a62">str</span>) 
> Timestamp when the cancellation occurred<br/>

<br/>

***