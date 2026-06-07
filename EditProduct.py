import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

import inventory_manager
from ProductFormWindow import ProductFormWindow


# Window to update an existing product.
class EditProduct(ProductFormWindow):
    def __init__(self, parent=None, pid=None):
        super().__init__(parent)
        self.title("Edit Product")

        self.pid = pid
        self.load_product()

    def build_ui(self):
        super().build_ui()
        btn_update = ttk.Button(self.frm_buttons, text="Update", command=self.on_update_product)
        btn_update.pack(side="right")

    # Fill the form with the existing product values.
    def load_product(self):
        row = self.db.get_product(self.pid)
        if row is None:
            return
        # Row order: pid, sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price.
        self.var_sku.set(row[1])
        self.var_name.set(row[2])
        for cat_id, cat_name in self.categories:
            if cat_id == row[3]:
                self.var_category.set(cat_name)
        for sup_id, sup_name, contact in self.suppliers:
            if sup_id == row[4]:
                self.var_supplier.set(sup_name)
        self.var_quantity.set(str(row[5]))
        self.var_reorder.set(str(row[6]))
        self.var_price.set(str(row[7]))

    # Validate the form and update the existing product.
    def on_update_product(self):
        try:
            clean = inventory_manager.ProductValidator.validate(
                self.var_sku.get(),
                self.var_name.get(),
                self.get_cat_id(),
                self.get_sup_id(),
                self.var_quantity.get(),
                self.var_reorder.get(),
                self.var_price.get(),
            )
            self.db.update_product(self.pid, *clean)
            self.destroy()
        except inventory_manager.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)
        except Exception as e:
            msg.showerror("System Error", f"An unexpected error occurred: {e}", parent=self)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = EditProduct(parent=root, pid=1)
    win.mainloop()
