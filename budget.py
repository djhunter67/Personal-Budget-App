#!/usr/bin/python
import pathlib
import sqlite3
from sqlite3.dbapi2 import Error
from colorama import Fore as F

R = F.RESET


class Budget:
    """Blueprint for any month and any amount"""

    items_costs = {}
    tot_dollars = 0.0
    # _date = ""

    def __init__(self, month, tot_dollars):

        self._date = month
        self.tot_dollars = tot_dollars

    def insert_bills(self, item, cost) -> None:
        """Take in the item name and item cost"""

        Budget.items_costs.update({item: cost})

    def calculate(self) -> float:
        """Deduct bills from total doll hairs"""
        starting_money = self.tot_dollars
        with Budget_Data("./budget_database.db") as db:
            tot_deductions = 0
            for date, item, cost, oid in db[1]:
                tot_deductions += cost
            net_monies_rem = starting_money - tot_deductions

        return net_monies_rem


class Budget_Data(object):
    """DATABASE Class"""

    def __init__(self, filename) -> None:
        self.filename = filename
        self.cur = None

        if not pathlib.Path(self.filename).exists():
            sql_table_budget = """
                CREATE TABLE IF NOT EXISTS Budget
                (date text NOT NULL,
                name text PRIMARY KEY,
                cost real NOT NULL,
                )
                """

            self.connection = sqlite3.connect(self.filename)
            self.cur = self.connection.cursor()
            self.cur.execute(sql_table_budget)
            self.cur.close()
            self.connection.close()

    def table_work(self, date, name, cost):
        self.cur.execute(
            f"INSERT INTO Budget VALUES\
        ('{date}','{name}',{cost})"
        )

    def execute(self, data):
        """Manipulate data in table"""
        self.cur.execute(data)

    def commit(self):
        self.connection.commit()

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.filename)
            self.cur = self.connection.cursor()
            self.cur.execute("SELECT *, oid FROM Budget ORDER BY cost")
        except Error as e:
            print(e)
        finally:
            rows = self.cur.fetchall()
            # make rows a str to add tables to a new db
            return self, rows

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


def main():

    JUL = Budget("July 2021", 6400.37)

    JUL.insert_bills("AT&T", 70.00)
    JUL.insert_bills("Electric Bill", 157.44)
    JUL.insert_bills("T-mobile", 116.96 - 50)
    JUL.insert_bills("Rent", 2306.39)
    JUL.insert_bills("Life Ins.", 15.22 + 16.63 + 2.50)
    JUL.insert_bills("YouTube Red", 5.99)
    JUL.insert_bills("KinderCare", 980)
    JUL.insert_bills("USAA", 350)
    # JUL.insert_bills("Storage", 201.16)
    JUL.insert_bills("Doordash", 9.99)
    JUL.insert_bills("Panda Exprss", 30.26)
    JUL.insert_bills("Publix", 92.53)
    JUL.insert_bills("KinderCare Uniforms", 55.00 * 2)
    JUL.insert_bills("CBR Stem Cells", 1425)
    JUL.insert_bills("Amazon for Corbin", 109.10)
    JUL.insert_bills("The Dutch Pot", 58.91)
    JUL.insert_bills("Chips: Target", 3.10)
    JUL.insert_bills("Dunkin Donuts", 6.41)
    JUL.insert_bills("QUIP", 10.00)
    JUL.insert_bills("Mod Pizza", 14.17)
    JUL.insert_bills("Dunkin", 17.34)
    JUL.insert_bills("Dinner: Wendys", 28.44)
    JUL.insert_bills("Lunch: The Dutch Pot", 40.05)
    JUL.insert_bills("Juice & Soda", 43.13)
    JUL.insert_bills("Seafood", 49.41)
    JUL.insert_bills("Sam's Club", 124.37)
    JUL.insert_bills("Twin Mattress", 141.54)

    print(
        f'\n{"Starting Funds: ":>22}${F.YELLOW}{JUL.tot_dollars}{R}\
 {JUL._date.upper()}\n'
    )

    with Budget_Data("./budget_database.db") as db:

        for item, cost in JUL.items_costs.items():
            try:
                db[0].table_work(JUL._date, item, cost)
            except Error:
                continue
        db[0].commit()

        for date, item, cost, oid in db[1]:
            print(f"{item:>20}: {F.RED}{cost:.2f}{R}")

    print(f'\n{"Remaining Funds: ":>22}${F.GREEN}{JUL.calculate():.2f}{R}\n')


if __name__ == "__main__":
    main()
