from tkinter import *
from tkinter import messagebox
from db_config import get_connection
from ui_helpers import COLORS, add_header, card, styled_entry, button


class Database:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.master.title('Add Product')
        self.master.geometry('1120x700')
        self.master.configure(bg=COLORS['bg'])
        self.master.resizable(False, False)

        add_header(master, 'Add Product', 'Add a new item to your inventory database')
        form = card(master, 720, 540); form.place(x=34, y=92)
        side = card(master, 320, 540); side.place(x=770, y=92)

        Label(form, text='Product Information', font=('Segoe UI', 15, 'bold'), bg='white', fg=COLORS['text']).place(x=28, y=24)
        labels = [
            ('Product Name', 'name_e'), ('Stock Quantity', 'stock_e'), ('Cost Price', 'cp_e'),
            ('Selling Price', 'sp_e'), ('Vendor Name', 'vendor_e'), ('Vendor Phone', 'vendor_phone_e')
        ]
        self.entries = {}
        for i, (label_text, attr) in enumerate(labels):
            col = 0 if i < 4 else 1
            row = i if i < 4 else i - 4
            x = 28 + col * 330
            y = 78 + row * 78
            Label(form, text=label_text, font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['muted']).place(x=x, y=y)
            e = styled_entry(form, width=27)
            e.place(x=x, y=y+25, width=285, height=38)
            setattr(self, attr, e); self.entries[attr] = e

        Label(form, text='Product ID (optional)', font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['muted']).place(x=28, y=390)
        self.id_e = styled_entry(form, width=27); self.id_e.place(x=28, y=415, width=285, height=38)
        Label(form, text='Leave blank to let MySQL generate the ID automatically.', font=('Segoe UI', 8), bg='white', fg=COLORS['muted']).place(x=28, y=458)
        button(form, 'CLEAR FORM', self.clear_all, 'secondary', 18).place(x=365, y=414, width=145, height=40)
        button(form, 'ADD PRODUCT', self.get_items, 'primary', 18).place(x=525, y=414, width=145, height=40)

        Label(side, text='Database Status', font=('Segoe UI', 15, 'bold'), bg='white', fg=COLORS['text']).place(x=24, y=24)
        self.status = Label(side, text='Checking database...', font=('Segoe UI', 10), bg='white', fg=COLORS['muted'], wraplength=270, justify='left')
        self.status.place(x=24, y=65)
        Label(side, text='Latest Product ID', font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['muted']).place(x=24, y=145)
        self.id_value = Label(side, text='—', font=('Segoe UI', 30, 'bold'), bg='white', fg=COLORS['blue'])
        self.id_value.place(x=24, y=170)
        Label(side, text='Activity', font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['muted']).place(x=24, y=245)
        self.activity = Label(side, text='No product added yet.', font=('Segoe UI', 10), bg='white', fg=COLORS['text'], wraplength=270, justify='left')
        self.activity.place(x=24, y=275)
        self.refresh_id_info()

    def refresh_id_info(self):
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor(); cursor.execute('SELECT MAX(id) FROM inventory')
            result = cursor.fetchone(); current = result[0] if result and result[0] is not None else 0
            self.id_value.config(text=str(current)); self.status.config(text='Connected to the inventory database.', fg=COLORS['success'])
        except Exception as exc:
            self.status.config(text=f'Database connection error:\n{exc}', fg=COLORS['danger'])
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def get_items(self, *args, **kwargs):
        name = self.name_e.get().strip(); stock = self.stock_e.get().strip(); cp = self.cp_e.get().strip(); sp = self.sp_e.get().strip()
        vendor = self.vendor_e.get().strip(); vendor_phone = self.vendor_phone_e.get().strip(); product_id = self.id_e.get().strip()
        if not all([name, stock, cp, sp]):
            messagebox.showerror('Missing Information', 'Please fill Product Name, Stock, Cost Price and Selling Price.', parent=self.master); return
        try:
            stock_value = int(stock); cp_value = float(cp); sp_value = float(sp)
            if stock_value < 0 or cp_value < 0 or sp_value < 0: raise ValueError
            totalcp = cp_value * stock_value; totalsp = sp_value * stock_value; assumed_profit = totalsp - totalcp
        except ValueError:
            messagebox.showerror('Invalid Values', 'Stock must be a non-negative integer and prices must be non-negative numbers.', parent=self.master); return
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor()
            if product_id:
                sql = '''INSERT INTO inventory (id, name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phoneno)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                values = (product_id, name, stock_value, cp_value, sp_value, totalcp, totalsp, assumed_profit, vendor, vendor_phone)
            else:
                sql = '''INSERT INTO inventory (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phoneno)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                values = (name, stock_value, cp_value, sp_value, totalcp, totalsp, assumed_profit, vendor, vendor_phone)
            cursor.execute(sql, values); con.commit()
            self.activity.config(text=f'Added “{name}” successfully.'); self.clear_all(); self.refresh_id_info()
            messagebox.showinfo('Success', f'{name} was added to the inventory.', parent=self.master)
        except Exception as exc:
            messagebox.showerror('Database Error', str(exc), parent=self.master)
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def clear_all(self):
        for entry in self.entries.values(): entry.delete(0, END)
        self.id_e.delete(0, END)
