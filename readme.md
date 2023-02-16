# University of Michigan UChicago Midwest Trading Competition 2022 - 2nd Place Overall

## Code
I apologize, I have not read through the code in a while and I forgot which code we ran at the competition. Feel free to take a guess which Python file we actually used.

## About the competition

The competition had 3 separate cases focused on market making, trading options, and portfolio management and required participants to write trading algorithms for each case.

## Case 1: Market Making (3rd Place)

### Case 1: Overview
Case 1's main objective was to market make on lumber futures. We received ~6 years historical of daily price data on lumber and monthly precipitation. With this data we were attempted to come up with a model to price the future spot price of lumber as it could be useful later for market making or market taking. We tested with various machine learning models such as SVM, TCN, and LSTM, and statistically models such as ARIMA, Exponential Smoothing, Seasonal Models, and other naive methods. Upon looking into the data we found that the trends did not have a very high seasonality correlation and the precipitation over a given month did not have a large affect on the underlying value of lumber (this is the conclusions we came to at). Most of the models we ran did not perform very well with the exception of the RNN/LSTM but we had complications with running the model with live/post training data and pivoted to focus more on the market making side of the case rather than the spot prediction.

### Case 1: Recommended Strategy
It is recommended to predict a "fair" price to create a marketing making algorithm that maximizes profits while maanging risk. If you knew the market price was above the "fair" price, you should take a short position. If you knew the market price was below "fair" price, you should take a long position. In general you should make as many trades as possible while minimizing the amount of contracts you hold.

### Case 1: Our Strategy
Screw the fair price and screw risk. We implemented a "penny in" strategy where we would send orders to the market one cent below the ask and 1 cent above the bid such that we would have the best bid and ask (while also making sure our prices do not cross over each other). This strategy worked well but we also thought many other teams would use a similar strategy and that we would need to create an edge. We thought that our order might fill quickly such that we could create orders outside the best bid and ask and they would still fill after some time and have a much larger spread and thus larger return. So we created "levels" outside of the penny-in spreads by set amount.

Let's say the order-books's best bid is $3.00 and the best ask is $3.25. We would submit a bid for $3.01 and submit an ask for $3.24. A dumb market player will submit a buy order for $3.25 because that is what they saw in the orderbook so they would expect it to be filled. But we intercepted that price and their bid for $3.25 would first get matched to our ask for $3.24, making us profit. 

We also want to implement "levels" so that if someone places a bid at $10 for an absurd quantity, they would eat through all the asks on the book from the lowest ask up to $10. It is important to understand that the timing of order placement is not synchronized among the participants. So we want our "levels" to be on the books at all times so if the occasional "dumb" order comes in for a absurd price and quantity, our orders on the books are ready to match them. So if the order-books's best bid is $3.00 and the best ask is $3.25, you could place bids at $2.90, $2.75, and $2.55. You could place asks at $3.35, $3.50, and $3.70. The level distance and quantity is chosen experimentally and this strategy is not effective if your competition knows what they are doing.

### Case 1: Improvements
The winning team implemented the same strategy as us, but their orders were able to get on the books faster then us. They claimed to be using multi-threading/multi-processing to send more orders to the exchange. In most of these trading competitions (Berkely, Jane Street ETC, MIT, etc) this is not possible because they rate limit your requests to the exchange. Another team that did well used the first 10 seconds of every round to send huge quantities of bogus trades. These are trades that have absurdly wide spreads and quantities. We also should have written a function that clears out our positions at the end of the round. This also would have been useful for Case 2.

### Case 2: Options Trading (4th Place**)
** We scored 1st every round and had the most PnL in this case but we did not clear our positions. The judges brought us down a few rankings for this <sb>subjective</sb> reason.

### Case 3: Portfolio Management (7th Place)



Case2:
- Close out of positions before the end of the round (otherwise when the contracts are cash-settled based on the black-sholes model we could lose a lot of money if we are on the wrong side of the trade - which happened to us taking use from 1st to ~4th), if we had a good theo price then we could use market taking to hedge our profits but with increased volatility
- A strat we used that worked really well to give us consistent gains (before contracts cash-settle) was to hedge our bets by placing positions on the opposite side of orders if they became too large. So for example if we were holding a long position that was too large (by our predefined risk limit) we would open a short position in the same contract (basically closing our long position). This worked to limit our risk and volatility in our gain during the trading cycle, however we failed to take into account closing all of our positions before our trading period ended (thus leaving use with some losses after cash settlement of our contracts)
- it's hard to test market making strategies when there is little volume, so in order to test in a comp like setting we need to run with a liquid market (ie many bots trading at the same time)

Case3:
- maybe used RL or some form of machine learning as Blacklitterman worked but not super well or used a more aggressive pairs trading

