from __future__ import annotations

import time
from typing import Optional
import pandas as pd

'''
Welcome to Forma.ai stock statement generator! In this problem, you will be coding up a transaction
statement generator for a existing trader on our stock trading system. The inputs are provided below, and
the exact output you are to generate is provided after the inputs.

actions: the timestamped actions that the stock trader performed, it can be BUY or SELL type, and they can
buy or sell a few different stocks. However, you should assume that the number of ticker is not limited to
3 types as in the example below, but potentially infinite, so the ticker should not be hardcoded anywhere.

stock_actions: the timestamped actions that the stock performed regardless of who the trader is. It includes
stock splits, and dividend payouts. Even though these actions are not performed by our trader, it still affects
our trader's portfolios, so it should be recorded in the statement that we prepare.

We are looking for easy to understand/extend program that doesn't perform any unnecessary actions.

Feel free to extend the test cases to include new ones that exercises your program to the fullest.
'''


class Statement:
    """
    A place to store all the statements based on date.

    === Private Attributes ===
    _transactions: all transaction statements based on date
    _status: a list of status statements(including stock price, share, and dividend) based on date
    _full: a combination of transaction and status statements based on date
    """
    _transactions: dict
    _status: dict
    _full: dict

    def __init__(self):
        self._transactions = {}
        self._status = {}
        self._full = {}

    def add_transactions(self, date: time, transaction: str):
        """Add new transaction statement to _transactions"""
        if date in self._transactions:
            self._transactions[date].append(transaction)
        else:
            self._transactions[date] = [transaction]

    def add_status(self, date: time, stat: str):
        """Add new status statement to _status"""
        self._status[date] = stat

    def get_transactions(self):
        """Get _transactions"""
        return self._transactions

    def combine(self, date):
        """Combine _transaction and _status together to full"""
        self._full[date] = self._status[date] + '\n' + "  Transactions:"
        for trans in self._transactions[date]:
            self._full[date] = self._full[date] + trans

    def print_full(self):
        """Print all the statements"""
        for i in self._full:
            print(self._full[i])


class Pool:
    """
    A place to store all the stocks' information

    === Private Attributes ===
    _stocks: a list of stocks owned
    """
    _stocks: [Stock]

    def __init__(self) -> None:
        """Initialize the Pool object, the initial value of _stocks is an empty set"""
        self._stocks = []

    def check_stock(self, ticker: str) -> Optional[Stock]:
        """Check whether a stock is in _stocks. If the stock is in _stocks, return the stock; if else, return None"""
        for i in self._stocks:
            if ticker == i.ticker:
                return i

    def add_stock(self, tick: str) -> bool:
        """
        If the stock has already been in _stocks, return False.
        If the stock is not in _stocks, add the stock to _stocks and return True.
        """
        if self.check_stock(tick) is None:
            new_stock = Stock(tick)
            self._stocks.append(new_stock)
            return True
        return False

    def status_output(self, date: str) -> str:
        """Generate a status statement based on date"""
        sum_dividend = 0
        status = "On " + str(date) + ", you have: " + "\n"
        for i in self._stocks:
            sum_dividend += i.dividend
            if i.shares != 0:
                status += "    - " + str(i.shares) + " shares of " + str(i.ticker) + " at $" + str('%.2f' % i.price) \
                          + " per share\n"
        if sum_dividend != 0:
            sum_dividend = '%.2f' % sum_dividend
        status += "    - $" + str(sum_dividend) + " of dividend income"
        return status


