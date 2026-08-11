from tkinter import *
from tkinter import messagebox
from db_config import get_connection
from ui_helpers import COLORS, add_header, card, styled_entry, button


class Update:
    def __init__(self, master, *args, **kwargs):
        self.master = master; self.master.title('Update Product'); self.master.geometry('1120x700'); self.master.configure(bg=COLORS['bg']); self.master.resizable(False, False)
        add_header(master, 'Update Product', 'Search by product ID, edit the details, and save changes')
        search_card = card(master, 1052, 88); search_card.place(x=34, y=92)
        Label(search_card, text='Product ID', font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['muted']).place(x=24, y=20)
        self.id_entry = styled_entry(search_card); self.id_entry.place(x=24, y=42, width=260, height=36)
        button(search_card, 'SEARCH PRODUCT', self.search, 'primary', 18).place(x=305, y=40, width=170, height=38)
        self.search_status = Label(search_card, text='No product loaded.', font=('Segoe UI', 10), bg='white', fg=COLORS['muted']); self.search_status.place(x=510, y=48)

        form = card(master, 1052, 470); form.place(x=34, y=196)
        Label(form, text='Product Details', font=('Segoe UI', 15, 'bold'), bg='white', fg=COLORS['text']).place(x=26, y=22)
        fields = [('Product Name','name'),('Stock Quantity','stock'),('Cost Price','cp'),('Selling Price','sp'),('Vendor Name','vendor'),('Vendor Phone','vendor_phone')]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            col = i % 2; row = i // 2; x = 28 + col * 500; y = 72 + row * 82
            Label(form, text=label, font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['muted']).place(x=x, y=y)
            e = styled_entry(form); e.place(x=x, y=y+24, width=420, height=38); self.entries[key] = e
        button(form, 'CLEAR', self.clear_form, 'secondary', 18).place(x=520, y=332, width=160, height=42)
        button(form, 'SAVE CHANGES', self.update_record, 'success', 18).place(x=700, y=332, width=190, height=42)
        self.note = Label(form, text='Search a product first. Existing values will be loaded into the form.', font=('Segoe UI', 9), bg='white', fg=COLORS['muted'])
        self.note.place(x=28, y=405)

    def search(self):
        product_id = self.id_entry.get().strip()
        if not product_id:
            messagebox.showerror('Search', 'Please enter a Product ID.', parent=self.master); return
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor(); cursor.execute('SELECT * FROM inventory WHERE id=%s', (product_id,)); result = cursor.fetchone()
            if not result:
                self.search_status.config(text='Product not found.', fg=COLORS['danger']); self.clear_form(False); return
            mapping = {'name':result[1], 'stock':result[2], 'cp':result[3], 'sp':result[4], 'vendor':result[8], 'vendor_phone':result[9]}
            for key, value in mapping.items(): self.entries[key].delete(0, END); self.entries[key].insert(0, str(value))
            self.search_status.config(text=f'Loaded product #{product_id}.', fg=COLORS['success']); self.note.config(text='Edit the values above and click SAVE CHANGES.')
        except Exception as exc: messagebox.showerror('Database Error', str(exc), parent=self.master)
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def update_record(self):
        product_id = self.id_entry.get().strip()
        if not product_id: messagebox.showerror('Update', 'Search a Product ID first.', parent=self.master); return
        try:
            name = self.entries['name'].get().strip(); stock = int(self.entries['stock'].get().strip()); cp = float(self.entries['cp'].get().strip()); sp = float(self.entries['sp'].get().strip())
            if not name or stock < 0 or cp < 0 or sp < 0: raise ValueError
            totalcp = cp * stock; totalsp = sp * stock; profit = totalsp - totalcp
        except ValueError:
            messagebox.showerror('Invalid Values', 'Enter a valid product name, non-negative stock, and numeric prices.', parent=self.master); return
        con = cursor = None
        try:
            con = get_connection(); cursor = con.cursor()
            sql = '''UPDATE inventory SET name=%s, stock=%s, cp=%s, sp=%s, totalcp=%s, totalsp=%s, assumed_profit=%s, vendor=%s, vendor_phoneno=%s WHERE id=%s'''
            values = (name, stock, cp, sp, totalcp, totalsp, profit, self.entries['vendor'].get().strip(), self.entries['vendor_phone'].get().strip(), product_id)
            cursor.execute(sql, values)
            if cursor.rowcount == 0: messagebox.showwarning('Update', 'No record was updated.', parent=self.master); return
            con.commit(); self.search_status.config(text=f'Product #{product_id} updated successfully.', fg=COLORS['success']); messagebox.showinfo('Success', 'Product updated successfully.', parent=self.master)
        except Exception as exc: messagebox.showerror('Database Error', str(exc), parent=self.master)
        finally:
            if cursor: cursor.close()
            if con: con.close()

    def clear_form(self, clear_id=True):
        if clear_id: self.id_entry.delete(0, END)
        for e in self.entries.values(): e.delete(0, END)
        self.search_status.config(text='No product loaded.', fg=COLORS['muted'])


if __name__ == '__main__':
    root = Tk(); Update(root); root.mainloop()
