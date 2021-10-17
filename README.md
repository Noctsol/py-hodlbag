# Summary
Python repository for my analytics project involving gathering data for crypto and running scenarios. As of right now, I want to set this up so that any developer can jsut download this and run this.


## Data
### Issues with Getting Data
Ideally, I would like to use nothing but APIs to pull the historical top 200 cryptocurrencies.However, there are problem with this:
    - The BEST cryptod data api for my use case if we include pricing, speed, information, AND FLEXIBILITY is the CryptoWatch API. However, it doesn't have any aggregated analytics like CoinMarketCap(historical snapshots).
    - Everything else is way too expensive and gives me a bunch of offering I don't need. For example:
        - CoinMarketCap requires an enterprise license to just have full access to historical. This is something like a couple grand a month. This is the case with every other API(CoinGecko, Messario.io, Nomics, etc.). 
        - Then, if we consider that you also have to pay for crap you don't even need.
        - Or they have these ONE TIME historical data deals that cost $1000+

    TLDR: Everything is trash except the CryptoWatchAPI if you are a small developer. I don't even need granular historical data of all crypto currencies. I need daily candles for the moving top 200 crypto currencies. This is not a lot of data. It shouldn't be this annoying to get. 
    
    If I figure out how to source this data, I'm coming for all you crappy companies. $25 a month for good api call rates and you can all die in a fire.

### Data Pull
We are only interested in the moving top 200 coins. Everything else is considered artificial dogshit. It's all shitcoins. Aside from the insults, I don't think it makes sense to do total market evaluations on all cryptos when the market is still young and most of it is scams. I would guess that nearly all of the value would be in top 150/200 coins/tokens anyways.

1. So we have a combination of pulling historical snapshot data from coinmarket cap with beautiful soup and Selenium. This will be used to pull the very first set of data. 
    - Why Selenium? Because companies went out of their way so that you can't webscrape data. So I just use my browser to load and let the javascript rendering run. 
    - The down side of this is that I have weekly data rather than daily. I consider to be acceptable because I'm hodling dawg. Who cares about the day to day?
    - The upside to this is this is free and I can recover data anytime I want given that I wait a couple hours
    - Ideally, when we get all of the data downloaded, I will put this on a database somewhere. Probably Digital Ocean since it doesn't cost your soul. Until then, it will probably all sit on a desktop in csv files for a while. 
    
2. Then we just call cryptowatch and coinmarketcap api daily or something like this. 




## Todo - I wrote this in 10 minutes.
- Build out basic environment to download data and define data schema
    -csv files, CSV FILES EVERYWHERE
- Build out investment/hodl(not to be confused with trading) algorithm
- Build out portfolio simulation tool
    - Initial
    - DCA
    - Buy signal
    - You should really sell signal
    - Consistent relative comparison to market /similar size caps as a whole
    - ranking movement tracking

- Stats im interested in
    - Top 10,50, 200 to total market cap
- Migrate code to Azure 
    - Migrate to Azure Cosmos DB
        - Actually, maybe not. Too expensive probably. Digitalocean might be an option
    - .Net core(only if we do this for real since python is easy to use)
 
- Build super robust alerting system
    - I literally have no clue how this will NOT be computationally expensive to run
    - As far as I know, nothing like this exists on the market


### Todo - the very far future if I decide this is useful 
- Figure out how to make website 
    - make sure mobile development is basically down in tandem
    -payment system
        - Figure out payment architecture
            - probably based on services/endpoint at different usage rates (is the most fair imo, similar to crypto watch in a way)
        - Figure out what system to use
    - user system
    - user security

- Desktop application

- Have a melt down as I'm basically running my own business at this point and try to sell.

### Todo - Marketing
- Put my money where my mouth is. If I'm selling you this, I'm sure as hell going to be using it.

