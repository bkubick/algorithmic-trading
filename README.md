# Algorithmic Trading

## Description

A toolbox that hosts utlities, classes, and various trading algorithms for trading stocks. This includes standard momentum and key performance indicators, as well as commonly used trading strategies as I continue to learn more on investing and develop new personalized strategies.

**IMPORTANT NOTE** This repository is for my personal discovery into algorithmic trading and is no means accurate, perfect, or contains investment advice. It is strictly a toolbox to help learn more about algorithmic trading.

**NOTE** This repository is my personalized toolbox from the Udemy Course, [Algorithmic Trading Quantitative Analysis Using Python](https://www.udemy.com/course/algorithmic-trading-quantitative-analysis-using-python/), and is still under development.

## Tech Stack
<img style="padding-right:20px;" align=left alt="Pandas" src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white"/>
<img style="padding-right:20px;" align=left alt="Matplotlib" src="https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)"/>
<img style="padding-right:20px;" alt="Numpy" src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white"/>

## Setup

I run this toolbox currently through a virtual environment and install all requirements directly through `pip install -r requirements.txt`. I have plans to set this up using a `setup.py` in the near future that way it can be installed directly through pip and this repository link, but this is a side project that I will continue to develop casually.

## Toolbox

As of now, I have not properly namespaced and exposed functionality for each module the way I want it to be layed out. For now, see below for the specific utilities this toolbox offers (I will reference how to access these once I properly expose functions at module levels).

* Key Performance Indicators
    * Compound Annual Growth Rate (CAGR)
    * Volatility
    * Sharpe Ratio
    * Sortino Ratio
    * Maximum Drawdown
    * Calmar Ratio

* Momentum Indicators
    * Moving Average Convergence/Divergence (MACD)
    * Relative Strength Index (RSI)
    * Average True Range (ATR)
    * Bollinger Bands (BBANDS)
    * Average Directional Index
    * Renko - *Not Implemented Yet*

* Strategies - *Not Implemented Yet*
    * Portfolio Rebalance
    * Renko MACD
    * Renko Obv
    * Resistance Breakout


## Additional Work

I am casually adding to this repository and making updated to make it more useful and usable. As of now, it is strictly a host for useful tools as I learn more about algorithmic trading. Additional work I have in mind with this repository is listed below:

1. Structure and setup using `setup.py`.
2. Add algorithmic strategies module that contains commonly used strategies for algorithmic trading.
3. Cleanup the `pandas` dataframe typehinting (possibly move away from pandas altogether, but TBD).
4. Modularize this better in determining which namespace should expose certain functionalities.
5. Add `Renko` momentum indicator.
