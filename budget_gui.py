from sqlite3.dbapi2 import Error
import tkinter as tk
from tkinter.constants import END
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showerror
from ttkthemes import ThemedStyle
from budget import Budget_Data, Budget


# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure


class Budget_GUI(tk.Frame):
    """The GUI that utilizes the database"""

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.the_frame = master

        style = ThemedStyle(master)
        style.set_theme("scidgrey")

        ##############################################################
        #                    ENTRY FIELDS                            #
        ##############################################################

        list1 = [
            "PICK MONTH",
            "JUL 2021",
            "AUG 2021",
            "SEP 2021",
            "OCT 2021",
            "NOV 2021",
            "DEC 2021",
            "JAN 2022"
            ]
        self.const_month = tk.StringVar()
        # self.const_month.set()
        self.const_month_ = ttk.OptionMenu(
            self.the_frame, self.const_month, *list1)
        self.const_month_.grid(row=1, column=1, padx=0)

        self.const_money = tk.StringVar()
        self.const_money_ = ttk.Entry(
            self.the_frame, textvariable=self.const_money, width=10
        )
        self.const_money_.grid(row=1, column=3, padx=5)

        self.item = tk.StringVar()
        self.item_ = ttk.Entry(self.the_frame, textvariable=self.item, width=10)
        self.item_.grid(row=3, column=1, padx=10, pady=20)

        self.cost = tk.StringVar()
        self.cost_ = ttk.Entry(self.the_frame, textvariable=self.cost, width=10)
        self.cost_.grid(row=4, column=1, padx=10)

        self.remove_entry = tk.StringVar()
        self.remove_entry_ = ttk.Entry(
            self.the_frame, textvariable=self.remove_entry, width=10
        )
        self.remove_entry_.grid(row=5, column=1, padx=10)

        ###############################################################
        #                       FIELD LABELS                          #
        ###############################################################

        init_money_label1 = ttk.Label(self.the_frame, text="Month Year")
        init_money_label1.grid(row=1, column=0)

        init_money_label2 = ttk.Label(self.the_frame, text="Starting Money")
        init_money_label2.grid(row=1, column=2)

        item_label = ttk.Label(self.the_frame, text="Item")
        item_label.grid(row=3, column=0)

        cost_label = ttk.Label(self.the_frame, text="Amount")
        cost_label.grid(row=4, column=0)

        remove_item = ttk.Label(self.the_frame, text="Remove Item")
        remove_item.grid(row=5, column=0)

        ###############################################################
        #                      BUTTON ACTIONS                         #
        ###############################################################

        def submit(event) -> None:

            Budget.insert_bills(Budget, self.item.get(), self.cost.get())
            self.item_.delete(0, END)
            self.cost_.delete(0, END)

            with Budget_Data("./budget_database.db") as db:

                for itemm, costt in Budget.items_costs.items():
                    try:
                        db[0].table_work(None, itemm, costt)
                    except Error:
                        showerror("info", "Item and cost not added")
                        continue
                    finally:
                        db[0].commit()
                        showinfo("info", "Item commited")

        def calculate() -> None:

            showinfo("Remaining Funds", f"${Budget.calculate(Budget)}")

        def query() -> None:

            print_records = ""
            with Budget_Data("./budget_database.db") as db:
                for date, item, cost, oid in db[1]:
                    print_records += str((f"{item:>20}: {cost:.2f}\n"))

            showinfo("BUDGET GUI", print_records)

        def construct() -> None:

            if not (self.const_month.get() and self.const_money.get()):
                showerror(None, "Both Date and Starting monies are required")
                return None
            else:
                month = Budget(self.const_month.get(), self.const_money.get())
                showinfo("Monthly Income", month.tot_dollars)

        def remove_() -> None:

            if not self.remove_entry.get():
                showerror(
                    "info",
                    "Item does not exist.\nItems\
 are case sensitive",
                )
                return None
            else:
                with Budget_Data("./budget_database.db") as db:

                    remove_thing = f"\nDELETE FROM Budget\nWHERE name =\
                    '{self.remove_entry.get()}';"
                    db[0].execute(remove_thing)
                    db[0].commit()
                    showinfo(
                        "info",
                        f"{self.remove_entry.get()}\
 deleted successfully!",
                    )
                    self.remove_entry_.delete(0, END)

        ################################################################
        #                       BUTTONS                                #
        ################################################################

        submit_btn = ttk.Button(self.the_frame, text="Submit")  # , command=submit)
        submit_btn.grid(row=6, column=0, pady=10, padx=20)
        self.the_frame.bind(("<Return>"), submit)

        calculate_btn = ttk.Button(self.the_frame, text="Funds", command=calculate)
        calculate_btn.grid(row=6, column=1, pady=10, padx=0)

        constructor_btn = ttk.Button(self.the_frame, text="Fund", command=construct)
        constructor_btn.grid(row=1, column=4, pady=5, padx=5)

        query_btn = ttk.Button(self.the_frame, text="Show Records", command=query)
        query_btn.grid(row=3, column=2, columnspan=None, pady=10, padx=10, ipadx=57)

        quit_btn = tk.Button(
            self.the_frame, text="Quit", fg="red", command=self.the_frame.quit
        )
        quit_btn.grid(row=3, column=3, padx=5, pady=5)

        remove_item = ttk.Button(self.the_frame, text="Remove", command=remove_)
        remove_item.grid()


def main():

    # JUL = Budget("July 2021", 6400.37)

    root = tk.Tk()
    root.title("BUDGET GUI")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w // 14}x{h // 8}+0+0")
    root.focus_set()
    root.bind("<Escape>", lambda e: e.widget.quit())

    Budget_GUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
