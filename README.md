# School Inventory Management System

A desktop-based Inventory Management System developed for **CCS School Atrauli (Aligarh)** using Python, Tkinter, and MySQL.

## Features

- Modern graphical login and registration interface
- Forgot Password with security-question recovery
- Add, update, search, and delete products
- Inventory dashboard with product, stock, value, and low-stock statistics
- Sales cart with quantity and discount calculation
- Automatic stock deduction after a successful bill
- Professional Microsoft Word bill generation
- Contact Us and About Us pages
- MySQL database integration
- Password hashing for application users
- Relative project paths for images and generated invoices

## Technologies Used

- Python
- Tkinter / ttk
- Pillow
- MySQL
- MySQL Connector/Python
- python-docx

## Installation

1. Install Python 3.10 or newer and MySQL Server.
2. Clone this repository.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Open `db_config.py` and set your **local** MySQL password. Do not commit your real database password to GitHub.
5. Run:

```bash
python loginpage.py
```

You can also use `run_project.bat` on Windows.

## Database

The application automatically creates the `inventory` database and required inventory table when it connects successfully to MySQL. `schema.sql` is also included for reference/setup.

## Demo Login

The included demo account is:

- Username: `Shreshth`
- Password: `123456`

Change the password after first use.

## Screenshots

Add project screenshots to a `screenshots/` folder and reference them here, for example:

```markdown
![Dashboard](screenshots/dashboard.png)
```

## Project Structure

```text
School project/
├── loginpage.py
├── dashboard.py
├── inventory.py
├── update.py
├── delete.py
├── main2.py
├── contactus.py
├── aboutus.py
├── db_config.py
├── ui_helpers.py
├── requirements.txt
├── schema.sql
├── run_project.bat
├── users.json
├── image/
└── invoices/
```

## Project Team

- Keshav Agrawal
- Shreshth Gaur
- Shivayansh Garg

Under the guidance of **Mr. Abhinav Kaushal**.

## Institution

**CCS School Atrauli (Aligarh)**

## Academic Project

This project was developed as an academic demonstration of GUI development, database connectivity, CRUD operations, authentication, sales processing, inventory management, and automated document generation.
