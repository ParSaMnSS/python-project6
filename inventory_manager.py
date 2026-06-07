import sqlite3
from datetime import datetime


# Custom exception for validation errors.
class ValidationError(Exception):
    pass


# Validator classes check user input and return cleaned values.
class ProductValidator:
    @staticmethod
    def validate(sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price):
        sku = str(sku).strip()
        name = str(name).strip()

        if not sku or not name:
            raise ValidationError("SKU and Name fields cannot be empty.")
        if not cat_id:
            raise ValidationError("Please select a category.")
        if not sup_id:
            raise ValidationError("Please select a supplier.")

        try:
            quantity = int(str(quantity).strip())
        except ValueError:
            raise ValidationError("Quantity must be a valid integer.")
        if quantity < 0:
            raise ValidationError("Quantity cannot be negative.")

        try:
            reorder_lvl = int(str(reorder_lvl).strip())
        except ValueError:
            raise ValidationError("Reorder level must be a valid integer.")
        if reorder_lvl < 0:
            raise ValidationError("Reorder level cannot be negative.")

        try:
            unit_price = float(str(unit_price).strip())
        except ValueError:
            raise ValidationError("Unit price must be a valid number.")
        if unit_price < 0:
            raise ValidationError("Unit price cannot be negative.")

        return sku, name, int(cat_id), int(sup_id), quantity, reorder_lvl, unit_price


class CategoryValidator:
    @staticmethod
    def validate(name):
        name = str(name).strip()
        if not name:
            raise ValidationError("Category name cannot be empty.")
        return (name,)


class SupplierValidator:
    @staticmethod
    def validate(name, contact):
        name = str(name).strip()
        contact = str(contact).strip()
        if not name:
            raise ValidationError("Supplier name cannot be empty.")
        return name, contact


class MovementValidator:
    @staticmethod
    def validate(pid, mtype, quantity, current_stock):
        if not pid:
            raise ValidationError("Please select a product.")
        try:
            quantity = int(str(quantity).strip())
        except ValueError:
            raise ValidationError("Quantity must be a valid integer.")
        if quantity <= 0:
            raise ValidationError("Quantity must be a positive integer.")
        if mtype == "OUT" and quantity > current_stock:
            raise ValidationError("Out quantity cannot exceed the current stock.")
        return int(pid), mtype, quantity


