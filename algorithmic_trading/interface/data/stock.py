# coding: utf-8

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Optional

from pandas import DataFrame


GenericAlias = type(List[str])


@dataclass
class DailyStockPrice:
    price_date: Optional[date]
    open_value: Optional[Decimal]
    close_value: Optional[Decimal]
    low: Optional[Decimal]
    high: Optional[Decimal]
    adj_close: Optional[Decimal]
    volume: Optional[int]


class StockDataFrame(DataFrame):
    # TODO: Need to get this working to get a typehintable dataframe to ensure each object/function understands
    # the columns associated with the dataframe.

    __class_getitem__ = classmethod(GenericAlias)
