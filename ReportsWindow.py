import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import matplotlib.pyplot as plt

import inventory_manager


# Window with buttons that open matplotlib charts.
class ReportsWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Reports")
        self.resizable(False, False)

        # Create the database object.
        self.db = inventory_manager.InventoryDatabase()
        self.db.create_table()

        self.build_ui()

    def build_ui(self):
        # Create the LabelFrame that holds the chart buttons.
        frm_buttons = ttk.LabelFrame(self, text="Charts")
        frm_buttons.pack(padx=20, pady=20, fill="x")

        self.btn_category = ttk.Button(frm_buttons, text="Stock by Category", command=self.on_stock_by_category)
        self.btn_category.pack(padx=10, pady=10, fill="x")

        self.btn_status = ttk.Button(frm_buttons, text="Stock Status", command=self.on_stock_status)
        self.btn_status.pack(padx=10, pady=10, fill="x")

    # Bar chart of total stock per category.
    def on_stock_by_category(self):
        data = self.db.get_stock_by_category()
        if not data:
            msg.showinfo("Reports", "No data available to plot.", parent=self)
            return
        names = [row[0] for row in data]
        quantities = [row[1] for row in data]
        plt.figure(num="Stock by Category")
        plt.title("Stock by Category")
        plt.bar(names, quantities, color=["#4e79a7", "#f28e2b", "#59a14f", "#e15759"])
        plt.xlabel("Category")
        plt.ylabel("Total Quantity")
        plt.show()

    # Pie chart of in-stock / low-stock / out-of-stock counts.
    def on_stock_status(self):
        in_stock, low_stock, out_of_stock = self.db.get_stock_status_counts()
        total = in_stock + low_stock + out_of_stock
        if total == 0:
            msg.showinfo("Reports", "No data available to plot.", parent=self)
            return
        labels = ["In Stock", "Low Stock", "Out of Stock"]
        sizes = [in_stock, low_stock, out_of_stock]
        colors = ["#59a14f", "#f28e2b", "#e15759"]
        explode = (0.05, 0.05, 0.05)
        plt.figure(num="Stock Status")
        plt.title("Stock Status")
        plt.pie(sizes, labels=labels, colors=colors, explode=explode, autopct="%.1f%%")
        plt.show()
