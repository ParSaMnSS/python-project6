import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

import inventory_manager


# Window to list, add, and delete categories.
class ManageCategories(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Manage Categories")
        self.resizable(False, False)

        self.db = inventory_manager.InventoryDatabase()
        self.db.create_table()

        self.var_name = tk.StringVar()

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        # Create the LabelFrame for adding a category.
        frm_add = ttk.LabelFrame(self, text="Add Category")
        frm_add.pack(padx=10, pady=10, fill="x")

        self.lbl_name = ttk.Label(frm_add, text="Name")
        self.lbl_name.grid(row=0, column=0, padx=5, pady=5)
        self.txt_name = ttk.Entry(frm_add, textvariable=self.var_name, width=25)
        self.txt_name.grid(row=0, column=1, padx=5, pady=5)
        self.btn_add = ttk.Button(frm_add, text="Add", command=self.on_add_category)
        self.btn_add.grid(row=0, column=2, padx=5, pady=5)

        # Create the Treeview that lists the existing categories.
        frm_list = ttk.LabelFrame(self, text="Categories")
        frm_list.pack(padx=10, pady=(0, 10), fill="both")

        self.tv = ttk.Treeview(frm_list, columns=("name",), show="headings", height=8)
        self.tv.heading("name", text="Name")
        self.tv.column("name", width=200)
        self.tv.pack(side="left", padx=5, pady=5)

        self.tv_scroll = ttk.Scrollbar(frm_list, orient="vertical", command=self.tv.yview)
        self.tv_scroll.pack(side="right", fill="y")
        self.tv.configure(yscrollcommand=self.tv_scroll.set)

        frm_actions = ttk.Frame(self)
        frm_actions.pack(padx=10, pady=(0, 10), fill="x")
        self.btn_delete = ttk.Button(frm_actions, text="Delete Selected", command=self.on_item_delete)
        self.btn_delete.pack(side="right")

    # Reload the category list (iid is the database id).
    def refresh_list(self):
        for item in self.tv.get_children():
            self.tv.delete(item)
        for cat_id, name in self.db.get_categories():
            self.tv.insert("", "end", iid=cat_id, values=(name,))

    def on_add_category(self):
        try:
            clean = inventory_manager.CategoryValidator.validate(self.var_name.get())
            self.db.add_category(*clean)
            self.var_name.set("")
            self.refresh_list()
        except inventory_manager.ValidationError as e:
            msg.showwarning("Validation Error", str(e), parent=self)
        except Exception as e:
            msg.showerror("System Error", f"An unexpected error occurred: {e}", parent=self)

    def on_item_delete(self):
        selected = self.tv.selection()
        if not selected:
            msg.showinfo("Delete", "Please select a category first.", parent=self)
            return
        if msg.askyesno("Confirm", "Delete the selected category?", parent=self):
            self.db.delete_category(int(selected[0]))
            self.refresh_list()
