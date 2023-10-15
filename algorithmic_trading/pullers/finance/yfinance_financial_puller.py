# coding: utf-8
import datetime as dt
from typing import Dict, List, Optional

from pandas import DataFrame
import yfinance as yf

from ...enums.finance import Ticker
from ...interface.pullers.financial_puller  import FinancialPuller
from ... import utils


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

    def get_daily_for_tickers(self,
                              tickers: List[Ticker],
                              start: Optional[utils.types.DateType] = None,
                              end: Optional[utils.types.DateType] = None) -> Dict[Ticker, DataFrame]:
        """ Gets historical data from the corresponding tickers

            Args:
                tickers (List[Ticker]): List of tickers for the companies to retrieve historical data
                start (Optional[DateType]): Start date (inclusive) for the historical data
                end (Optional[DateType]): End date (inclusive) for the historical data

            Returns
                Dictionary of dataframes for the corresponding Tickers with the following index and columns
                index: 'date'
                columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """
        start = start or dt.datetime.today() - dt.timedelta(3650)
        end = end or dt.datetime.today()
        data = {}

        for ticker in tickers:
            ticker_value = ticker.value
            if ticker_value is not None:
                dataframe: DataFrame = yf.download(tickers=ticker_value, interval='1d', start=start, end=end)
                data[ticker] = self._clean_daily_dataframe(dataframe)

        return data

    def get_monthly_for_tickers(self,
                                tickers: List[Ticker],
                                start: Optional[utils.types.DateType] = None,
                                end: Optional[utils.types.DateType] = None) -> Dict[Ticker, DataFrame]:
        """ Gets historical data from the corresponding tickers

            Args:
                tickers (List[Ticker]): List of tickers for the companies to retrieve historical data
                start (Optional[DateType]): Start date (inclusive) for the historical data
                end (Optional[DateType]): End date (inclusive) for the historical data
            
            Returns
                Dictionary of dataframes for the corresponding Tickers with the following index and columns
                index: 'date'
                columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """
        start = start or dt.datetime.today() - dt.timedelta(3650)
        end = end or dt.datetime.today()
        data = {}

        for ticker in tickers:
            ticker_value = ticker.value
            if ticker_value is not None:
                dataframe = yf.download(tickers=ticker_value, interval='1mo', start=start, end=end)
                data[ticker] = self._clean_daily_dataframe(dataframe)

        return data
