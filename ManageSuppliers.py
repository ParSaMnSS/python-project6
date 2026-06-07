import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

import inventory_manager


# Window to list, add, and delete suppliers.
class ManageSuppliers(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Manage Suppliers")
        self.resizable(False, False)

        self.db = inventory_manager.InventoryDatabase()
        self.db.create_table()

        self.var_name = tk.StringVar()
        self.var_contact = tk.StringVar()

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        frm_add = ttk.LabelFrame(self, text="Add Supplier")
        frm_add.pack(padx=10, pady=10, fill="x")

        lbl_name = ttk.Label(frm_add, text="Name")
        lbl_name.grid(row=0, column=0, padx=5, pady=5)
        entry_name = ttk.Entry(frm_add, textvariable=self.var_name, width=25)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        lbl_contact = ttk.Label(frm_add, text="Contact")
        lbl_contact.grid(row=1, column=0, padx=5, pady=5)
        entry_contact = ttk.Entry(frm_add, textvariable=self.var_contact, width=25)
        entry_contact.grid(row=1, column=1, padx=5, pady=5)

        btn_add = ttk.Button(frm_add, text="Add", command=self.on_add_supplier)
        btn_add.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

        frm_list = ttk.LabelFrame(self, text="Suppliers")
        frm_list.pack(padx=10, pady=(0, 10), fill="both")

        self.tv = ttk.Treeview(
            frm_list, columns=("name", "contact"), show="headings", height=8
        )
        self.tv.heading("name", text="Name")
        self.tv.heading("contact", text="Contact")
        self.tv.column("name", width=160)
        self.tv.column("contact", width=140)
        self.tv.pack(side="left", padx=5, pady=5)

        tv_scroll = ttk.Scrollbar(frm_list, orient="vertical", command=self.tv.yview)
        tv_scroll.pack(side="right", fill="y")
        self.tv.configure(yscrollcommand=tv_scroll.set)

        frm_actions = ttk.Frame(self)
        frm_actions.pack(padx=10, pady=(0, 10), fill="x")
        btn_delete = ttk.Button(frm_actions, text="Delete Selected", command=self.on_item_delete)
        btn_delete.pack(side="right")

    # Reload the supplier list (iid is the database id).
    def refresh_list(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        for sup_id, name, contact in self.db.get_suppliers():
            self.tv.insert("", "end", iid=sup_id, values=(name, contact))

    def on_add_supplier(self):
        try:
            clean = inventory_manager.SupplierValidator.validate(
                self.var_name.get(), self.var_contact.get()
            )
            self.db.add_supplier(*clean)
            self.var_name.set("")
            self.var_contact.set("")
            self.refresh_list()
        except inventory_manager.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)
        except Exception as e:
            msg.showerror("System Error", f"An unexpected error occurred: {e}", parent=self)

    def on_item_delete(self):
        selected = self.tv.selection()
        if not selected:
            msg.showinfo("Delete", "Please select a supplier first.", parent=self)
            return
        if msg.askyesno("Confirm", "Delete the selected supplier?", parent=self):
            self.db.delete_supplier(int(selected[0]))
            self.refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    win = ManageSuppliers(parent=root)
    win.mainloop()
