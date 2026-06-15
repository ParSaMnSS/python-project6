# Inventory & Warehouse Management (SEN4017)

A tkinter desktop application that tracks products, the categories and suppliers they
belong to, and stock-in / stock-out movements, with reorder-level warnings. Built with
Python and tkinter, using SQLite for storage.

## Running

```
python inventory_manager.py   # creates and seeds inventory.db
python build_locales.py       # compiles the .po files into .mo (run once)
python ListProducts.py        # starts the application
```

## Features

- Seven GUI windows (main list, add, edit, categories, suppliers, stock movement, reports).
- Validation on every data-input form; no database write happens on invalid input.
- Charts with matplotlib (stock by category, stock status pie).
- Excel import / export with openpyxl.
- Internationalization for English and Turkish with gettext.

## Files

- `inventory_manager.py` — validators and the SQLite data layer.
- `ProductFormWindow.py`, `AddProduct.py`, `EditProduct.py` — shared product form.
- `ManageCategories.py`, `ManageSuppliers.py`, `StockMovement.py` — secondary windows.
- `ReportsWindow.py` — matplotlib charts.
- `ListProducts.py` — main window, internationalization, and Excel import/export.
- `build_locales.py` — compiles the `.po` files into `.mo`.
- `locales/` — English and Turkish translation files.

## Task split

Tasks are shared equally between the two group members. If one member leaves, the other
covers both columns.

**Member A — Data layer & product entry**

- `inventory_manager.py`: schema, `create_table`, `fill_data`, CRUD/query methods, the
  movement-updates-quantity logic, and the chart-data queries.
- All validator classes and the validation rules.
- `ProductFormWindow.py`, `AddProduct.py`, `EditProduct.py`.
- Excel import/export with openpyxl.

**Member B — Main UI, secondary windows, charts & i18n**

- `ListProducts.py`: Treeview, low-stock highlighting, statistics, menu/buttons, key
  bindings, and wiring every sub-window.
- `ManageCategories.py`, `ManageSuppliers.py`, `StockMovement.py`.
- `ReportsWindow.py` and both matplotlib charts.
- Internationalization (EN/TR): gettext setup, language switch, `.po` files,
  `build_locales.py`.

## Generative-AI disclosure

This project was built with AI assistance (an AI coding assistant). The report's
Generative-AI appendix should log the prompts used and note which files were
AI-generated, as required by the assignment.
