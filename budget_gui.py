from sqlite3.dbapi2 import Error
import tkinter as tk
from tkinter.constants import END
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from budget import Budget_Data, Budget

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure

root = tk.Tk()
root.title("BUDGET GUI")
root.geometry("650x450")


class Budget_GUI:
    """The GUI that utilizes the database"""

    def __init__(self, master) -> None:

        """self.master = tk.Tk()
        self.master.title("BUDGET GUI")
        self.master.geometry("600x200")"""

        the_frame = tk.Frame(master)
        the_frame.pack()

        style = ThemedStyle(master)
        style.set_theme("scidgrey")

        # def fields(self) -> None:

        ##############################################################
        #                    ENTRY FIELDS                            #
        ##############################################################

        self.const_month = tk.StringVar()
        self.const_month = ttk.Entry(the_frame, width=20)
        self.const_month.grid(row=1, column=1, padx=5)

        self.const_money = tk.StringVar()
        self.const_money = ttk.Entry(the_frame, width=10)
        self.const_money.grid(row=1, column=3, padx=5)

        self.item = tk.StringVar()
        self.item = ttk.Entry(the_frame, width=20)
        self.item.grid(row=3, column=1, padx=10, pady=20)

        self.cost = tk.StringVar()
        self.cost = ttk.Entry(the_frame, width=20)
        self.cost.grid(row=4, column=1, padx=10)

        # TODO Create a field to display output

        ###############################################################
        #                       FIELD LABELS                          #
        ###############################################################

        init_money_label1 = ttk.Label(the_frame, text="Month Year")
        init_money_label1.grid(row=1, column=0)

        init_money_label2 = ttk.Label(the_frame, text="Starting Money")
        init_money_label2.grid(row=1, column=2)

        item_label = ttk.Label(the_frame, text="Item")
        item_label.grid(row=3, column=0)

        cost_label = ttk.Label(the_frame, text="Amount")
        cost_label.grid(row=4, column=0)

        # def buttons(self) -> None:

        ###############################################################
        #                      BUTTON ACTIONS                         #
        ###############################################################

        def submit() -> None:

            # TODO add class instantion passed from the GUI.

            Budget.insert_bills(Budget, self.item.get(), self.cost.get())
            self.item.delete(0, END)
            self.cost.delete(0, END)

            with Budget_Data("budget_database.db") as db:

                for itemm, costt in Budget.items_costs.items():
                    try:
                        db[0].table_work(None, itemm, costt)
                    except Error:
                        continue
                db[0].commit()

            # TODO Create a remove item button action

        def calculate() -> str:

            calculate_label = ttk.Label(
                the_frame, text=f"{Budget.calculate(Budget):.2f}"
            )
            calculate_label.grid(row=7, column=0, columnspan=2)

        def query() -> str:

            print_records = ""
            with Budget_Data("budget_database.db") as db:
                for date, item, cost, oid in db[1]:
                    print_records += str((f"{item:>20}: {cost:.2f}\n"))

            query_label = ttk.Label(the_frame, text=print_records)
            query_label.grid(row=4, column=2, columnspan=2)

        def construct() -> None:

            Budget(self.const_month.get(), self.const_money.get())

        def clr_query() -> None:

            pass

        ################################################################
        #                       BUTTONS                                #
        ################################################################

        # root.bind("<Return>", submit)
        submit_btn = ttk.Button(the_frame, text="Enter", command=submit)
        submit_btn.grid(row=6, column=0, pady=10, padx=20)

        calculate_btn = ttk.Button(the_frame, text="Funds", command=calculate)
        calculate_btn.grid(row=6, column=1, pady=10, padx=0)

        constructor_btn = ttk.Button(the_frame, text="Fund", command=construct)
        constructor_btn.grid(row=1, column=4, pady=5, padx=5)

        query_btn = ttk.Button(the_frame, text="Show Records", command=query)
        query_btn.grid(row=3, column=2, columnspan=1, pady=10, padx=10, ipadx=37)

        clr_query_ = ttk.Button(the_frame, text="Clear", command=clr_query)
        clr_query_.grid(row=3, column=3, columnspan=1, padx=5, pady=5)

        quit_btn = ttk.Button(the_frame, text="Quit", command=the_frame.quit)
        quit_btn.grid(row=3, column=4, padx=5, pady=5)

        # TODO Create a remove item button


def main():

    # JUL = Budget("July 2021", 6400.37)

    Budget_GUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
