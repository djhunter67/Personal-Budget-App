from sqlite3.dbapi2 import Error, paramstyle
import tkinter as tk

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
from budget import Budget_Data, Budget


class Budget_GUI:
    """The GUI that utilizes the database"""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("BUDGET GUI")
        self.root.geometry("400x400")

    def fields(self) -> None:

        item = tk.Entry(self.root, width=30)
        item.grid(row=3, column=1, padx=20)

        cost = tk.Entry(self.root, width=30)
        cost.grid(row=4, column=1, padx=20)

        item_label = tk.Label(self.root, text="Cost")
        item_label.grid(row=3, column=0)

        cost_label = tk.Label(self.root, text="Amount")
        cost_label.grid(row=4, column=0)

    def buttons(self) -> None:

        submit_btn = tk.Button(
            self.root, text="Store information")#, command=Budget.insert_bills()        )
        submit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=0)

        calculate_btn = tk.Button(
            self.root, text="Calculate")#, command=Budget.calculate()        )
        calculate_btn.grid(row=5, column=2, columnspan=2, pady=10, padx=0)
        self.root.mainloop()


def main():

    JUL = Budget("July 2021", 6400.37)
    """
    JUL.insert_bills("AT&T", 70.00)
    JUL.insert_bills("Electric Bill", 157.44)
    JUL.insert_bills("T-mobile", 116.96 - 50)
    JUL.insert_bills("Rent", 2306.39)
    JUL.insert_bills("Life Ins.", 15.22 + 16.63 + 2.50)
    JUL.insert_bills("YouTube Red", 5.99)
    JUL.insert_bills("KinderCare", 980)
    JUL.insert_bills("USAA", 350)
    JUL.insert_bills("Storage", 201.16)
    JUL.insert_bills("Doordash", 9.99)
    JUL.insert_bills("Panda Exprss", 30.26)
    JUL.insert_bills("Publix", 92.53)
    JUL.insert_bills("KinderCare Uniforms", 55.00 * 2)
    JUL.insert_bills("CBR Stem Cells", 1425)
    """
    sql_table_budget = """
    CREATE TABLE IF NOT EXISTS Budget
        (date text NOT NULL,
        name text PRIMARY KEY,
        cost real NOT NULL)
        """

    gui = Budget_GUI()
    gui.fields()
    gui.buttons()

    with Budget_Data("budget_database.db", sql_table_budget) as db:

        # db[0].execute(sql_table_budget)
        for item, cost in JUL.items_costs.items():
            try:
                db[0].table_work(JUL._date, item, cost)
            except Error:
                continue
        db[0].commit()


if __name__ == "__main__":
    main()
