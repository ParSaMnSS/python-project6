import tkinter as tk
from tkinter import ttk

import inventory_manager


# Base form window shared by AddProduct and EditProduct.
class ProductFormWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Product Form")
        self.resizable(False, False)

        self.db = inventory_manager.InventoryDatabase()
        self.db.create_table()

        self.var_sku = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_category = tk.StringVar()
        self.var_supplier = tk.StringVar()
        self.var_quantity = tk.StringVar()
        self.var_reorder = tk.StringVar()
        self.var_price = tk.StringVar()

        self.categories = self.db.get_categories()
        self.suppliers = self.db.get_suppliers()

        self.build_ui()

    # Build the shared product form.
    def build_ui(self):
        # Create the LabelFrame container.
        frm_form = ttk.LabelFrame(self, text="Product Details")
        frm_form.pack(padx=10, pady=10, fill="x")

        # Reusable padding for the label and entry columns.
        lbl_pad = {"padx": (10, 5), "pady": 6, "sticky": "w"}
        ent_pad = {"padx": (5, 10), "pady": 6}

        # Create the form widgets.
        self.lbl_sku = ttk.Label(frm_form, text="SKU")
        self.txt_sku = ttk.Entry(frm_form, textvariable=self.var_sku, width=30)

        self.lbl_name = ttk.Label(frm_form, text="Name")
        self.txt_name = ttk.Entry(frm_form, textvariable=self.var_name, width=30)

        self.lbl_category = ttk.Label(frm_form, text="Category")
        self.combo_category = ttk.Combobox(frm_form, textvariable=self.var_category, state="readonly", width=28)
        self.combo_category["values"] = [c[1] for c in self.categories]

        self.lbl_supplier = ttk.Label(frm_form, text="Supplier")
        self.combo_supplier = ttk.Combobox(frm_form, textvariable=self.var_supplier, state="readonly", width=28)
        self.combo_supplier["values"] = [s[1] for s in self.suppliers]

        self.lbl_quantity = ttk.Label(frm_form, text="Quantity")
        self.txt_quantity = ttk.Entry(frm_form, textvariable=self.var_quantity, width=30)

        self.lbl_reorder = ttk.Label(frm_form, text="Reorder Level")
        self.txt_reorder = ttk.Entry(frm_form, textvariable=self.var_reorder, width=30)

        self.lbl_price = ttk.Label(frm_form, text="Unit Price")
        self.txt_price = ttk.Entry(frm_form, textvariable=self.var_price, width=30)

        # Place widgets using the Grid geometry manager.
        self.lbl_sku.grid(row=0, column=0, **lbl_pad)
        self.txt_sku.grid(row=0, column=1, **ent_pad)
        self.lbl_name.grid(row=1, column=0, **lbl_pad)
        self.txt_name.grid(row=1, column=1, **ent_pad)
        self.lbl_category.grid(row=2, column=0, **lbl_pad)
        self.combo_category.grid(row=2, column=1, **ent_pad)
        self.lbl_supplier.grid(row=3, column=0, **lbl_pad)
        self.combo_supplier.grid(row=3, column=1, **ent_pad)
        self.lbl_quantity.grid(row=4, column=0, **lbl_pad)
        self.txt_quantity.grid(row=4, column=1, **ent_pad)
        self.lbl_reorder.grid(row=5, column=0, **lbl_pad)
        self.txt_reorder.grid(row=5, column=1, **ent_pad)
        self.lbl_price.grid(row=6, column=0, **lbl_pad)
        self.txt_price.grid(row=6, column=1, **ent_pad)

        # Subclasses add their Save / Update button to this frame.
        self.frm_buttons = ttk.Frame(self)
        self.frm_buttons.pack(padx=10, pady=(0, 10), fill="x")

    # Map the selected category name back to its id.
    def get_cat_id(self):
        name = self.var_category.get()
        for cat_id, cat_name in self.categories:
            if cat_name == name:
                return cat_id
        return None

    # Map the selected supplier name back to its id.
    def get_sup_id(self):
        name = self.var_supplier.get()
        for sup_id, sup_name, contact in self.suppliers:
            if sup_name == name:
                return sup_id
        return None

    def reset_text_boxes(self):
        self.var_sku.set("")
        self.var_name.set("")
        self.var_category.set("")
        self.var_supplier.set("")
        self.var_quantity.set("")
        self.var_reorder.set("")
        self.var_price.set("")