# Data layer: handles all SQLite access for the application.
class InventoryDatabase:
    def __init__(self, db_name="inventory.db"):
        self.db_name = db_name

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    # Create the four tables if they do not already exist.
    def create_table(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Categories (
                    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Suppliers (
                    sup_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Products (
                    pid INTEGER PRIMARY KEY AUTOINCREMENT,
                    sku TEXT NOT NULL,
                    name TEXT NOT NULL,
                    cat_id INTEGER,
                    sup_id INTEGER,
                    quantity INTEGER DEFAULT 0,
                    reorder_lvl INTEGER DEFAULT 0,
                    unit_price REAL DEFAULT 0
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Movements (
                    mid INTEGER PRIMARY KEY AUTOINCREMENT,
                    pid INTEGER,
                    mtype TEXT,
                    quantity INTEGER,
                    mdate TEXT
                )
            """)

    # Clear the tables and insert some sample data.
    def fill_data(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Movements")
            cur.execute("DELETE FROM Products")
            cur.execute("DELETE FROM Suppliers")
            cur.execute("DELETE FROM Categories")

            categories = [("Electronics",), ("Stationery",), ("Hardware",)]
            cur.executemany("INSERT INTO Categories (name) VALUES (?)", categories)

            suppliers = [
                ("TechWorld Ltd", "0212 555 1010"),
                ("OfficePlus", "0216 555 2020"),
                ("BuildMart", "0312 555 3030"),
            ]
            cur.executemany(
                "INSERT INTO Suppliers (name, contact) VALUES (?, ?)", suppliers
            )

            products = [
                ("ELC-001", "USB Cable", 1, 1, 50, 10, 3.5),
                ("ELC-002", "Wireless Mouse", 1, 1, 8, 10, 12.0),
                ("STA-001", "A4 Paper Pack", 2, 2, 0, 5, 4.25),
                ("STA-002", "Blue Pen Box", 2, 2, 100, 20, 6.0),
                ("HRD-001", "Screwdriver Set", 3, 3, 15, 5, 9.75),
            ]
            cur.executemany(
                """INSERT INTO Products
                   (sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                products,
            )

    # --- Category methods ---
    def add_category(self, name):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Categories (name) VALUES (?)", (name,))
            return cur.lastrowid

    def get_categories(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT cat_id, name FROM Categories ORDER BY name")
            return cur.fetchall()

    def delete_category(self, cat_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Categories WHERE cat_id = ?", (cat_id,))

    # --- Supplier methods ---
    def add_supplier(self, name, contact):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Suppliers (name, contact) VALUES (?, ?)", (name, contact)
            )
            return cur.lastrowid

    def get_suppliers(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT sup_id, name, contact FROM Suppliers ORDER BY name")
            return cur.fetchall()

    def delete_supplier(self, sup_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Suppliers WHERE sup_id = ?", (sup_id,))

    # --- Product methods ---
    def save_product(self, sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO Products
                   (sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price),
            )
            return cur.lastrowid

    def update_product(self, pid, sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """UPDATE Products SET
                   sku = ?, name = ?, cat_id = ?, sup_id = ?,
                   quantity = ?, reorder_lvl = ?, unit_price = ?
                   WHERE pid = ?""",
                (sku, name, cat_id, sup_id, quantity, reorder_lvl, unit_price, pid),
            )

    # Read all products with their category and supplier names for display.
    def get_products(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.pid, p.sku, p.name,
                       c.name AS category, s.name AS supplier,
                       p.quantity, p.reorder_lvl, p.unit_price
                FROM Products p
                LEFT JOIN Categories c ON p.cat_id = c.cat_id
                LEFT JOIN Suppliers s ON p.sup_id = s.sup_id
                ORDER BY p.name
            """)
            return cur.fetchall()

    def get_product(self, pid):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT pid, sku, name, cat_id, sup_id,
                          quantity, reorder_lvl, unit_price
                   FROM Products WHERE pid = ?""",
                (pid,),
            )
            return cur.fetchone()

    def delete_product(self, pid):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Products WHERE pid = ?", (pid,))

    def get_count_and_total_value(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*), COALESCE(SUM(quantity * unit_price), 0) FROM Products"
            )
            return cur.fetchone()

    # --- Movement methods ---
    # Record a movement and adjust the product quantity (IN adds, OUT subtracts).
    def add_movement(self, pid, mtype, quantity):
        with self.get_connection() as conn:
            cur = conn.cursor()
            mdate = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute(
                "INSERT INTO Movements (pid, mtype, quantity, mdate) VALUES (?, ?, ?, ?)",
                (pid, mtype, quantity, mdate),
            )
            if mtype == "IN":
                cur.execute(
                    "UPDATE Products SET quantity = quantity + ? WHERE pid = ?",
                    (quantity, pid),
                )
            else:
                cur.execute(
                    "UPDATE Products SET quantity = quantity - ? WHERE pid = ?",
                    (quantity, pid),
                )

    def get_movements(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT m.mid, p.name, m.mtype, m.quantity, m.mdate
                FROM Movements m
                LEFT JOIN Products p ON m.pid = p.pid
                ORDER BY m.mid DESC
            """)
            return cur.fetchall()

    # --- Chart data methods ---
    def get_stock_by_category(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.name, COALESCE(SUM(p.quantity), 0)
                FROM Categories c
                LEFT JOIN Products p ON p.cat_id = c.cat_id
                GROUP BY c.cat_id
                ORDER BY c.name
            """)
            return cur.fetchall()

    # Count products that are in stock, low on stock, or out of stock.
    def get_stock_status_counts(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM Products WHERE quantity = 0")
            out_of_stock = cur.fetchone()[0]
            cur.execute(
                "SELECT COUNT(*) FROM Products WHERE quantity > 0 AND quantity <= reorder_lvl"
            )
            low_stock = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM Products WHERE quantity > reorder_lvl")
            in_stock = cur.fetchone()[0]
            return in_stock, low_stock, out_of_stock


if __name__ == "__main__":
    db = InventoryDatabase()
    db.create_table()
    db.fill_data()
    print("Database initialized.")