class Stock:
    """
    A place to store all the stocks' information

    === Attributes ===
    ticker: the 'name' of the stock
    shares: the number of shares owned for the stock
    price: the average price of the stock bought
    dividend: the amount of dividend of the stock
    """
    ticker: str
    shares: int
    price: float
    dividend: float

    def __init__(self, ticker: str) -> None:
        """
        Initialize the Stock object based on ticker. The initial values of shares,
        price and dividend are all zeros
        """
        self.ticker = ticker
        self.shares = 0
        self.price = 0
        self.dividend = 0

    def _buy_shares(self, shares: int, price: float) -> str:
        """
        The action of buying shares. Current price is averaged to new price.
        Current shares is the original shares plus the shares bought.
        Return transaction statement.
        """
        self.price = (self.price * self.shares + shares * price) / (self.shares + shares)
        self.shares += shares
        return '\n    - You bought ' + str(shares) + ' shares of ' + self.ticker + ' at a price of $' + \
               str('%.2f' % price) + ' per share'

    def _sell_shares(self, shares: int, price: float) -> str:
        """
        The action of selling shares.
        Current shares is the original shares minus the shares bought.
        Return transaction statement.
        """
        self.shares -= shares
        gain = (price - self.price) * shares
        pro_or_loss = 'profit'
        if gain < 0:
            pro_or_loss = 'loss'

        return '\n    - You sold ' + str(shares) + ' shares of ' + self.ticker + ' at a price of $' + \
               str('%.2f' % price) + ' per share for a ' + pro_or_loss + ' of $' + str('%.2f' % gain)

    def _split_shares(self, split: float) -> str:
        """
        The action of splitting shares. Current shares is the original shares times the split number.
        Current price is the original price divided by the split number.
        Return transaction statement.
        """
        self.shares *= split
        self.price /= split
        return '\n    - ' + self.ticker + " split " + str(split) + " to 1, and you have " + \
               str(self.shares) + " shares"

    def _dividend_shares(self, dividend: float) -> str:
        """
        The action of dividend.
        Current dividend is original dividend plus new dividend(shares owned times dividend number)
        Return transaction statement.
        """
        self.dividend += self.shares * dividend
        return "\n    - " + self.ticker + " paid out $" + str('%.2f' % dividend) + \
               " dividend per share, and you have " + str(self.shares) + " shares"

    def action(self, act, price, shares, dividend, split) -> str:
        """Combine all actions together. Return transaction statement."""
        if act == 'BUY':
            return self._buy_shares(int(shares), float(price))
        if act == 'SELL':
            return self._sell_shares(int(shares), float(price))
        if dividend != '':
            return self._dividend_shares(float(dividend))
        if split != '':
            return self._split_shares(int(split))


def main(actions: list, stock_actions: list):
    """
    Main function.
    The basic idea is to combine actions and stock_actions together based on date.
    Then, all the actions are looped to generate and add statements to Statement object(stat)
    Finally, all the statements in stat are printed.
    """
    actions = pd.DataFrame(actions)
    actions['date'] = pd.to_datetime(actions['date']).dt.date
    stock_actions = pd.DataFrame(stock_actions)
    stock_actions['date'] = pd.to_datetime(stock_actions['date']).dt.date
    row_concat = pd.concat([actions, stock_actions], ignore_index=True, sort=False)
    df = row_concat.sort_values(by=['date'])
    my_pool = Pool()
    stat = Statement()
    for i in range(df.shape[0]):
        date = df.iloc[i]['date']
        action = df.iloc[i]['action']
        tick = df.iloc[i]['ticker']
        if type(tick) != str:
            tick = df.iloc[i]['stock']
        price = df.iloc[i]['price']
        shares = df.iloc[i]['shares']
        split = df.iloc[i]['split']
        divid = df.iloc[i]['dividend']

        if my_pool.check_stock(tick) is not None and my_pool.check_stock(tick).shares != 0:
            stat.add_transactions(date, my_pool.check_stock(tick).action(action, price, shares, divid, split))
        elif action == 'BUY':
            my_pool.add_stock(tick)
            stat.add_transactions(date, my_pool.check_stock(tick).action(action, price, shares, divid, split))

        if date in stat.get_transactions():
            stat.add_status(date, my_pool.status_output(date))
            stat.combine(date)

    stat.print_full()


