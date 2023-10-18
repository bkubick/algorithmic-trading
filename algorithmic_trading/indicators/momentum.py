# coding: utf-8
from pandas import DataFrame, Series
import numpy as np


# TODO: Look into the library ta-lib (Technical analysis library) https://github.com/mrjbq7/ta-lib
# Look into the Pattern Recognition of ta-lib
# Additional notes on pattern recognition are on https://thepatternsite.com/
# Avoid using this library, but good source to build my own library

# TODO: Replace the DataFrame typehint with StockDataFrame once I get it made
def macd(df: DataFrame, a: int = 12, b: int = 26, c: int = 9) -> DataFrame:
    """ Moving Average Convergence Divergence
        https://www.tradingview.com/scripts/macd/?solution=43000502344

        Args:
            df (DataFrame): Columns - ['adj_close']
        
        Returns:
            DataFrame: Columns - ['ma_fast', 'ma_slow', 'macd', 'signal']
    """
    new_df = df.copy()

    new_df['ma_fast'] = new_df['adj_close'].ewm(span=a, min_periods=a).mean()
    new_df['ma_slow'] = new_df['adj_close'].ewm(span=b, min_periods=b).mean()
    new_df['macd'] = new_df['ma_fast'] - new_df['ma_slow']
    new_df['signal'] = new_df['macd'].ewm(span=c, min_periods=c).mean()

    columns = ['ma_fast', 'ma_slow', 'macd', 'signal']
    return new_df[columns]


def _rma(df: Series, n: int = 14) -> Series:
    """ Moving average used in RSI. It is the exponentially weighted moving average
        with alpha = 1 / length.

        https://www.tradingview.com/pine-script-reference/v5/#fun_ta%7Bdot%7Drma
    """
    return df.ewm(alpha=1/n, min_periods=n).mean()


# TODO: Replace the DataFrame typehint with StockDataFrame once I get it made
def rsi(df: DataFrame, n: int = 14) -> DataFrame:
    """ Relative Strength Index

        https://www.tradingview.com/pine-script-reference/v5/#fun_ta%7Bdot%7Drsi

        Args:
            df (DataFrame): Columns - ['adj_close']
        
        Returns:
            DataFrame: Columns - ['gain', 'loss', 'avg_gain', 'avg_loss', 'relative_strength', 'rsi']
    """
    new_df = df.copy()

    new_df['change'] = new_df['adj_close'] - new_df['adj_close'].shift(1)
    new_df['gain'] = np.where(new_df['change'] >= 0, new_df['change'], 0)
    new_df['loss'] = np.where(new_df['change'] < 0, -1 * new_df['change'], 0)
    new_df['avg_gain'] = _rma(new_df['gain'], n)
    new_df['avg_loss'] = _rma(new_df['loss'], n)
    new_df['relative_strength'] = new_df['avg_gain'] / new_df['avg_loss']
    new_df['rsi'] = 100 - (100 / (1 + new_df['relative_strength']))

    columns = ['gain', 'loss', 'avg_gain', 'avg_loss', 'relative_strength', 'rsi']
    return new_df[columns]


# TODO: Replace the DataFrame typehint with StockDataFrame once I get it made
def average_true_range(df: DataFrame, n: int = 14) -> Series:
    """ Average True Range
        https://www.tradingview.com/scripts/averagetruerange/?solution=43000501823

        Args:
            df (DataFrame): Columns - ['high', 'low', 'adj_close']
        
        Returns:
            Series: ATR values
    """
    new_df = df.copy()

    new_df['high_minus_low'] = new_df['high'] - new_df['low']
    new_df['high_minus_previous_close'] = new_df['high'] - new_df['adj_close'].shift(1)
    new_df['low_minus_previous_close'] = new_df['low'] - new_df['adj_close'].shift(1)

    true_range_columns = ['high_minus_low', 'high_minus_previous_close', 'low_minus_previous_close']
    new_df['true_range'] = new_df[true_range_columns].max(axis=1, skipna=False)
    new_df['atr'] = new_df['true_range'].ewm(span=n, min_periods=n).mean()

    return new_df['atr']


# TODO: Replace the DataFrame typehint with StockDataFrame once I get it made
def bbands(df: DataFrame, n: int = 14) -> DataFrame:
    """ Bollinger Bands

        Args:
            df (DataFrame): Columns - ['adj_close']
        
        Returns:
            DataFrame: Columns - ['middle_band', 'upper_band', 'lower_band', 'bollinger_band_width']
    """
    new_df = df.copy()

    new_df['middle_band'] = new_df['adj_close'].rolling(n).mean()
    new_df['upper_band'] = new_df['middle_band'] + 2 * new_df['adj_close'].rolling(n).std(ddof=0)
    new_df['lower_band'] = new_df['middle_band'] - 2 * new_df['adj_close'].rolling(n).std(ddof=0)
    new_df['bollinger_band_width'] = new_df['upper_band'] - new_df['lower_band']

    columns = ['middle_band', 'upper_band', 'lower_band', 'bollinger_band_width']
    return new_df[columns]


# TODO: Replace the DataFrame typehint with StockDataFrame once I get it made
def adx(df: DataFrame, n: int = 20) -> DataFrame:
    """ Average Directional Index

        https://www.tradingview.com/scripts/directionalmovement/?solution=43000502250
        https://www.tradingview.com/pine-script-reference/v5/#fun_ta%7Bdot%7Ddmi

        Args:
            df (DataFrame): Columns - ['high', 'low', 'adj_close']
        
        Returns:
            DataFrame: Columns - [
                'avg_true_range', 'up_move', 'down_move', 'plus_down_move', 'minus_down_move',
                'plus_directional_indicator', 'minus_directional_indicator', 'adx',
            ]
    """
    new_df = df.copy()

    new_df['avg_true_range'] = atr(new_df, n)
    new_df['up_move'] = new_df['high'] - new_df['high'].shift(1)
    new_df['down_move'] = new_df['low'].shift(1) - new_df['low']
    new_df['plus_down_move'] = np.where(((new_df['up_move'] >= new_df['down_move']) & (new_df['up_move'] > 0)), new_df['up_move'], 0)
    new_df['minus_down_move'] = np.where(((new_df['down_move'] >= new_df['up_move']) & (new_df['down_move'] > 0)), new_df['down_move'], 0)
    new_df['plus_directional_indicator'] = 100 * (new_df['plus_down_move'] / new_df['avg_true_range']).ewm(span=n, min_periods=n).mean()
    new_df['minus_directional_indicator'] = 100 * (new_df['minus_down_move'] / new_df['avg_true_range']).ewm(span=n, min_periods=n).mean()

    new_df['adx'] = 100 * abs(new_df['plus_directional_indicator'] - new_df['minus_directional_indicator']) / (new_df['plus_directional_indicator'] + new_df['minus_directional_indicator']).ewm(span=n, min_periods=n).mean()

    columns = ['avg_true_range', 'up_move', 'down_move', 'plus_down_move', 'minus_down_move', 'plus_directional_indicator', 'minus_directional_indicator', 'adx']
    return new_df[columns]


def renko(df: DataFrame, n: int = 20) -> DataFrame:
    """ TODO: Need to implement this one.

        The course uses the library, stocktrends

        Args:
            df (DataFrame): Columns - ['open', 'high', 'low', 'close', 'adj_close', 'volume']
    """
    raise NotImplementedError('This method has not been implemented yet')
