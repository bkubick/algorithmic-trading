# coding: utf-8
from abc import ABC, abstractmethod
import datetime as dt
from typing import Dict, List, Optional, Union

from pandas import DataFrame

from ...enums.finance import Ticker
from ... import utils


class FinancialPuller(ABC):

    DAILY_COLUMNS: List[str] = ['open', 'high', 'low', 'close', 'adj_close', 'volume']

    @abstractmethod
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

    @abstractmethod
    def get_monthly_for_tickers(self,
                                tickers: List[Ticker],
                                start: Optional[utils.types.DateType] = None,
                                end: Optional[utils.types.DateType] = None) -> Dict[Ticker, DataFrame]:
        """ Gets monthly historical data from the corresponding tickers

            Args:
                tickers (List[Ticker]): List of tickers for the companies to retrieve historical data
                start (Optional[DateType]): Start date (inclusive) for the historical data
                end (Optional[DateType]): End date (inclusive) for the historical data

            Returns
                Dictionary of dataframes for the corresponding Tickers with the following index and columns
                index: 'date'
                columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """
