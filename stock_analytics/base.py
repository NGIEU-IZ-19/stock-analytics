"""
stock_analytics base module.

This is the principal module of the stock_analytics project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""

import datetime
from datetime import datetime as dt

import pandas as pd
import yfinance as yf
import numpy



class stock_analytics:

    def __init__(self, instrument, year=dt.utcnow().strftime("%Y"), month=dt.utcnow().strftime("%m"),
                 day=dt.utcnow().strftime("%d"), timedelta=1, fullPeriod=False, period='5y', interval='1d'):
        """
        A class that uses the yfinance api and lets you plot indicators of a stock such as:
            - History data
            - Simple moving averages (SMA)
            - Volatility
            - Volumes
        """

        self.df_earnings = self.get_earnings
        self.instrument = instrument
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.start = datetime.date(self.year, self.month, self.day)
        self.end = self.start + datetime.timedelta(days=timedelta)

        self.fullPeriod = fullPeriod
        self.period = period
        self.interval = interval
        self.df_history = self.get_stock_history

    @property
    def get_stock_history(self):
        """
        Method for downloading data from Yahoo Finance returns:
            - Dataframe with historical paper data
        """
        df = yf.Ticker(self.instrument)

        if self.fullPeriod:
            df = df.history(period=self.period, interval=self.interval)
        else:
            df = df.history(interval='1m', start=str(self.start), end=str(self.end))
        return df

    def get_sma_50(self, period=50):
        """
        The 50-day simple moving average is a trend line that shows the average of 50 days of closing prices for a
        stock, plotted over time.

        Method returns a dataframe with 50 days average value of money
        """

        self.df_history['SMA50'] = self.df_history['Close'].rolling(window=period).mean()

        return self.df_history['SMA50']

    def get_sma_200(self, period=200):
        """
        The 200-day simple moving average is a trend line that shows the average of 50 days of closing prices for a
        stock, plotted over time.

        Method returns a dataframe with 50 days average value of money
        """

        self.df_history['SMA200'] = self.df_history['Close'].rolling(window=period).mean()

        return self.df_history['SMA200']

    def volatility(self):
        """
        Volatility is a measurement of the variation of prices over time.
    
        Method returns:
            -   Volatility (annualized standard deviation) numerical value, in percent
            -   Daily log return of the Close price
        """
        self.df_history['Log returns'] = numpy.log(self.df_history['Close']/self.df_history['Close'].shift())
        volatility_year = self.df_history['Log returns'].std()*252**.5
        volatility_percent = str(round(volatility_year, 4) * 100)

        return volatility_year, volatility_percent, self.df_history['Log returns']

    def volume(self):
        """
        # Volatility is a measurement of the variation of prices over time.
        #
        # Method returns:
        #     -   Volatility (annualized standard deviation) numerical value, in percent
        #     -   Daily log return of the Close price
        """
        return self.df_history['Volume']

    def get_earnings(self):
        """
        Earnings are perhaps the single most important and most closely studied number in a company's financial
        statements. It shows a company's real profitability compared to the analyst estimates, its own historical
        performance, and the earnings of its competitors and industry peers.

        Method returns a dataframe with Earnings data.
        """

        df = yf.Ticker(self.instrument)
        self.df_earnings = df.earnings

        return self.df_self.df_earnings

    # def obv(self):
    #     """
    #     On-balance volume (OBV) is a technical trading momentum indicator that uses volume flow to predict changes in
    #     stock price. Joseph Granville first developed the OBV metric in the 1963 book Granville's New Key to Stock
    #     Market Profits.
    #
    #
    #     """
    #
    #     # Creating "Vol+-" is a temporary column where,
    #     # Vol is positive for Close > Previous Close
    #     # Vol is negative for Close < Previous Close
    #     # Zero if Close == Previous Close
    #
    #     df.loc[df["Close"] > df["Close"].shift(1), "Vol+-"] = df["Volume"]
    #     df.loc[df["Close"] < df["Close"].shift(1), "Vol+-"] = df["Volume"] * (-1)
    #     df.loc[df["Close"] == df["Close"].shift(1), "Vol+-"] = 0
    #
    #     df["OBV"] = self._indicators_df["Vol+-"].cumsum()
    #     df.drop(["Vol+-"], axis=1, inplace=True)
    #
    #     print(self.df_earnings)


if __name__ == '__main__':
    #     #Example of plotting the Apple stock
    admin = stock_analytics("AAPL", fullPeriod=True, period='1y', interval='1d')
    admin_print = pd.DataFrame(admin.df_history)
    print(admin_print.columns)
    print(admin.get_earnings())

