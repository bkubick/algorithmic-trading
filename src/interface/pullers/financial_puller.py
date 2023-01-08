# coding: utf-8
from abc import ABC, abstractmethod
from typing import Dict, List

from pandas import DataFrame

from src.enums.finance import Ticker


class FinancialPuller(ABC):

    DAILY_COLUMNS: List[str] = ['open', 'high', 'low', 'close', 'adj_close', 'volume']

    @abstractmethod
    def get_daily_for_ticker(self, ticker: Ticker) -> DataFrame:
        """ Gets historical data from the corresponding ticker
        
        Args:
            ticker (Ticker): Ticker of the company to retrieve historical data from
        
        Returns
            Dataframe for the corresponding Ticker with the following index and columns
            index: 'date'
            columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """

    @abstractmethod
    def get_daily_for_tickers(self, tickers: List[Ticker]) -> Dict[Ticker, DataFrame]:
        """ Gets historical data from the corresponding tickers
        
        Args:
            tickers (List[Ticker]): List of tickers for the companies to retrieve historical data
        
        Returns
            Dictionary of dataframes for the corresponding Tickers with the following index and columns
            index: 'date'
            columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """
