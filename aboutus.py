from tkinter import *
from ui_helpers import COLORS, setup_window, card


class about:
    def __init__(self, root):
        self.root = root; setup_window(root, 'About Us', '1000x600'); root.resizable(False, False)
        header = Frame(root, bg=COLORS['navy'], height=115); header.pack(fill='x'); header.pack_propagate(False)
        Label(header, text='About the Project', font=('Segoe UI', 27, 'bold'), bg=COLORS['navy'], fg='white').pack(anchor='w', padx=35, pady=(22,0))
        Label(header, text='A school project focused on practical inventory management.', font=('Segoe UI', 10), bg=COLORS['navy'], fg='#CDE6F2').pack(anchor='w', padx=37, pady=2)
        body=Frame(root,bg=COLORS['bg']); body.pack(fill='both',expand=True)
        intro=card(body,920,150); intro.place(x=40,y=30)
        Label(intro,text='Inventory Management Software',font=('Segoe UI',18,'bold'),bg='white',fg=COLORS['text']).place(x=25,y=22)
        Label(intro,text='A desktop application designed to streamline product, stock and sales management for a school or small business.',font=('Segoe UI',10),bg='white',fg=COLORS['muted'],wraplength=850,justify='left').place(x=25,y=62)
        Label(intro,text='Built with Python • Tkinter • MySQL',font=('Segoe UI',10,'bold'),bg='white',fg=COLORS['blue_dark']).place(x=25,y=105)
        Label(body,text='Project Team',font=('Segoe UI',17,'bold'),bg=COLORS['bg'],fg=COLORS['text']).place(x=40,y=205)
        names=[('Shivayansh Garg','Student Developer')]
        x=40
        for name,role in names:
            c=card(body,285,160); c.place(x=x,y=245)
            Label(c,text=name,font=('Segoe UI',13,'bold'),bg='white',fg=COLORS['text']).place(x=20,y=30)
            Label(c,text=role,font=('Segoe UI',9),bg='white',fg=COLORS['muted']).place(x=20,y=62)
            Frame(c,bg=COLORS['blue'],height=3,width=70).place(x=20,y=95)
            Label(c,text='Inventory Management Project',font=('Segoe UI',9),bg='white',fg=COLORS['muted']).place(x=20,y=115)
            x+=310
        Label(body,text='Under the guidance of Mr. Abhinav Kaushal',font=('Segoe UI',10,'bold'),bg=COLORS['bg'],fg=COLORS['muted']).place(x=40,y=435)
        Label(body,text='CCS School Atrauli (Aligarh)',font=('Segoe UI',12,'bold'),bg=COLORS['bg'],fg=COLORS['blue_dark']).place(x=40,y=465)


if __name__ == '__main__':
    root=Tk(); about(root); root.mainloop()
