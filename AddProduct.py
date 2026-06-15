import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

import inventory_manager
from ProductFormWindow import ProductFormWindow


# Window to insert a new product.
class AddProduct(ProductFormWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Add Product")

    def build_ui(self):
        super().build_ui()
        self.btn_save = ttk.Button(self.frm_buttons, text="Save", command=self.on_save_product)
        self.btn_save.pack(side="right")

    # Validate the form and insert a new product.
    def on_save_product(self):
        try:
            clean = inventory_manager.ProductValidator.validate(self.var_sku.get(), self.var_name.get(), self.get_cat_id(), self.get_sup_id(), self.var_quantity.get(), self.var_reorder.get(), self.var_price.get())
            self.db.save_product(*clean)
            self.destroy()
        except inventory_manager.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)
        except Exception as e:
            msg.showerror("System Error", f"An unexpected error occurred: {e}", parent=self)
