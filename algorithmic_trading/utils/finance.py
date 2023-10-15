# coding: utf-8

from __future__ import annotations

import typing

import pandas as pd

from . import types


TRADING_DAYS_PER_YEAR: int = 252
TRADING_MONTHS_PER_YEAR: int = 12


def numeric_from_str(value: str, numeric_type: types.NumericType = int) -> types.NumericType:
    """ Filters the str value with the return type as the numeric type desired
    
    Args:
        value (str): String value that is desired to be converted to a Numeric
        numeric_type (Numeric): Desired numeric type to convert the str value to
    
    Returns
        Converted value
    """
    filtered_value = value.replace(',', '')
    
    return numeric_type(filtered_value)


def get_return_from_adj_close(dataframe: pd.DataFrame,
                              fill_na: types.NumericType = 0) -> pd.DataFrame:
    """ Gets the return from the adjusted close price of the dataframe.

        Args:
            dataframe (pd.DataFrame): dataframe of stock prices
                Columns: [..., 'adj_close']
            fill_na (NumericType): Fill NA values with this value. Default is 0.

        Returns:
            (DataFrame) DataFrame with `return` column added
                Return Columns: [..., 'adj_close', 'return']
    """
    dataframe_copy = dataframe.copy()
    dataframe_copy['return'] = dataframe_copy['adj_close'].pct_change()
    dataframe_copy.fillna(fill_na, inplace=True)

    return dataframe_copy


# TODO: This ticker changes over time, so I need to figure out how to handle this
def get_dow_jones_tickers() -> typing.List[str]:
    """ Returns the list of tickers for the Dow Jones Industrial Average

        Returns:
            (List[str]) List of tickers for the Dow Jones Industrial Average
    """
    return [
        'MMM',
        'AXP',
        'AMGN',
        'AAPL',
        'BA',
        'CAT',
        'CVX',
        'CSCO',
        'KO',
        'DIS',
        'DOW',
        'GS',
        'HD',
        'HON',
        'INTC',
        'IBM',
        'JNJ',
        'JPM',
        'MCD',
        'MRK',
        'MSFT',
        'NKE',
        'PG',
        'CRM',
        'TRV',
        'UNH',
        'VZ',
        'V',
        'WBA',
        'WMT',
    ]
