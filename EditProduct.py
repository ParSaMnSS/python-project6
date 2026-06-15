import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

import inventory_manager
from ProductFormWindow import ProductFormWindow


# Window to update an existing product.
class EditProduct(ProductFormWindow):
    def __init__(self, parent=None, pid=None, sku="", name="", category="", supplier="", quantity="", reorder="", price=""):
        super().__init__(parent)
        self.title("Edit Product")

        self.pid = pid
        # Fill the form with the values passed in from the selected Treeview row.
        self.var_sku.set(sku)
        self.var_name.set(name)
        self.var_category.set(category)
        self.var_supplier.set(supplier)
        self.var_quantity.set(str(quantity))
        self.var_reorder.set(str(reorder))
        self.var_price.set(str(price))

    def build_ui(self):
        super().build_ui()
        self.btn_update = ttk.Button(self.frm_buttons, text="Update", command=self.on_update_product)
        self.btn_update.pack(side="right")

    # Validate the form and update the existing product.
    def on_update_product(self):
        try:
            clean = inventory_manager.ProductValidator.validate(self.var_sku.get(), self.var_name.get(), self.get_cat_id(), self.get_sup_id(), self.var_quantity.get(), self.var_reorder.get(), self.var_price.get())
            self.db.update_product(self.pid, *clean)
            self.destroy()
        except inventory_manager.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)
        except Exception as e:
            msg.showerror("System Error", f"An unexpected error occurred: {e}", parent=self)
