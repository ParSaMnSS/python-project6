import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

import inventory_manager


# Window to record a stock IN or OUT movement.
class StockMovement(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Stock Movement")
        self.resizable(False, False)

        self.db = inventory_manager.InventoryDatabase()
        self.db.create_table()

        self.var_product = tk.StringVar()
        self.var_type = tk.StringVar(value="IN")
        self.var_quantity = tk.StringVar()

        self.products = self.db.get_products()

        self.build_ui()

    def build_ui(self):
        frm_form = ttk.LabelFrame(self, text="Record Movement")
        frm_form.pack(padx=10, pady=10, fill="x")

        lbl_product = ttk.Label(frm_form, text="Product")
        lbl_product.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_product = ttk.Combobox(
            frm_form, textvariable=self.var_product, state="readonly", width=28
        )
        self.combo_product["values"] = [f"{p[1]} - {p[2]}" for p in self.products]
        self.combo_product.grid(row=0, column=1, padx=5, pady=5)

        lbl_type = ttk.Label(frm_form, text="Type")
        lbl_type.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        combo_type = ttk.Combobox(
            frm_form, textvariable=self.var_type, state="readonly", width=28
        )
        combo_type["values"] = ["IN", "OUT"]
        combo_type.grid(row=1, column=1, padx=5, pady=5)

        lbl_quantity = ttk.Label(frm_form, text="Quantity")
        lbl_quantity.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_quantity = ttk.Entry(frm_form, textvariable=self.var_quantity, width=30)
        entry_quantity.grid(row=2, column=1, padx=5, pady=5)

        frm_actions = ttk.Frame(self)
        frm_actions.pack(padx=10, pady=(0, 10), fill="x")
        btn_save = ttk.Button(frm_actions, text="Save", command=self.on_save_movement)
        btn_save.pack(side="right")

    # Return the product row chosen in the combobox.
    def get_selected_product(self):
        index = self.combo_product.current()
        if index < 0:
            return None
        return self.products[index]

    def on_save_movement(self):
        try:
            product = self.get_selected_product()
            pid = product[0] if product else None
            current_stock = product[5] if product else 0
            clean = inventory_manager.MovementValidator.validate(
                pid, self.var_type.get(), self.var_quantity.get(), current_stock
            )
            self.db.add_movement(*clean)
            self.destroy()
        except inventory_manager.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)
        except Exception as e:
            msg.showerror("System Error", f"An unexpected error occurred: {e}", parent=self)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = StockMovement(parent=root)
    win.mainloop()
