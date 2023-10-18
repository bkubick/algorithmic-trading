# coding: utf-8

from __future__ import annotations

from decimal import Decimal
import typing

import matplotlib.pyplot as plt
import pandas as pd

from ..indicators import momentum


def plot_portfolio_returns(portfolio_returns: typing.List[Decimal], figsize: typing.Tuple[int, int] = (16, 9)) -> None:
    """ Plots the portfolio returns.

        Args:
            portfolio_returns (typing.List[Decimal]): The portfolio returns.
    """
    plt.figure(figsize=figsize)
    plt.plot(portfolio_returns)
    plt.title('Portfolio Returns')
    plt.xlabel('Date')
    plt.ylabel('Returns')


def plot_portfolio_returns_vs_benchmark(portfolio_returns: typing.List[Decimal],
                                        benchmark_returns: typing.List[Decimal],
                                        figsize: typing.Tuple[int, int] = (16, 9)) -> None:
    """ Plots the portfolio returns vs the benchmark returns.

        Args:
            portfolio_returns (typing.List[Decimal]): The portfolio returns.
            benchmark_returns (typing.List[Decimal]): The benchmark returns.
    """
    plt.figure(figsize=figsize)
    plt.plot(portfolio_returns, label='Portfolio Returns')
    plt.plot(benchmark_returns, label='Benchmark Returns')
    plt.title('Portfolio Returns vs Benchmark Returns')
    plt.xlabel('Date')
    plt.ylabel('Returns')
    plt.legend()


def plot_position_details_from_dataframe(position_df: pd.DataFrame,
                                         start: typing.Optional[int] = None,
                                         end: typing.Optional[int] = None,
                                         figsize: typing.Tuple[int, int] = (12, 14)) -> None:
    """ Plots the position details from the dataframe.

        Args:
            position_df (pd.DataFrame): The position dataframe.
            start (Optional[int]): Start index to plot. Default is None.
            end (Optional[int]): End index to plot. Default is None.
            figsize (Optional[Tuple[int, int]]): Figure size. Default is (12, 14).

        Returns:
            Plots the position details from the dataframe.
    """
    fig, axs = plt.subplots(len(position_df.columns), figsize=figsize, sharex=True)

    fig.suptitle('Position Details')
    fig.subplots_adjust(top=0.95)
    x = position_df.index.to_numpy()

    for index, feature in enumerate(position_df):
        title = feature.upper().replace('_', ' ')
        axs[index].plot(x[start:end], position_df[feature][start:end])
        axs[index].set_title(title, fontsize=10)


def plot_position_macd(position_df: pd.DataFrame,
                       start: typing.Optional[int] = None,
                       end: typing.Optional[int] = None,
                       figsize: typing.Tuple[int, int] = (12, 14)) -> None:
    """ Plots the position macd details.
    
        Args:
            position_df (pd.DataFrame): The position dataframe.
                Columns - ['adj_close']
            start (Optional[int]): Start index to plot. Default is None.
            end (Optional[int]): End index to plot. Default is None.
            figsize (Optional[Tuple[int, int]]): Figure size. Default is (12, 14).

        Returns:
            Plots the position macd details.
    """
    macd_df = momentum.macd(position_df)
    fig, axs = plt.subplots(len(macd_df.columns), figsize=figsize, sharex=True)

    fig.suptitle('Position MACD Details')
    fig.subplots_adjust(top=0.95)
    x = macd_df.index.to_numpy()

    for index, feature in enumerate(macd_df):
        title = feature.upper().replace('_', ' ')
        axs[index].plot(x[start:end], macd_df[feature][start:end])
        axs[index].set_title(title, fontsize=10)


def plot_position_rsi(position_df: pd.DataFrame,
                      start: typing.Optional[int] = None,
                      end: typing.Optional[int] = None,
                      figsize: typing.Tuple[int, int] = (12, 14)) -> None:
    """ Plots the position rsi details.
    
        Args:
            position_df (pd.DataFrame): The position dataframe.
                Columns - ['adj_close']
            start (Optional[int]): Start index to plot. Default is None.
            end (Optional[int]): End index to plot. Default is None.
            figsize (Optional[Tuple[int, int]]): Figure size. Default is (12, 14).

        Returns:
            Plots the position rsi details.
    """
    rsi_df = momentum.rsi(position_df)
    fig, axs = plt.subplots(len(rsi_df.columns), figsize=figsize, sharex=True)

    fig.suptitle('Position RSI Details')
    fig.subplots_adjust(top=0.95)
    x = rsi_df.index.to_numpy()

    for index, feature in enumerate(rsi_df):
        title = feature.upper().replace('_', ' ')
        axs[index].plot(x[start:end], rsi_df[feature][start:end])
        axs[index].set_title(title, fontsize=10)
