# coding: utf-8
from typing import Dict, List

from pandas import DataFrame
import yfinance as yf

from ...enums.finance import Ticker
from ...interface.pullers.financial_puller  import FinancialPuller
from ...utils.finance import TICKERS


class YFinanceFinancialPuller(FinancialPuller):

    def _clean_daily_dataframe(self, dataframe: DataFrame) -> DataFrame:
        """ Cleans the dataframe to ensure that the index is the date and the columns are the following:

            ['open', 'high', 'low', 'close', 'adj_close', 'volume']

            Args:
                dataframe (DataFrame): Dataframe to clean
            
            Returns:
                Cleaned dataframe
        """
        dataframe = dataframe.rename_axis('date')
        dataframe.columns = self.DAILY_COLUMNS
        dataframe.dropna(axis=0, how='any', inplace=True)

        return dataframe

    def get_daily_for_ticker(self, ticker: Ticker) -> DataFrame:
        """ Gets historical data from the corresponding ticker

            Args:
                ticker (Ticker): Ticker of the company to retrieve historical data from
            
            Returns
                Dataframe for the corresponding Ticker with the following index and columns
                index: 'date'
                columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """
        ticker_value = TICKERS.get(ticker)

        data = DataFrame()
        if ticker_value is not None:
            data = yf.download(tickers=ticker_value, period='max')

        data = self._clean_daily_dataframe(data)

        return data.rename_axis()

    def get_daily_for_tickers(self, tickers: List[Ticker]) -> Dict[Ticker, DataFrame]:
        """ Gets historical data from the corresponding tickers

            Args:
                tickers (List[Ticker]): List of tickers for the companies to retrieve historical data
            
            Returns
                Dictionary of dataframes for the corresponding Tickers with the following index and columns
                index: 'date'
                columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """
        data = {}

        for ticker in tickers:
            ticker_value = TICKERS.get(ticker)
            if ticker_value is not None:
                dataframe = yf.download(tickers=ticker_value, period='max')
                data[ticker] = self._clean_daily_dataframe(dataframe)

        return data
