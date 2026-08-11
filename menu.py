from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent


class menu:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1366x680+50+75')
        self.root.title('Menu')
        self.root.config(bg='white')
        self.root.resizable(False, False)
        image = Image.open(BASE_DIR / 'dashboard.png').convert('RGB').resize((1366, 680), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        frame = Frame(self.root, bg='white'); frame.place(x=0, y=0, relwidth=1, relheight=1)
        Label(frame, image=self.photo, bd=0).pack()
