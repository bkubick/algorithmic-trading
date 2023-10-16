# coding: utf-8
from __future__ import annotations

import typing

from pandas import DataFrame, Series
import numpy as np

from ..pullers.finance.financial_puller import FinancialPuller
from .. import utils


_PERIOD_TO_NUM_PERIODS = {
    'day': utils.finance.TRADING_DAYS_PER_YEAR,
    'month': utils.finance.TRADING_MONTHS_PER_YEAR,
}


def cagr(df: DataFrame, period: typing.Optional[str] = None) -> float:
    """ Calculates the Compound Annual Growth Rate (CAGR) for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']
            period (Optional[str]): Period of the stock prices. Default is 'day'.

        Returns:
            Calculated CAGR value for the df.
    """
    new_df = df.copy()

    period = period or 'day'
    num_periods = _PERIOD_TO_NUM_PERIODS.get(period)
    if num_periods is None:
        raise ValueError(f'Invalid period: {period}')

    n = len(df) / num_periods

    df_columns = set(new_df.columns)
    if 'return' not in df_columns:
        new_df = utils.finance.get_return_from_adj_close(new_df)

    new_df['cum_return'] = (1 + new_df['return']).cumprod()

    cagr = (new_df['cum_return'][-1])**(1/n) - 1
    return cagr


def volatility(df: DataFrame, period: typing.Optional[str] = None) -> float:
    """ Calculates the volatility for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']
            period (Optional[str]): Period of the stock prices. Default is 'day'.

        Returns:
            Calculated volatility value for the df.
    """
    new_df = df.copy()

    period = period or 'day'
    num_periods = _PERIOD_TO_NUM_PERIODS.get(period)
    if num_periods is None:
        raise ValueError(f'Invalid period: {period}')

    df_columns = set(new_df.columns)
    if 'return' not in df_columns:
        new_df = utils.finance.get_return_from_adj_close(new_df)

    volatility = new_df['return'].std() * np.sqrt(num_periods)
    return volatility


def sharpe_ratio(df: DataFrame, rf: float = 0.03) -> float:
    """ Calculates the Sharpe Ratio for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']

        Returns:
            Calculated ratio value for the df.
    """
    new_df = df.copy()

    ratio = (cagr(new_df) - rf) / volatility(df)

    return ratio


def sortino_ratio(df: DataFrame, rf: float = 0.03, period: typing.Optional[str] = None) -> float:
    """ Calculates the Sortino Ratio for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']
            rf (float):
            period (Optional[str]): Period of the stock prices. Default is 'day'.

        Returns:
            Calculated ratio value for the df.
    """
    new_df = df.copy()

    period = period or 'day'
    num_periods = _PERIOD_TO_NUM_PERIODS.get(period)
    if num_periods is None:
        raise ValueError(f'Invalid period: {period}')

    df_columns = set(new_df.columns)
    if 'return' not in df_columns:
        new_df = utils.finance.get_return_from_adj_close(new_df)

    neg_return = np.where(new_df['return'] > 0, 0, new_df['return'])
    neg_volatility = Series(neg_return[neg_return != 0]).std() * np.sqrt(num_periods)

    ratio = (cagr(new_df) - rf) / neg_volatility

    return ratio


def maximum_drawdown(df: DataFrame) -> float:
    """ Calculates the Maximum Drawdown for the given dataframe.

        Args:
            df (DataFrame): Columns - ['return'] or ['adj_close']

        Returns:
            Calculated Max Drawdown value for the df.
    """
    new_df = df.copy()

    df_columns = set(new_df.columns)
    if 'return' not in df_columns:
        new_df = utils.finance.get_return_from_adj_close(new_df)

    new_df['cum_return'] = (1 + new_df['return']).cumprod()
    new_df['cum_roll_max'] = new_df['cum_return'].cummax()
    new_df['drawdown'] = new_df['cum_roll_max'] - new_df['cum_return']

    drawdown = (new_df['drawdown'] / new_df['cum_roll_max']).max()

    return drawdown


def calmar_ratio(df: DataFrame) -> float:
    """ Calculates the Calmar Ratio for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']

        Returns:
            Calculated ratio value for the df.
    """
    new_df = df.copy()

    return cagr(new_df) / maximum_drawdown(new_df)


def average_true_range(df: DataFrame, periods: int = 14) -> float:
    """ Calculates the Average True Range (ATR) for the given position information.
    
        Args:
            df (DataFrame): Columns - ['high', 'low', 'close']
            periods (int): Number of periods to calculate the ATR for. Default is 14.
        
        Returns:
            (float) Calculated ATR value for the df.
    """
    data = df.copy()

    # Ensure that the DataFrame is sorted by date
    data = data.sort_values(by='date').reset_index(drop=True)

    # Calculate True Range (TR) for the DataFrame
    data['h-l'] = data['high'] - data['low']
    data['h-yc'] = abs(data['high'] - data['close'].shift(1))
    data['l-yc'] = abs(data['low'] - data['close'].shift(1))
    data['tr'] = data[['h-l', 'h-yc', 'l-yc']].max(axis=1)

    # Calculate the first ATR
    first_atr = data['tr'][:periods].mean()

    # Calculate subsequent ATR values
    atr_values = [first_atr]
    for i in range(periods, len(data)):
        tr = data['tr'].iloc[i]
        atr = (atr_values[-1] * (periods - 1) + tr) / periods
        atr_values.append(atr)

    return atr_values[-1]
