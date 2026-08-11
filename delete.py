from tkinter import *
from tkinter import messagebox
from db_config import get_connection
from ui_helpers import COLORS, add_header, card, styled_entry, button


class Delete:
    def __init__(self, master, *args, **kwargs):
        self.master = master; self.master.title('Delete Product'); self.master.geometry('1120x700'); self.master.configure(bg=COLORS['bg']); self.master.resizable(False, False)
        add_header(master, 'Delete Product', 'Find an item by ID and permanently remove it from inventory')
        search = card(master, 1052, 88); search.place(x=34, y=92)
        Label(search, text='Product ID', font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['muted']).place(x=24, y=20)
        self.id_entry = styled_entry(search); self.id_entry.place(x=24, y=42, width=260, height=36)
        button(search, 'SEARCH PRODUCT', self.search, 'primary', 18).place(x=305, y=40, width=170, height=38)
        self.status = Label(search, text='No product selected.', font=('Segoe UI', 10), bg='white', fg=COLORS['muted']); self.status.place(x=510, y=48)

        details = card(master, 690, 470); details.place(x=34, y=196)
        Label(details, text='Product Details', font=('Segoe UI', 15, 'bold'), bg='white', fg=COLORS['text']).place(x=26, y=22)
        fields = [('Product Name','name'),('Stock Quantity','stock'),('Cost Price','cp'),('Selling Price','sp'),('Total Cost','totalcp'),('Total Sales Value','totalsp'),('Vendor Name','vendor'),('Vendor Phone','vendor_phone')]
        self.labels = {}
        for i, (label, key) in enumerate(fields):
            col = i % 2; row = i // 2; x = 28 + col * 320; y = 72 + row * 76
            Label(details, text=label, font=('Segoe UI', 9, 'bold'), bg='white', fg=COLORS['muted']).place(x=x, y=y)
            value = Label(details, text='—', font=('Segoe UI', 11, 'bold'), bg='white', fg=COLORS['text'], anchor='w')
            value.place(x=x, y=y+24, width=280); self.labels[key] = value

        danger = card(master, 330, 470, '#FFF7F7'); danger.place(x=756, y=196)
        Label(danger, text='Delete Confirmation', font=('Segoe UI', 15, 'bold'), bg='#FFF7F7', fg=COLORS['danger']).place(x=24, y=24)
        Label(danger, text='Deleting a product is permanent.\nMake sure the Product ID is correct before continuing.', font=('Segoe UI', 10), bg='#FFF7F7', fg=COLORS['muted'], justify='left', wraplength=280).place(x=24, y=68)
        self.delete_button = button(danger, 'DELETE PRODUCT', self.delete_record, 'danger', 20)
        self.delete_button.place(x=24, y=180, width=280, height=46)
        button(danger, 'CLEAR', self.clear_entries, 'secondary', 20).place(x=24, y=240, width=280, height=42)

    def search(self):
        product_id = self.id_entry.get().strip()
        if not product_id: messagebox.showerror('Search', 'Please enter a Product ID.', parent=self.master); return
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor(); cursor.execute('SELECT * FROM inventory WHERE id=%s', (product_id,)); result = cursor.fetchone()
            if not result:
                self.status.config(text='Product not found.', fg=COLORS['danger']); self.clear_details(); return
            values = {'name':result[1], 'stock':result[2], 'cp':result[3], 'sp':result[4], 'totalcp':result[5], 'totalsp':result[6], 'vendor':result[8], 'vendor_phone':result[9]}
            for key, value in values.items(): self.labels[key].config(text=str(value))
            self.status.config(text=f'Product #{product_id} loaded. Ready to delete.', fg=COLORS['warning'])
        except Exception as exc: messagebox.showerror('Database Error', str(exc), parent=self.master)
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def delete_record(self):
        product_id = self.id_entry.get().strip()
        if not product_id: messagebox.showerror('Delete', 'Search a Product ID first.', parent=self.master); return
        if not messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete product #{product_id}?', parent=self.master): return
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor(); cursor.execute('DELETE FROM inventory WHERE id=%s', (product_id,))
            if cursor.rowcount == 0: messagebox.showwarning('Delete', 'No record found.', parent=self.master); return
            con.commit(); messagebox.showinfo('Deleted', f'Product #{product_id} was deleted successfully.', parent=self.master); self.clear_entries()
        except Exception as exc: messagebox.showerror('Database Error', str(exc), parent=self.master)
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def clear_details(self):
        for label in self.labels.values(): label.config(text='—')
    def clear_entries(self):
        self.id_entry.delete(0, END); self.clear_details(); self.status.config(text='No product selected.', fg=COLORS['muted'])


if __name__ == '__main__':
    root = Tk(); Delete(root); root.mainloop()
