from pathlib import Path
from tkinter import *
from tkinter import messagebox, ttk
from db_config import get_connection
from ui_helpers import COLORS, setup_window, card, button, configure_treeview_style

BASE_DIR = Path(__file__).resolve().parent


class IMS:
    def __init__(self, root):
        self.root = root
        setup_window(self.root, 'INVENTORY MANAGEMENT SOFTWARE', '1400x800')
        self.root.config(bg=COLORS['bg'])
        self.root.resizable(False, False)
        self.child_windows = []
        configure_treeview_style()

        self.topmenu = Frame(self.root, bg=COLORS['navy'], height=62)
        self.topmenu.pack(fill='x')
        self.topmenu.pack_propagate(False)

        Label(self.topmenu, text='CCS INVENTORY', font=('Segoe UI', 16, 'bold'),
              bg=COLORS['navy'], fg='white').pack(side='left', padx=(28, 24))
        buttons = [
            ('MAIN', self.show_home), ('ADD', self.Database), ('UPDATE', self.Update),
            ('DELETE', self.Delete), ('SALE', self.Application), ('CONTACT', self.contact),
            ('ABOUT US', self.about), ('EXIT', self.exit_program)
        ]
        for text, command in buttons:
            Button(self.topmenu, text=text, font=('Segoe UI', 10, 'bold'),
                   bg=COLORS['navy'], fg='white', activebackground=COLORS['blue'],
                   activeforeground='white', relief='flat', bd=0, cursor='hand2',
                   padx=12, command=command).pack(side='left', fill='y', padx=1)

        self.content = Frame(self.root, bg=COLORS['bg'])
        self.content.pack(fill='both', expand=True)
        self.root.protocol('WM_DELETE_WINDOW', self.exit_program)

        self.footer = Label(self.root, text='Inventory Software  |  By CCS School Atrauli (Aligarh)',
                            font=('Segoe UI', 9), bg='#102F43', fg='#DCEBF3')
        self.footer.pack(fill='x', ipady=8)
        self.show_home()

    def show_home(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        Label(self.content, text='Dashboard', font=('Segoe UI', 25, 'bold'),
              bg=COLORS['bg'], fg=COLORS['text']).place(x=34, y=24)
        Label(self.content, text='Overview of your inventory and recent activity',
              font=('Segoe UI', 10), bg=COLORS['bg'], fg=COLORS['muted']).place(x=36, y=62)

        stats = self.get_stats()
        cards = [
            ('TOTAL PRODUCTS', stats['products'], 'Products in database', COLORS['blue'], COLORS['soft_blue']),
            ('TOTAL STOCK', stats['stock'], 'Units currently available', '#7A5AF8', '#F0ECFF'),
            ('INVENTORY VALUE', f"₹{stats['value']:,.2f}", 'At selling price', COLORS['success'], COLORS['soft_green']),
            ('LOW STOCK', stats['low'], '10 or fewer units', COLORS['warning'], COLORS['soft_orange']),
        ]
        x = 35
        for title, value, desc, accent, bg in cards:
            c = card(self.content, 285, 118, bg)
            c.place(x=x, y=98)
            Frame(c, bg=accent, width=6).place(x=0, y=0, relheight=1)
            Label(c, text=title, font=('Segoe UI', 9, 'bold'), bg=bg, fg=COLORS['muted']).place(x=22, y=18)
            Label(c, text=str(value), font=('Segoe UI', 24, 'bold'), bg=bg, fg=COLORS['text']).place(x=22, y=42)
            Label(c, text=desc, font=('Segoe UI', 9), bg=bg, fg=COLORS['muted']).place(x=22, y=82)
            x += 305

        quick = card(self.content, 430, 170)
        quick.place(x=35, y=240)
        Label(quick, text='Quick Actions', font=('Segoe UI', 15, 'bold'), bg='white', fg=COLORS['text']).place(x=22, y=18)
        button(quick, '+  Add Product', self.Database, 'primary', 18).place(x=22, y=65, width=180, height=42)
        button(quick, '↗  New Sale', self.Application, 'success', 18).place(x=215, y=65, width=180, height=42)
        button(quick, '↻  Refresh', self.show_home, 'secondary', 18).place(x=22, y=115, width=180, height=36)
        button(quick, '⚙  Update Product', self.Update, 'secondary', 18).place(x=215, y=115, width=180, height=36)

        recent = card(self.content, 860, 355)
        recent.place(x=485, y=240)
        Label(recent, text='Recent Inventory', font=('Segoe UI', 15, 'bold'), bg='white', fg=COLORS['text']).pack(anchor='w', padx=22, pady=(18, 2))
        Label(recent, text='Latest products added to the database', font=('Segoe UI', 9), bg='white', fg=COLORS['muted']).pack(anchor='w', padx=22, pady=(0, 12))

        table_frame = Frame(recent, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 18))
        columns = ('id', 'name', 'stock', 'cp', 'sp', 'vendor')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Modern.Treeview')
        headings = {'id':'ID', 'name':'PRODUCT', 'stock':'STOCK', 'cp':'COST', 'sp':'SELLING', 'vendor':'VENDOR'}
        widths = {'id':60, 'name':200, 'stock':90, 'cp':100, 'sp':100, 'vendor':170}
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor='center' if col != 'name' and col != 'vendor' else 'w')
        scroll = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        for row in self.get_recent_products():
            tree.insert('', 'end', values=row)

    def get_stats(self):
        stats = {'products': 0, 'stock': 0, 'value': 0.0, 'low': 0}
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor()
            cursor.execute('SELECT COUNT(*), COALESCE(SUM(stock),0), COALESCE(SUM(sp * stock),0), COALESCE(SUM(stock <= 10),0) FROM inventory')
            result = cursor.fetchone()
            if result:
                stats['products'], stats['stock'], stats['value'], stats['low'] = result
        except Exception:
            pass
        finally:
            if cursor: cursor.close()
            if con: con.close()
        return stats

    def get_recent_products(self):
        rows = []
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor()
            cursor.execute('SELECT id, name, stock, cp, sp, vendor FROM inventory ORDER BY id DESC LIMIT 8')
            rows = cursor.fetchall()
        except Exception:
            pass
        finally:
            if cursor: cursor.close()
            if con: con.close()
        return rows

    def _open_window(self, title, constructor, geometry='1120x700'):
        window = Toplevel(self.root)
        setup_window(window, title, geometry)
        window.transient(self.root)
        self.child_windows.append(window)
        try:
            constructor(window)
        except Exception:
            if window.winfo_exists(): window.destroy()
            raise
        return window

    def Database(self):
        from inventory import Database
        self._open_window('Add Product', Database)
    def Application(self):
        from main2 import Application
        self._open_window('Sales', Application)
    def Delete(self):
        from delete import Delete
        self._open_window('Delete Product', Delete)
    def about(self):
        from aboutus import about
        self._open_window('About Us', about)
    def contact(self):
        from contactus import contact
        self._open_window('Contact Us', contact)
    def Update(self):
        from update import Update
        self._open_window('Update Product', Update)
    def menu(self):
        self.show_home()
    def exit_program(self):
        self.root.destroy()


if __name__ == '__main__':
    root = Tk(); IMS(root); root.mainloop()
