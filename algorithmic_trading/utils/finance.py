# coding: utf-8
from decimal import Decimal
import typing

import pandas as pd

from . import types
from ..enums.finance import Ticker


TRADING_DAYS_PER_YEAR: int = 252
TRADING_MONTHS_PER_YEAR: int = 12

DOW_JONES_CONSTITUENT_TICKERS: typing.List[Ticker] = [
    Ticker.THREE_M,
    Ticker.AMERICAN_EXPRESS,
    Ticker.AMGEN,
    Ticker.APPLE,
    Ticker.BOEING,
    Ticker.CATERPILLAR,
    Ticker.CHEVRON,
    Ticker.CISCO,
    Ticker.COCACOLA,
    Ticker.DISNEY,
    Ticker.DOW_INC,
    Ticker.GOLDMAN_SACHS,
    Ticker.HOME_DEPOT,
    Ticker.HONEYWELL,
    Ticker.INTEL,
    Ticker.IBM,
    Ticker.JOHNSON_JOHNSON,
    Ticker.JPMORGAN,
    Ticker.MCDONALDS,
    Ticker.MERCK,
    Ticker.MICROSOFT,
    Ticker.NIKE,
    Ticker.PROCTER_GAMBLE,
    Ticker.SALESFORCE,
    Ticker.TRAVELERS,
    Ticker.UNITED_HEALTH,
    Ticker.VERIZON,
    Ticker.VISA,
    Ticker.WALGREENS,
    Ticker.WALMART,
]


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


def get_monthly_return_dataframe(monthly_dataframe: pd.DataFrame,
                                 fill_na: typing.Optional[types.NumericType] = None) -> pd.DataFrame:
    """ Gets the monthly return dataframe from the monthly dataframe

        Args:
            monthly_dataframe (pd.DataFrame): Monthly dataframe
                Columns: [..., 'adj_close']
            fill_na (Optional[NumericType]): Fill NA values with this value

        Returns:
            (DataFrame) DataFrame with monthly return column added
                Return Columns: [..., 'adj_close', 'monthly_return']
    """
    monthly_dataframe_copy = monthly_dataframe.copy()
    monthly_dataframe_copy['monthly_return'] = monthly_dataframe_copy['adj_close'].pct_change()

    if fill_na is not None:
        monthly_dataframe_copy.fillna(fill_na, inplace=True)

    return monthly_dataframe_copy