if __name__ == "__main__":
    actions = [{'date': '1992/07/14 11:12:30', 'action': 'BUY', 'price': '12.3', 'ticker': 'AAPL', 'shares': '500'},
               {'date': '1992/09/13 11:15:20', 'action': 'SELL', 'price': '15.3', 'ticker': 'AAPL', 'shares': '100'},
               {'date': '1992/10/14 15:14:20', 'action': 'BUY', 'price': '20', 'ticker': 'MSFT', 'shares': '300'},
               {'date': '1992/10/17 16:14:30', 'action': 'SELL', 'price': '20.2', 'ticker': 'MSFT', 'shares': '200'},
               {'date': '1992/10/19 15:14:20', 'action': 'BUY', 'price': '21', 'ticker': 'MSFT', 'shares': '500'},
               {'date': '1992/10/23 16:14:30', 'action': 'SELL', 'price': '18.2', 'ticker': 'MSFT', 'shares': '600'},
               {'date': '1992/10/25 10:15:20', 'action': 'SELL', 'price': '20.3', 'ticker': 'AAPL', 'shares': '300'},
               {'date': '1992/10/25 16:12:10', 'action': 'BUY', 'price': '18.3', 'ticker': 'MSFT', 'shares': '500'}]
    stock_actions = [{'date': '1992/08/14', 'dividend': '0.10', 'split': '', 'stock': 'AAPL'},
                     {'date': '1992/09/01', 'dividend': '', 'split': '3', 'stock': 'AAPL'},
                     {'date': '1992/10/15', 'dividend': '0.20', 'split': '', 'stock': 'MSFT'},
                     {'date': '1992/10/16', 'dividend': '0.20', 'split': '', 'stock': 'ABC'}]
    main(actions, stock_actions)

"""
On 1992-07-14, you have:
    - 500 shares of AAPL at $12.30 per share
    - $0 of dividend income
  Transactions:
    - You bought 500 shares of AAPL at a price of $12.30 per share
On 1992-08-14, you have:
    - 500 shares of AAPL at $12.30 per share
    - $50.00 of dividend income
  Transactions:
    - AAPL paid out $0.10 dividend per share, and you have 500 shares
On 1992-09-01, you have:
    - 1500 shares of AAPL at $4.10 per share
    - $50.00 of dividend income
  Transactions:
    - AAPL split 3 to 1, and you have 1500 shares
On 1992-09-13, you have:
    - 1400 shares of AAPL at $4.10 per share
    - $50.00 of dividend income
  Transactions:
    - You sold 100 shares of AAPL at a price of $15.30 per share for a profit of $1120.00
On 1992-10-14, you have:
    - 1400 shares of AAPL at $4.10 per share
    - 300 shares of MSFT at $20.00 per share
    - $50.00 of dividend income
  Transactions:
    - You bought 300 shares of MSFT at a price of $20.00 per share
On 1992-10-15, you have:
    - 1400 shares of AAPL at $4.10 per share
    - 300 shares of MSFT at $20.00 per share
    - $110.00 of dividend income
  Transactions:
    - MSFT paid out $0.20 dividend per share, and you have 300 shares
On 1992-10-17, you have:
    - 1400 shares of AAPL at $4.10 per share
    - 100 shares of MSFT at $20.00 per share
    - $110.00 of dividend income
  Transactions:
    - You sold 200 shares of MSFT at a price of $20.20 per share for a profit of $40.00
On 1992-10-19, you have:
    - 1400 shares of AAPL at $4.10 per share
    - 600 shares of MSFT at $20.83 per share
    - $110.00 of dividend income
  Transactions:
    - You bought 500 shares of MSFT at a price of $21.00 per share
On 1992-10-23, you have:
    - 1400 shares of AAPL at $4.10 per share
    - $110.00 of dividend income
  Transactions:
    - You sold 600 shares of MSFT at a price of $18.20 per share for a loss of $-1580.00
On 1992-10-25, you have:
    - 1100 shares of AAPL at $4.10 per share
    - 500 shares of MSFT at $18.30 per share
    - $110.00 of dividend income
  Transactions:
    - You sold 300 shares of AAPL at a price of $20.30 per share for a profit of $4860.00
    - You bought 500 shares of MSFT at a price of $18.30 per share
"""
