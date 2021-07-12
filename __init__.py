#!/usr/bin/env python

from budget_gui import Budget_GUI
import tkinter as tk


def main():

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
