# coding: utf-8

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
import typing


@dataclass
class Position:
    """ Position dataclass to hold the position information

        Attributes:
            ticker (str): Ticker symbol
            shares (Decimal): Number of shares
            purchase_price (Decimal): Purchase price
            purchase_date (datetime): Purchase date
            current_price (Decimal): Current price
    """
    ticker: str
    shares: Decimal
    purchase_price: Decimal
    purchased_at: datetime
    current_price: Decimal
    current_datetime: datetime

    @property
    def total_return(self) -> Decimal:
        """ Calculates the return value of the position.

            Returns:
                (Decimal) Return value.
        """
        return (self.current_price - self.purchase_price) * self.shares


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
    positions: typing.List[Position]

    def get_position(self, ticker: str) -> typing.Optional[Position]:
        """ Gets the position for the given ticker.

            Args:
                ticker (str): Ticker symbol to get the position for.

            Returns:
                (Optional[Position]) Position for the given ticker.
        """
        for position in self.positions:
            if position.ticker == ticker:
                return position

        return None

    @property
    def position_value(self) -> Decimal:
        """ Calculates the position value of the portfolio.

            Returns:
                (Decimal) Position value.
        """
        return sum([position.current_price * position.shares for position in self.positions])

    @property
    def total_position_return(self) -> Decimal:
        """ Calculates the total position return for the portfolio.

            Returns:
                (Decimal) Portfolio position return.
        """
        return sum([position.total_return for position in self.positions])

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
    def position_allocations(self) -> typing.Dict[str, Decimal]:
        """ Calculates the position allocation for the portfolio.

            Returns:
                (Dict[str, Decimal]) Position allocation.
        """
        return {position.ticker: position.current_price * position.shares for position in self.positions}

    @property
    def position_allocation_percentages(self) -> typing.Dict[str, Decimal]:
        """ Calculates the position allocation percentage for the portfolio.

            Returns:
                (Dict[str, Decimal]) Position allocation percentage.
        """
        position_allocations = self.position_allocations
        total_allocation = Decimal(sum(position_allocations.values()))
        return {ticker: allocation / total_allocation for ticker, allocation in position_allocations.items()}
