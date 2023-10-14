# coding: utf-8
from decimal import Decimal
from typing import Dict, Union

from numpy import float64

from ..enums.finance import Ticker


Numeric = Union[Decimal, int, float, float64]


# Ticker enum to the ticker value
TICKERS: Dict[Ticker, str] = {
    Ticker.APPLE: 'AAPL',
    Ticker.MICROSOFT: 'MSFT',
    Ticker.NETES: 'NTES',
    Ticker.GOOGLE: 'GOOG',
    Ticker.AMAZON: 'AMZN',
    Ticker.FACEBOOK: 'FB',
}


def numeric_from_str(value: str, numeric_type: Numeric = int) -> Numeric:
    """ Filters the str value with the return type as the numeric type desired
    
    Args:
        value (str): String value that is desired to be converted to a Numeric
        numeric_type (Numeric): Desired numeric type to convert the str value to
    
    Returns
        Converted value
    """
    filtered_value = value.replace(',', '')
    
    return numeric_type(filtered_value)
