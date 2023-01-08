# coding: utf-8
from pandas import DataFrame

from src.enums.finance import Ticker
from src.pullers.finance.yfinance_financial_puller import YFinanceFinancialPuller
from src.utils.finance import TICKERS


puller = YFinanceFinancialPuller()

finance_data = puller.get_daily_for_tickers(tickers=[Ticker.APPLE, Ticker.MICROSOFT, Ticker.NETES])


data = DataFrame({
    TICKERS[Ticker.APPLE]: finance_data[Ticker.APPLE]['close'],
    TICKERS[Ticker.MICROSOFT]: finance_data[Ticker.MICROSOFT]['close'],
    TICKERS[Ticker.NETES]: finance_data[Ticker.NETES]['close'],
})

data.dropna(axis=0, how='any', inplace=True)
