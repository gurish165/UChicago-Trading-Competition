# bot notes
At the start of a trading session there may be a few messages before the initial rain report (where we shouldn't trade - at least I don't think so). Once we get the initial rain report that means we are on day 1 of 252 and we should start trading.

START: start trading once we read in the weather report

M2M pnl: mark to market pnl
https://www.investopedia.com/ask/answers/06/realizedprofitsvsunrealizedprofits.asp
https://www.investopedia.com/terms/m/marktomarket.asp


Note:

In this case, the exchange computes M2M pnl taking the market price of asset to be (best bid + best ask)/2.

Note that the realized pnl reported by the exchange does NOT take into account the settlement of expired future contracts.

At the end of each round, all remaining future positions will be liquidated at the respective settlement price of each contract. The pnl from this is then added to the existing realized pnl to get the final pnl which you are scored on.

M2M pnl is not used in scoring, so you may simply treat it as an additional piece of information that the exchange provides you with. This may (or may not) be useful when you do not know the exact settlement prices of the contracts. You may of course also compute your own M2M pnl by using a different formula for the "market price" of asset.