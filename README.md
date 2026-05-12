# Invoice Creator

A desktop application for creating and storing invoices, built with Python.

## Features

- Create invoices with recipient, seller, product, quantity, price, and VAT information
- Automatically calculates total amount including VAT
- Saves invoices to a local SQLite database
- Exports each invoice as a PDF file
- Simple and clean desktop UI

## Tech Stack

- **UI:** Tkinter
- **Database:** SQLite + SQLAlchemy
- **PDF Generation:** ReportLab
- **Packaging:** PyInstaller

## Project Structure

```
create_invoice/
├── ui.py           # Desktop UI (entry point)
├── service.py      # Business logic
├── models.py       # Database models
├── database.py     # Database connection
└── faturalar.db    # SQLite database (auto-created)
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gulerdeniz/create_invoice.git
cd create_invoice
```

2. Install dependencies:
```bash
pip install sqlalchemy reportlab
```

3. Run the application:
```bash
python ui.py
```

## Building the Executable

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole ui.py
```

The executable will be created in the `dist/` folder. PDF files are saved to a `faturalar/` folder next to the executable.

## Usage

1. Fill in the invoice details
2. Click **Create Invoice**
3. The invoice is saved to the database and exported as a PDF
4. Click **Clear Form** to reset the fields
