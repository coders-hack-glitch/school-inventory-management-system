from tkinter import *
from ui_helpers import COLORS, setup_window, card


class contact:
    def __init__(self, root):
        self.root = root; setup_window(root, 'Contact Us', '900x560'); root.resizable(False, False)
        header = Frame(root, bg=COLORS['navy'], height=110); header.pack(fill='x'); header.pack_propagate(False)
        Label(header, text='Contact Us', font=('Segoe UI', 27, 'bold'), bg=COLORS['navy'], fg='white').pack(anchor='w', padx=35, pady=(22,0))
        Label(header, text='We are happy to help with your inventory software.', font=('Segoe UI', 10), bg=COLORS['navy'], fg='#CDE6F2').pack(anchor='w', padx=37, pady=2)
        body = Frame(root, bg=COLORS['bg']); body.pack(fill='both', expand=True)
        c1=card(body, 390, 300); c1.place(x=45,y=45); c2=card(body, 390, 300); c2.place(x=465,y=45)
        Label(c1, text='Get in Touch', font=('Segoe UI', 17, 'bold'), bg='white', fg=COLORS['text']).place(x=25,y=25)
        Label(c1, text='Phone', font=('Segoe UI', 9, 'bold'), bg='white', fg=COLORS['muted']).place(x=25,y=82)
        Label(c1, text='+91 6397979092', font=('Segoe UI', 12, 'bold'), bg='white', fg=COLORS['blue_dark']).place(x=25,y=105)
        Label(c1, text='Email', font=('Segoe UI', 9, 'bold'), bg='white', fg=COLORS['muted']).place(x=25,y=150)
        Label(c1, text='keshabagrawal94125@outlook.com', font=('Segoe UI', 11), bg='white', fg=COLORS['text']).place(x=25,y=173)
        Label(c1, text='For inquiries, assistance, or feedback,\nplease use the contact details above.', font=('Segoe UI', 10), bg='white', fg=COLORS['muted'], justify='left').place(x=25,y=220)
        Label(c2, text='School Project', font=('Segoe UI', 17, 'bold'), bg='white', fg=COLORS['text']).place(x=25,y=25)
        Label(c2, text='CCS School Atrauli (Aligarh)', font=('Segoe UI', 14, 'bold'), bg='white', fg=COLORS['blue_dark']).place(x=25,y=82)
        Label(c2, text='Inventory Management Software', font=('Segoe UI', 11), bg='white', fg=COLORS['muted']).place(x=25,y=120)
        Label(c2, text='Simple • Fast • Organized', font=('Segoe UI', 11, 'bold'), bg='white', fg=COLORS['success']).place(x=25,y=180)
        Label(c2, text='Thank you for using our project.', font=('Segoe UI', 10), bg='white', fg=COLORS['muted']).place(x=25,y=230)


if __name__ == '__main__':
    root=Tk(); contact(root); root.mainloop()
