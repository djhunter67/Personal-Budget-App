from sqlite3.dbapi2 import Error
import tkinter as tk
from tkinter.constants import END
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from budget import Budget_Data, Budget

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure


class Budget_GUI:
    """The GUI that utilizes the database"""

    def __init__(self) -> None:

        self.root = tk.Tk()
        self.root.title("BUDGET GUI")
        self.root.geometry("600x200")

        style = ThemedStyle(self.root)
        style.set_theme("scidgrey")

    def fields(self) -> None:

        self.init_money1 = ttk.Entry(self.root, width=20)
        self.init_money1.grid(row=2, column=1, padx=5)

        self.init_money2 = ttk.Entry(self.root, width=10)
        self.init_money2.grid(row=2, column=3, padx=5)

        # global item
        self.item = tk.StringVar()
        self.item = ttk.Entry(self.root, width=20)
        self.item.grid(row=3, column=1, padx=10, pady=20)

        # global cost
        self.cost = tk.StringVar()
        self.cost = ttk.Entry(self.root, width=20)
        self.cost.grid(row=4, column=1, padx=10)

        # disp_field = ttk.Entry(self.root, width=30)
        # disp_field.grid(row=6)

        init_money_label1 = ttk.Label(self.root, text="Month Year")
        init_money_label1.grid(row=2, column=0)

        init_money_label2 = ttk.Label(self.root, text="Starting Money")
        init_money_label2.grid(row=2, column=2)

        item_label = ttk.Label(self.root, text="Item")
        item_label.grid(row=3, column=0)

        cost_label = ttk.Label(self.root, text="Amount")
        cost_label.grid(row=4, column=0)

    def submit(*args) -> None:

        item = args[0][0]
        cost = args[0][1]

        Budget.insert_bills(Budget, item.get(), cost.get())

    def buttons(self) -> None:

        self.root.bind("<Return>", self.submit)
        submit_btn = ttk.Button(
            self.root, text="Enter", command=self.submit(self.item, self.cost)
        )
        submit_btn.grid(row=5, column=0, pady=10, padx=20)

        calculate_btn = ttk.Button(
            self.root, text="Calculate"
        )  # , command=Budget.calculate()        )
        calculate_btn.grid(row=5, column=1, pady=10, padx=0)

        self.root.mainloop()


def main():

    JUL = Budget("July 2021", 6400.37)

    sql_table_budget = """
    CREATE TABLE IF NOT EXISTS Budget
        (date text NOT NULL,
        name text PRIMARY KEY,
        cost real NOT NULL)
        """

    """ gui = Budget_GUI()
    gui.fields()
    gui.buttons() """

    root = tk.Tk()
    root.title("BUDGET GUI")
    root.geometry("650x500")

    style = ThemedStyle(root)
    style.set_theme("scidgrey")
    init_money1 = ttk.Entry(root, width=20)
    init_money1.grid(row=1, column=1, padx=5)

    init_money2 = ttk.Entry(root, width=10)
    init_money2.grid(row=1, column=3, padx=5)

    item = tk.StringVar()
    item = ttk.Entry(root, width=20)
    item.grid(row=3, column=1, padx=10, pady=20)

    cost = tk.StringVar()
    cost = ttk.Entry(root, width=20)
    cost.grid(row=4, column=1, padx=10)

    # disp_field = ttk.Entry(self.root, width=30)
    # disp_field.grid(row=6)

    ###############################################################
    #                       FIELDS                                #
    ###############################################################

    init_money_label1 = ttk.Label(root, text="Month Year")
    init_money_label1.grid(row=1, column=0)

    init_money_label2 = ttk.Label(root, text="Starting Money")
    init_money_label2.grid(row=1, column=2)

    item_label = ttk.Label(root, text="Item")
    item_label.grid(row=3, column=0)

    cost_label = ttk.Label(root, text="Amount")
    cost_label.grid(row=5, column=0)

    ###############################################################
    #                      BUTTON ACTIONS                         #
    ###############################################################

    def submit(*args) -> None:

        Budget.insert_bills(Budget, item.get(), cost.get())
        item.delete(0, END)
        cost.delete(0, END)

    def calculate(*args) -> str:

        calculate_label = ttk.Label(root, text=calculate)
        calculate_label.grid(row=7, column=0, columnspan=2)

        return (f"{Budget.calculate(self=Budget):.2f}")

    def query(*args) -> str:

        print_records = ""
        with Budget_Data("budget_database.db", sql_table_budget) as db:
            for date, item, cost, oid in db[1]:
                print_records += str((f"{item:>20}: {cost:.2f}\n"))

        query_label = ttk.Label(root, text=print_records)
        query_label.grid(row=4, column=2, columnspan=2)

    ################################################################
    #                       BUTTONS                                #
    ################################################################

    # root.bind("<Return>", submit)
    submit_btn = ttk.Button(root, text="Enter", command=submit)
    submit_btn.grid(row=6, column=0, pady=10, padx=20)

    calculate_btn = ttk.Button(root, text="Calculate", command=calculate)
    calculate_btn.grid(row=6, column=1, pady=10, padx=0)

    constructor_btn = ttk.Button(root, text="Enter", command=submit)
    constructor_btn.grid(row=1, column=4, pady=5, padx=5)

    query_btn = ttk.Button(root, text="Show Records", command=query)
    query_btn.grid(row=3, column=2, columnspan=2, pady=10, padx=10, ipadx=137)

    root.mainloop()


if __name__ == "__main__":
    main()
