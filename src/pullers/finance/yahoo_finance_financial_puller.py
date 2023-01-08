# coding: utf-8
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from numpy import float64
from pandas import DataFrame

from src.enums.finance import Ticker
from src.interface.pullers.financial_puller import FinancialPuller
from src.utils.finance import numeric_from_str, TICKERS


class YahooFinancePage(Enum):
    HISTORICAL_DATA: str = 'historical_data'


class YahooFinanceFinancialPuller(FinancialPuller):

    DATE_FORMAT: str = '%b %d, %Y'
    PAGE_URLS: Dict[YahooFinancePage, str] = {
        YahooFinancePage.HISTORICAL_DATA: 'https://finance.yahoo.com/quote/<ticker>/history?p=<ticker>'
    }

    def __init__(self) -> None:
        headers = {'User-Agent': 'Chrome/107.0.5304.110'}
        self._request = requests.Session()
        self._request.headers.update(headers)
        self._response_cache: Dict[str, requests.Response] = {}

    def _get_response(self, url: str) -> Optional[requests.Response]:
        """ Gets the response for the corresponding url and caches the response if the response is
            a valid 200.

            Args:
                url (str): Url to request a response from
            
            Returns:
                200 Response for the corresponding url, or None
        """
        if self._response_cache.get(url):
            response = self._response_cache.get(url)
        else:
            response = self._request.get(url=url)

            if response.status_code == 200:
                self._response_cache[url] = response
            else:
                return None

        return response

    def _get_response_from_ticker(self, ticker: Ticker, page: YahooFinancePage) -> Optional[requests.Response]:
        """ Gets the response for the corresponding Ticker and page

            Args:
                ticker (Ticker): Ticker of the company to retrieve data from
                page (YahooFinancePage): Corresponding page that the data is being retrieved from
            
            Returns:
                200 Response for the corresponding page, or None
        """
        ticker_value = TICKERS.get(ticker)
        if ticker_value is None:
            return None

        url = self.PAGE_URLS[page].replace('<ticker>', ticker_value)
        return self._get_response(url=url)

    def clear_cache(self):
        """ Clears the cached responses """
        self._response_cache: Dict[str, requests.Response] = {}

    def get_daily_for_ticker(self, ticker: Ticker) -> DataFrame:
        # TODO Currently, YahooFinance dynamically loads rows, but by default, has 100 on the page.
        # I need to make this scrape by 1-6 month intervals in order to get the remaining data
        """ Gets historical data from the corresponding ticker

            Args:
                ticker (Ticker): Ticker of the company to retrieve historical data from
            
            Returns
                Dataframe for the corresponding Ticker with the following index and columns
                index: 'date'
                columns: ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        """
        response = self._get_response_from_ticker(ticker=ticker, page=YahooFinancePage.HISTORICAL_DATA)

        if response is None:
            return []

        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')

        table: Tag = soup.find_all('table', {'data-test': 'historical-prices'})[0]
        table_body: Tag = table.find_all('tbody')[0]
        rows: List[Tag] = table_body.find_all('tr')

        all_data = defaultdict(list)
        for row in rows:
            columns: List[Tag] = row.find_all('td')
            if len(columns) == 7:
                all_data['date'].append(datetime.strptime(columns[0].get_text(), self.DATE_FORMAT).date())
                all_data['open'].append(numeric_from_str(columns[1].get_text(), numeric_type=float64))
                all_data['high'].append(numeric_from_str(columns[2].get_text(), numeric_type=float64))
                all_data['low'].append(numeric_from_str(columns[3].get_text(), numeric_type=float64))
                all_data['close'].append(numeric_from_str(columns[4].get_text(), numeric_type=float64))
                all_data['adj_close'].append(numeric_from_str(columns[5].get_text(), numeric_type=float64))
                all_data['volume'].append(numeric_from_str(columns[6].get_text(), numeric_type=int))

        data = DataFrame(all_data)
        data = data.set_index('date')
        data.dropna(axis=0, how='any', inplace=True)
        return data

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
            data[ticker] = self.get_daily_for_ticker(ticker=ticker)
        
        return data
