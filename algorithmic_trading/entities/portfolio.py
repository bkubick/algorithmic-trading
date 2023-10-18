# coding: utf-8

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
import typing

from ..utils import types


class TransactionType(Enum):
    """ Transaction type enum to hold the transaction type information

        Attributes:
            BUY (str): Buy transaction type
            SELL (str): Sell transaction type
    """
    BUY = 'BUY'
    SELL = 'SELL'


@dataclass
class Transaction:
    """ Transaction dataclass to hold the transaction information

        Attributes:
            ticker (types.TickerType): Ticker symbol
            shares (Decimal): Number of shares
            price (Decimal): Price
            datetime (datetime): Datetime
            transaction_type (TransactionType): Transaction type
    """
    ticker: types.TickerType
    shares: Decimal
    price: Decimal
    datetime: datetime
    transaction_type: TransactionType


@dataclass
class Position:
    """ Position dataclass to hold the position information

        Attributes:
            ticker (types.TickerType): Ticker symbol
            shares (Decimal): Number of shares
            current_price (Decimal): Current price
            current_datetime (datetime): Current datetime
    """
    ticker: types.TickerType
    shares: Decimal
    current_price: Decimal
    current_datetime: datetime

    @property
    def value(self) -> Decimal:
        """ Calculates the value of the position.

            Returns:
                (Decimal) Return value.
        """
        return self.shares * self.current_price


@dataclass
class Portfolio:
    """ Portfolio dataclass to hold the portfolio information

        Attributes:
            name (str): Name of the portfolio.
            description (Optional[str]): Description of the portfolio
            start_date (date): Start date of the portfolio
            end_date (Optional[date]): End date of the portfolio (if applicable)
            starting_cash (Decimal): Starting cash of the portfolio to invest
            available_cash (Decimal): Available cash of the portfolio to invest
            positions (List[Position]): List of positions in the portfolio
        
        Properties:
            position_value (Decimal): Position value of the portfolio
            total_value (Decimal): Total value of the portfolio
            total_return (Decimal): Total return of the portfolio
            return_percentage (Decimal): Total return percentage of the portfolio
            total_positions (int): Total number of positions in the portfolio
            position_allocations (Dict[str, Decimal]): Position allocation of the portfolio
            position_allocation_percentages (Dict[str, Decimal]): Position allocation percentage of the portfolio
    """
    name: str
    description: typing.Optional[str]
    start_date: date
    end_date: typing.Optional[date]
    starting_cash: Decimal
    available_cash: Decimal
    positions: typing.Dict[types.TickerType, Position]
    transactions: typing.Dict[types.TickerType, typing.List[Transaction]]

    def buy(self, ticker: types.TickerType,
            shares: Decimal,
            purchase_price: Decimal,
            current_price: Decimal) -> None:
        """ Buys the given number of shares for the given ticker.

            Args:
                ticker (types.TickerType): Ticker symbol to buy.
                shares (Decimal): Number of shares to buy.
                purchase_price (Decimal): Purchase price.
                current_price (Decimal): Current price.
        """
        position = self.positions.get(ticker)

        if position is None:
            position = Position(ticker=ticker,
                                shares=shares,
                                current_price=current_price,
                                current_datetime=datetime.now())

            self.positions[ticker] = position
        else:
            position.shares += shares
            position.current_price = current_price

        transaction = Transaction(ticker=ticker,
                                  shares=shares,
                                  price=purchase_price,
                                  datetime=datetime.now(),
                                  transaction_type=TransactionType.BUY)

        self._add_transaction(transaction)
        self.available_cash -= shares * position.current_price

    def sell(self, ticker: str, shares: Decimal) -> None:
        """ Sells the given number of shares for the given ticker.

            Args:
                ticker (str): Ticker symbol to sell.
                shares (Decimal): Number of shares to sell.
        """
        position = self.positions.get(ticker)

        if position is None:
            raise ValueError(f'Position for ticker {ticker} does not exist in the portfolio')

        position.shares -= shares
        self.available_cash += shares * position.current_price

        transaction = Transaction(ticker=ticker,
                                  shares=shares,
                                  price=position.current_price,
                                  datetime=datetime.now(),
                                  transaction_type=TransactionType.SELL)

        self._add_transaction(transaction)

        if position.shares == 0:
            del self.positions[ticker]

    def _add_transaction(self, transaction: Transaction) -> None:
        """ Adds the given transaction to the portfolio.
        
            Args:
                transaction (Transaction): Transaction to add.
        """
        if transaction.ticker in self.transactions:
            self.transactions[transaction.ticker].append(transaction)
        else:
            self.transactions[transaction.ticker] = [transaction]

    @property
    def position_value(self) -> Decimal:
        """ Calculates the position value of the portfolio.

            Returns:
                (Decimal) Position value.
        """
        return sum([position.current_price * position.shares for position in self.positions.values()])

    @property
    def total_value(self) -> Decimal:
        """ Calculates the total value of the portfolio.

            Returns:
                (Decimal) Total value.
        """
        return self.position_value + self.available_cash

    @property
    def total_return(self) -> Decimal:
        """ Calculates the total return for the portfolio.

            Returns:
                (Decimal) Portfolio return.
        """
        return self.total_value - self.starting_cash

    @property
    def return_percentage(self) -> Decimal:
        """ Calculates the return percentage for the portfolio.

            Returns:
                (Decimal) Portfolio return percentage.
        """
        return self.total_return / self.starting_cash

    @property
    def total_positions(self) -> int:
        """ Calculates the total number of positions in the portfolio.

            Returns:
                (int) Number of positions.
        """
        return len(self.positions)
    
    @property
    def position_allocations(self) -> typing.Dict[types.TickerType, Decimal]:
        """ Calculates the position allocation for the portfolio.

            Returns:
                (Dict[types.TickerType, Decimal]) Position allocation.
        """
        allocations_by_ticker = {}
        for position in self.positions.values():
            if position.ticker in allocations_by_ticker:
                allocations_by_ticker[position.ticker] += position.current_price * position.shares
            else:
                allocations_by_ticker[position.ticker] = position.current_price * position.shares

        return allocations_by_ticker

    @property
    def position_allocation_percentages(self) -> typing.Dict[types.TickerType, Decimal]:
        """ Calculates the position allocation percentage for the portfolio.

            Returns:
                (Dict[types.TickerType, Decimal]) Position allocation percentage.
        """
        position_allocations = self.position_allocations
        total_allocation = Decimal(sum(position_allocations.values()))

        position_allocation_weights = {}
        for ticker, allocation in position_allocations.items():
            if ticker in position_allocation_weights:
                position_allocation_weights[ticker] += allocation / total_allocation
            else:
                position_allocation_weights[ticker] = allocation / total_allocation

        return position_allocation_weights
