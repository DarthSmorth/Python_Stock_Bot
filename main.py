import finnhub #Loads the finnhub library
from datetime import datetime, timedelta #Imports tools from Pythons built-in datetime module, datetime-gives you the current date/time (like a clock) and timedelta-lets you do math with time (like "3 days ago")
news_block = "" #Collect all news strings
api_key = 'cvusrjpr01qjg13baol0cvusrjpr01qjg13baolg' #Saving personal API key into a variable for easy reuse
finnhub_client = finnhub.Client(api_key=api_key) #Creates a connection object that lets you talk to Finnhub's API using key

import requests
from bs4 import BeautifulSoup
import time

def get_top_moomoo_tickers():
    url = 'https://www.moomoo.com/quote/us/stock-list/all-us-stocks/top-gainers'
    headers = {'User-Agent': 'Mozilla/5.0'}


    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    tickers = []
    for span in soup.select('span.code.ellipsis'):
        ticker = span.text.strip()
        tickers.append(ticker)

    return tickers[:10] 

while True:

    watchlist = get_top_moomoo_tickers() #Defining a list (tickers I want to scan)

    today = datetime.today().strftime('%Y-%m-%d') #gives the current date & time, e.g. 2025-04-15 14:23:09.123456, "strftime" converts it into a clean string "2025-04-15"
    three_days_ago = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d') #Creates a 3-day chunk of time using "timedelta(days=3)", subtracts 3 days from today using "datetime.today() - timedelta(days=3)", and converts it all into a clean string "three_days ago = "2025-04-12"

    enable_news= False #Set to false to skip headlines/news updates
    news_limit= 1

    print("=" * 40)
    print("💸 STONKS TO CONSIDER 💸")
    print("=" * 40)

    for symbol in watchlist: #Saying every stock code in my list do the stuff below
        quote = finnhub_client.quote(symbol) #Calls the API for that stock and returns a dictionary 

        current_price = quote['c'] #Current price-live price rn, after market last closed
        prev_close = quote['pc'] #Previous close price-price when the market last closed
        change = current_price - prev_close #Calculates the dollar change from now and then
        percent_change = (change / prev_close) * 100 #Calculates the percent change, so we can tell if its +2% or -4%, etc. How much the stock went up in percentage

        print(f"{symbol}: ${current_price:.2f} ({percent_change:+.2f}%)") #Prints the stock's ticker, current price, and percent change in a clean, formatted way. E.g AAPL: $173.21 (+2.34%)
            
        if percent_change > 2: #Recommends buying if up 2%+
            print(" ✅ Consider Buying - positive trend")
        elif percent_change < -2: #Warns if its dropping fast
            print(" ❌ Consider Avoiding - negative trend")
        else: #Chill, suggest holding
            print(" 🤝 Hold - neutral trend")
        

        if enable_news: #Checks if news is enabled at top of code
            try: #Protects program from breaking if news API fails, internet cut outs, etc. "Dont crash, just handle it"
                news = finnhub_client.company_news(symbol, _from=three_days_ago, to=today) #Calling the API to get the company news headlines for the stock, grabs the news from the last 3 days
                news_block += f"{symbol}:\n" #Adds the stock ticker as a heading (e.g. AAPL:)
                if news:
                        for article in news[:news_limit]: #Changes the amount of news present for each ticker
                            news_block += f" - {article['headline']}\n"  #Adds a news headline as a bullet point under the ticker   
                else:
                        news_block += " - No recent news found.\n"
                news_block += "-" * 40 + "\n" #Adds a horizontal divider line (40 dashes)
            except Exception as e: #If all else fails print error message, hitting rate limits, etc
                news_block += f" Could not fetch news for {symbol}: {e}\n" #Add an error message if news couldn't be fetched
                news_block += "-" * 40 + "\n" #Adds a horizontal divider line (40 dashes)

        print("-" * 40)  # One final separator after all stocks

    if enable_news:
        print("=" * 40)
        print("📰 NEWS HEADLINES 📰")
        print("=" * 40)
        print(news_block)

    print("\n Waiting for refresh...\n")
    time.sleep(10)




          
  



          
          
