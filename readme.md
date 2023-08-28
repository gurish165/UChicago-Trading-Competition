# UTC 2022
The write up is currently underway but feel free to take a look around and give a star to come back to the project!


## About the Team

The University Of Michigan Team: <br>
Gurish Sharma<br>
Suchir Gupta<br>
Jaewoo Kim<br>
John Trager<br>
## About the Competition
https://tradingcompetition.uchicago.edu/

The competition had 3 separate cases focused on market making, trading options, and portfolio management and required participants to write trading algorithms for each case.

I've put together a slide deck to explain the competition and our stategies (click the image below to see the pdf):

[![presentaion](https://github.com/John-Trager/UChicago-Trading-Competition/blob/22458399692469a59804d697b61ec320cdc121fa/media/utc22.jpeg)](https://github.com/John-Trager/UChicago-Trading-Competition/blob/22458399692469a59804d697b61ec320cdc121fa/media/utc22.pdf)

## Case strategy breakdown
### Case 1 (3rd place)
Case 1's main objective was to market make on lumber futures. We received ~6 years historical of daily price data on lumber and monthly precipitation. With this data we were attempted to come up with a model to price the future spot price of lumber as it could be useful later for market making or market taking. We tested with various machine learning models such as SVM, TCN, and LSTM, and statistically models such as ARIMA, Exponential Smoothing, Seasonal Models, and other naive methods. Upon looking into the data we found that the trends did not have a very high seasonality correlation and the precipitation over a given month did not have a large affect on the underlying value of lumber (this is the conclusions we came to at). Most of the models we ran did not perform very well with the exception of the RNN/LSTM but we had complications with running the model with live/post training data and pivoted to focus more on the market making side of the case rather than the spot prediction.

For our market making strategy we focused on the strategies outline in [this blog](https://tianyi.io/post/chicago1/). We implemented a "penny in" strategy where we would send orders to the market one cent below the ask and 1 cent above the bid such that we would have the best bid and ask. This strategy worked well but we also thought many other teams would use a similar strategy and that we would need to create an edge. We thought that our order might fill quickly such that we could create orders outside the best bid and ask and they would still fill after some time and have a much larger spread and thus larger return. So we created "levels" outside of the penny-in spreads by set amount. For example say if we had a spread of $3.00 and $3.25, we could sel levels outside of these orders by say 5 cents so


### Case 2 (4th)
Case 2 was similar to case 1 in that we were still trading / market making but now it was options with multiple different expiration dates. Initially we approached the problem by using the black-scholes model to find a strategy to market take but were unable to come up with a stable strategy. We instead took inspiration from our Case 1 algorithm and decided to market-make on all the different options. This worked well but was extremely risky as we initially didn't have a way to hedge or limit our risk. To deal with this when one of our positions became to long on a given side of an option we would purchase options on the opposite side. For example if we were holding a long position that was too large (by our predefined risk limit) we would open a short position in the same contract (basically closing our long position). This worked to limit our risk and volatility in our gain during the trading cycle, however we failed to take into account closing all of our positions before our trading period ended (thus leaving use with some losses after cash settlement of our contracts). This cost our position from 1st -> ~4th.

### Case 3 (7th)
Case 3 was portfolio optimization (optimizing for Sharpe Ratio). We were given a basket of stocks and their historical price for some years. We were also given investors forecast for each of the stocks. We took this data and used Blacklitterman portfolio optimization. It worked to put us in the middle of the pack but didn't work amazing. From what was heard it may be worth looking into some RL method or Markov Chains.

## Results + Debrief
Our team ended 3rd for case1 of market making, roughly 4th for case 2, and around 7th for the third case. In the end we won 2nd overall.

### Things to consider
Case1:
- running multiple threads for market making so that our orders update much faster
- fooling other players by putting bogus bid/asks towards the beginning
- using aggressive trading: penny in + levels
- finding a way to maximize trades while not going over position limit (being able to close out of large positions)

Case2:
- Close out of positions before the end of the round (otherwise when the contracts are cash-settled based on the black-sholes model we could lose a lot of money if we are on the wrong side of the trade - which happened to us taking use from 1st to ~4th), if we had a good theo price then we could use market taking to hedge our profits but with increased volatility
- A strat we used that worked really well to give us consistent gains (before contracts cash-settle) was to hedge our bets by placing positions on the opposite side of orders if they became too large. So for example if we were holding a long position that was too large (by our predefined risk limit) we would open a short position in the same contract (basically closing our long position). This worked to limit our risk and volatility in our gain during the trading cycle, however we failed to take into account closing all of our positions before our trading period ended (thus leaving use with some losses after cash settlement of our contracts)
- it's hard to test market making strategies when there is little volume, so in order to test in a comp like setting we need to run with a liquid market (ie many bots trading at the same time)

Case3:
- maybe used RL or some form of machine learning as Blacklitterman worked but not super well or used a more aggressive pairs trading

## Fintech / Trading Industry Takeaways
- Many trading firms have added crypto trading desks within the past year
    - ctc mentioned trading with offshore accounts (as in the US it is not legal yet)
- Getting a quant/SWE interview is just a matter of networking, having a strong resume (job, experince, projects, competitions etc)


## Running the Code
The code is pretty disorganized as it was all put together very quickly. If there is a enough demand I may consider coming back and trying ot run the code.
