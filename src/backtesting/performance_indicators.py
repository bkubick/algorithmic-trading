# coding: utf-8
from pandas import DataFrame, Series
import numpy as np


def cagr(df: DataFrame) -> float:
    """ Calculates the Compound Annual Growth Rate (CAGR) for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']

        Returns:
            Calculated CAGR value for the df.
    """
    new_df = df.copy()

    # TODO: Need to automatically calculate 'n' based of the interval period of df stock prices
    # 252 = trading days in a year
    # Because this is daily, n does not change
    n = len(df) / 252

    new_df['return'] = new_df['adj_close'].pct_change()
    new_df['cum_return'] = (1 + new_df['return']).cumprod()
    
    cagr = (new_df['cum_return'][-1])**(1/n) - 1
    return cagr


def volatility(df: DataFrame) -> float:
    """ Calculates the volatility for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']

        Returns:
            Calculated volatility value for the df.
    """
    new_df = df.copy()

    new_df['return'] = new_df['adj_close'].pct_change()
    volatility = new_df['return'].std() * np.sqrt(252)
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


def sortino_ratio(df: DataFrame, rf: float = 0.03) -> float:
    """ Calculates the Sortino Ratio for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']
            rf (float):

        Returns:
            Calculated ratio value for the df.
    """
    new_df = df.copy()

    new_df['return'] = new_df['adj_close'].pct_change()
    neg_return = np.where(new_df['return'] > 0, 0, df['return'])
    neg_volatility = Series(neg_return[neg_return != 0]).std() * np.sqrt(252)

    ratio = (cagr(new_df) - rf) / neg_volatility

    return ratio


def maximum_drawdown(df: DataFrame):
    """ Calculates the Maximum Drawdown for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']

        Returns:
            Calculated Max Drawdown value for the df.
    """
    new_df = df.copy()

    new_df['return'] = new_df['adj_close'].pct_change()
    new_df['cum_return'] = (1 + new_df['adj_close']).cumprod()
    new_df['cum_roll_max'] = new_df['cum_return'].cummax()
    new_df['drawdown'] = new_df['cum_roll_max'] - new_df['cum_return']

    drawdown = (new_df['drawdown'] / new_df['cum_roll_max']).max()

    return drawdown


def calmar_ratio(df: DataFrame):
    """ Calculates the Calmar Ratio for the given dataframe.

        Args:
            df (DataFrame): Columns - ['adj_close']

        Returns:
            Calculated ratio value for the df.
    """
    new_df = df.copy()

    return cagr(new_df) / maximum_drawdown(new_df)
