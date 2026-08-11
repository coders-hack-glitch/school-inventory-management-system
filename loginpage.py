from pathlib import Path
from tkinter import Tk, Toplevel, StringVar, Label, Entry, Button, Frame, messagebox, OptionMenu
from PIL import Image, ImageTk
import hashlib
import json
import os
import tempfile

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / 'users.json'


class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title('Inventory Management System - Login')
        self.root.geometry('1200x720+80+20')
        self.root.configure(bg='#eef3f8')
        self.root.resizable(False, False)

        self.primary = '#0b8fc4'
        self.primary_dark = '#076b94'
        self.text = '#253746'
        self.muted = '#6d7b88'
        self.card = '#ffffff'

        # ---------- Main layout ----------
        self.left = Frame(self.root, bg='#123e5a', width=610, height=720)
        self.left.pack(side='left', fill='y')
        self.left.pack_propagate(False)

        self.right = Frame(self.root, bg='#eef3f8', width=590, height=720)
        self.right.pack(side='right', fill='both', expand=True)
        self.right.pack_propagate(False)

        # Left branding section
        Label(
            self.left,
            text='INVENTORY',
            font=('Segoe UI', 30, 'bold'),
            bg='#123e5a', fg='white'
        ).place(x=45, y=38)
        Label(
            self.left,
            text='MANAGEMENT SYSTEM',
            font=('Segoe UI', 16, 'bold'),
            bg='#123e5a', fg='#7fd8f5'
        ).place(x=47, y=82)
        Label(
            self.left,
            text='Manage products, stock and sales\nfrom one simple dashboard.',
            font=('Segoe UI', 12),
            justify='left',
            bg='#123e5a', fg='#dcebf3'
        ).place(x=48, y=125)

        self.image_holder = Frame(self.left, bg='white', width=500, height=360)
        self.image_holder.place(x=55, y=215)
        self.image_holder.pack_propagate(False)

        self.im1 = self.load_image('Image 2.png', (480, 340))
        self.im2 = self.load_image('Image 3.png', (480, 340))
        self.im3 = self.load_image('Image 4.png', (480, 340))
        self.lbl_change_image = Label(self.image_holder, bg='white', bd=0)
        self.lbl_change_image.pack(expand=True)
        self.animate()

        Label(
            self.left,
            text='Simple • Fast • Organized',
            font=('Segoe UI', 11, 'bold'),
            bg='#123e5a', fg='#b9d8e7'
        ).place(x=48, y=650)

        # Right login card
        self.login_card = Frame(self.right, bg=self.card, highlightbackground='#d8e0e7', highlightthickness=1)
        self.login_card.place(x=95, y=72, width=400, height=575)

        Label(
            self.login_card,
            text='Welcome Back',
            font=('Segoe UI', 26, 'bold'),
            bg='white', fg=self.text
        ).place(x=40, y=38)
        Label(
            self.login_card,
            text='Sign in to continue to your inventory dashboard',
            font=('Segoe UI', 10),
            bg='white', fg=self.muted
        ).place(x=40, y=82)

        Label(self.login_card, text='Username', font=('Segoe UI', 11, 'bold'), bg='white', fg=self.text).place(x=40, y=135)
        self.username = StringVar()
        self.username_entry = Entry(
            self.login_card, textvariable=self.username, font=('Segoe UI', 12),
            bg='#f5f8fa', fg=self.text, relief='flat', highlightthickness=1,
            highlightbackground='#d6e0e7', highlightcolor=self.primary
        )
        self.username_entry.place(x=40, y=165, width=320, height=40)

        Label(self.login_card, text='Password', font=('Segoe UI', 11, 'bold'), bg='white', fg=self.text).place(x=40, y=225)
        self.password = StringVar()
        self.password_entry = Entry(
            self.login_card, textvariable=self.password, show='*', font=('Segoe UI', 12),
            bg='#f5f8fa', fg=self.text, relief='flat', highlightthickness=1,
            highlightbackground='#d6e0e7', highlightcolor=self.primary
        )
        self.password_entry.place(x=40, y=255, width=320, height=40)

        Button(
            self.login_card, text='LOGIN', font=('Segoe UI', 12, 'bold'),
            bg=self.primary, fg='white', activebackground=self.primary_dark,
            activeforeground='white', relief='flat', bd=0, cursor='hand2',
            command=self.login
        ).place(x=40, y=320, width=320, height=44)

        Button(
            self.login_card, text='Forgot Password?', font=('Segoe UI', 10, 'bold'),
            bg='white', fg=self.primary_dark, activebackground='white',
            activeforeground=self.primary, relief='flat', bd=0, cursor='hand2',
            command=self.forgot_password
        ).place(x=120, y=382, width=160, height=28)

        Frame(self.login_card, bg='#dbe3e9', height=1, width=135).place(x=40, y=430)
        Label(self.login_card, text='OR', font=('Segoe UI', 10, 'bold'), bg='white', fg=self.muted).place(x=185, y=416, width=30)
        Frame(self.login_card, bg='#dbe3e9', height=1, width=135).place(x=225, y=430)

        Label(
            self.login_card, text="Don't have an account?",
            font=('Segoe UI', 10), bg='white', fg=self.muted
        ).place(x=75, y=468)
        Button(
            self.login_card, text='CREATE NEW ACCOUNT',
            font=('Segoe UI', 10, 'bold'), bg='white', fg=self.primary_dark,
            activebackground='white', activeforeground=self.primary,
            relief='flat', bd=0, cursor='hand2', command=self.open_register
        ).place(x=215, y=462, width=145, height=32)

        self.username_entry.focus_set()
        self.root.bind('<Return>', lambda event: self.login())

    def load_image(self, filename, size):
        image = Image.open(BASE_DIR / filename).convert('RGB')
        image.thumbnail(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2500, self.animate)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def load_users(self):
        if not USERS_FILE.exists():
            default = {
                'Shreshth': {
                    'password': self.hash_password('123456'),
                    'question': 'What is your favourite color?',
                    'answer': self.hash_password('blue')
                }
            }
            USERS_FILE.write_text(json.dumps(default, indent=4), encoding='utf-8')
            return default
        try:
            data = json.loads(USERS_FILE.read_text(encoding='utf-8'))
            if not isinstance(data, dict):
                return {}

            # Convert accounts created by the previous version (where the
            # value was only a password hash) into the new account format.
            changed = False
            for username, value in list(data.items()):
                if isinstance(value, str):
                    data[username] = {
                        'password': value,
                        'question': '',
                        'answer': ''
                    }
                    changed = True
            if changed:
                self.save_users(data)
            return data
        except (json.JSONDecodeError, OSError):
            return {}

    def save_users(self, users):
        # Write atomically so a password change cannot be lost because of a
        # partial/failed write. The next login always reads the saved file.
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(users, indent=4, ensure_ascii=False)
        fd, temp_name = tempfile.mkstemp(prefix='users_', suffix='.tmp', dir=str(USERS_FILE.parent))
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as temp_file:
                temp_file.write(payload)
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.replace(temp_name, USERS_FILE)
        except Exception:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise

    def verify_password(self, username, password):
        # Always reload the file from disk. Do not keep an old password in memory.
        users = self.load_users()
        account = users.get(username)
        if not isinstance(account, dict):
            return False
        stored_hash = account.get('password', '')
        if not isinstance(stored_hash, str) or not stored_hash:
            return False
        return stored_hash == self.hash_password(password)

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()

        if not username or not password:
            messagebox.showerror('Login Error', 'Please enter both username and password.', parent=self.root)
            return

        # Password verification always reads the latest saved password.
        if self.verify_password(username, password):
            messagebox.showinfo('Login Successful', f'Welcome, {username}!', parent=self.root)
            self.open_dashboard()
        else:
            messagebox.showerror('Login Error', 'Invalid username or password.', parent=self.root)

    def forgot_password(self):
        ForgotPasswordWindow(self.root, self)

    def open_register(self):
        RegisterWindow(self.root, self)

    def open_dashboard(self):
        self.root.destroy()
        dashboard = Tk()
        from dashboard import IMS
        IMS(dashboard)
        dashboard.mainloop()


class RegisterWindow:
    def __init__(self, parent, login_window):
        self.parent = parent
        self.login_window = login_window
        self.window = Toplevel(parent)
        self.window.title('Create New Account')
        self.window.geometry('470x620+430+50')
        self.window.configure(bg='#eef3f8')
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        card = Frame(self.window, bg='white', highlightbackground='#d8e0e7', highlightthickness=1)
        card.place(x=35, y=20, width=400, height=575)

        Label(card, text='Create Account', font=('Segoe UI', 25, 'bold'), bg='white', fg='#253746').place(x=35, y=28)
        Label(card, text='Create your login for the inventory system', font=('Segoe UI', 10), bg='white', fg='#6d7b88').place(x=35, y=70)

        self.username = StringVar()
        self.password = StringVar()
        self.confirm = StringVar()
        self.question = StringVar(value='What is your favourite color?')
        self.answer = StringVar()

        self.add_field(card, 'Username', self.username, 120)
        self.add_field(card, 'Password', self.password, 200, show='*')
        self.add_field(card, 'Confirm Password', self.confirm, 280, show='*')

        Label(card, text='Security Question', font=('Segoe UI', 10, 'bold'), bg='white', fg='#253746').place(x=35, y=355)
        OptionMenu(
            card, self.question,
            'What is your favourite color?',
            'What is your favourite food?',
            'What is the name of your first school?'
        ).place(x=35, y=382, width=330, height=30)
        Label(card, text='Security Answer', font=('Segoe UI', 10, 'bold'), bg='white', fg='#253746').place(x=35, y=420)
        Entry(card, textvariable=self.answer, font=('Segoe UI', 11), bg='#f5f8fa', fg='#253746', relief='flat', highlightthickness=1, highlightbackground='#d6e0e7', highlightcolor='#0b8fc4').place(x=35, y=446, width=330, height=32)

        Button(
            card, text='CREATE ACCOUNT', font=('Segoe UI', 11, 'bold'),
            bg='#0b8fc4', fg='white', activebackground='#076b94', activeforeground='white',
            relief='flat', bd=0, cursor='hand2', command=self.register
        ).place(x=35, y=495, width=330, height=44)

        Button(
            card, text='Cancel', font=('Segoe UI', 10, 'bold'), bg='white', fg='#0b6f98',
            activebackground='white', relief='flat', bd=0, cursor='hand2', command=self.window.destroy
        ).place(x=150, y=545, width=100, height=30)

    def add_field(self, parent, label, variable, y, show=None):
        Label(parent, text=label, font=('Segoe UI', 11, 'bold'), bg='white', fg='#253746').place(x=35, y=y)
        entry = Entry(
            parent, textvariable=variable, font=('Segoe UI', 12), show=show or '',
            bg='#f5f8fa', fg='#253746', relief='flat', highlightthickness=1,
            highlightbackground='#d6e0e7', highlightcolor='#0b8fc4'
        )
        entry.place(x=35, y=y + 28, width=330, height=38)

    def register(self):
        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm.get()

        answer = self.answer.get().strip()

        if not username or not password or not confirm or not answer:
            messagebox.showerror('Registration Error', 'Please fill all fields, including the security answer.', parent=self.window)
            return
        if len(username) < 3:
            messagebox.showerror('Registration Error', 'Username must contain at least 3 characters.', parent=self.window)
            return
        if len(password) < 6:
            messagebox.showerror('Registration Error', 'Password must contain at least 6 characters.', parent=self.window)
            return
        if password != confirm:
            messagebox.showerror('Registration Error', 'Passwords do not match.', parent=self.window)
            return

        users = self.login_window.load_users()
        if username in users:
            messagebox.showerror('Registration Error', 'That username already exists.', parent=self.window)
            return

        users[username] = {
            'password': self.login_window.hash_password(password),
            'question': self.question.get(),
            'answer': self.login_window.hash_password(answer.lower())
        }
        self.login_window.save_users(users)
        self.login_window.username.set(username)
        self.login_window.password.set('')
        messagebox.showinfo('Account Created', 'Your account has been created successfully. You can now log in.', parent=self.window)
        self.window.destroy()
        self.login_window.password_entry.focus_set()


class ForgotPasswordWindow:
    QUESTIONS = [
        'What is your favourite color?',
        'What is your favourite food?',
        'What is the name of your first school?'
    ]

    def __init__(self, parent, login_window):
        self.login_window = login_window
        self.window = Toplevel(parent)
        self.window.title('Forgot Password')
        self.window.geometry('500x610+420+55')
        self.window.configure(bg='#eef3f8')
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self.username = StringVar()
        self.answer = StringVar()
        self.new_password = StringVar()
        self.confirm_password = StringVar()
        self.question = StringVar(value='')

        self.card = Frame(self.window, bg='white', highlightbackground='#d8e0e7', highlightthickness=1)
        self.card.place(x=35, y=25, width=430, height=555)

        Label(self.card, text='Reset Password', font=('Segoe UI', 25, 'bold'), bg='white', fg='#253746').place(x=35, y=30)
        Label(self.card, text='Verify your account and choose a new password', font=('Segoe UI', 10), bg='white', fg='#6d7b88').place(x=35, y=72)

        self.add_label('Username', 115)
        Entry(self.card, textvariable=self.username, font=('Segoe UI', 12), bg='#f5f8fa', relief='flat', highlightthickness=1, highlightbackground='#d6e0e7').place(x=35, y=143, width=280, height=38)
        Button(self.card, text='FIND ACCOUNT', font=('Segoe UI', 9, 'bold'), bg='#0b8fc4', fg='white', activebackground='#076b94', relief='flat', bd=0, cursor='hand2', command=self.find_account).place(x=325, y=143, width=70, height=38)

        self.question_label = Label(self.card, text='Security question will appear here', font=('Segoe UI', 10, 'bold'), wraplength=350, justify='left', bg='white', fg='#253746')
        self.question_label.place(x=35, y=205, width=360, height=45)

        self.add_label('Security Answer', 265)
        self.answer_entry = Entry(self.card, textvariable=self.answer, font=('Segoe UI', 11), bg='#f5f8fa', relief='flat', highlightthickness=1, highlightbackground='#d6e0e7')
        self.answer_entry.place(x=35, y=293, width=360, height=38)

        self.add_label('New Password', 345)
        self.new_entry = Entry(self.card, textvariable=self.new_password, show='*', font=('Segoe UI', 11), bg='#f5f8fa', relief='flat', highlightthickness=1, highlightbackground='#d6e0e7')
        self.new_entry.place(x=35, y=373, width=360, height=38)

        self.add_label('Confirm New Password', 425)
        self.confirm_entry = Entry(self.card, textvariable=self.confirm_password, show='*', font=('Segoe UI', 11), bg='#f5f8fa', relief='flat', highlightthickness=1, highlightbackground='#d6e0e7')
        self.confirm_entry.place(x=35, y=453, width=360, height=38)

        Button(self.card, text='RESET PASSWORD', font=('Segoe UI', 11, 'bold'), bg='#0b8fc4', fg='white', activebackground='#076b94', relief='flat', bd=0, cursor='hand2', command=self.reset_password).place(x=35, y=505, width=360, height=40)

        self.set_recovery_enabled(False)

    def add_label(self, text, y):
        Label(self.card, text=text, font=('Segoe UI', 10, 'bold'), bg='white', fg='#253746').place(x=35, y=y)

    def set_recovery_enabled(self, enabled):
        state = 'normal' if enabled else 'disabled'
        self.answer_entry.config(state=state)
        self.new_entry.config(state=state)
        self.confirm_entry.config(state=state)

    def find_account(self):
        username = self.username.get().strip()
        if not username:
            messagebox.showerror('Forgot Password', 'Enter your username first.', parent=self.window)
            return

        users = self.login_window.load_users()
        account = users.get(username)
        if not isinstance(account, dict):
            messagebox.showerror('Forgot Password', 'This account uses the older login format and has no security question. Create a new account or contact the administrator.', parent=self.window)
            return

        question = account.get('question', '')
        answer_hash = account.get('answer', '')
        if not question or not answer_hash:
            messagebox.showerror('Forgot Password', 'Security recovery is not configured for this account. Create a new account or contact the administrator.', parent=self.window)
            return

        self.question.set(question)
        self.question_label.config(text='Security Question: ' + question)
        self.set_recovery_enabled(True)
        self.answer_entry.focus_set()

    def reset_password(self):
        username = self.username.get().strip()
        answer = self.answer.get().strip()
        new_password = self.new_password.get()
        confirm = self.confirm_password.get()

        if not username:
            messagebox.showerror('Forgot Password', 'Enter your username.', parent=self.window)
            return
        if not self.question.get():
            messagebox.showerror('Forgot Password', 'Click FIND ACCOUNT first.', parent=self.window)
            return
        if not answer or not new_password or not confirm:
            messagebox.showerror('Forgot Password', 'Please fill the answer and both new password fields.', parent=self.window)
            return
        if len(new_password) < 6:
            messagebox.showerror('Forgot Password', 'New password must contain at least 6 characters.', parent=self.window)
            return
        if new_password != confirm:
            messagebox.showerror('Forgot Password', 'New passwords do not match.', parent=self.window)
            return

        users = self.login_window.load_users()
        account = users.get(username)
        if not isinstance(account, dict):
            messagebox.showerror('Forgot Password', 'Account recovery is not available for this account.', parent=self.window)
            return

        expected = account.get('answer', '')
        actual = self.login_window.hash_password(answer.lower())
        if actual != expected:
            messagebox.showerror('Forgot Password', 'Incorrect security answer.', parent=self.window)
            return

        # Capture the previous hash so we can make sure the old credential is
        # actually replaced, not merely append a new value.
        old_password_hash = account.get('password', '')
        new_password_hash = self.login_window.hash_password(new_password)
        account['password'] = new_password_hash
        users[username] = account

        try:
            self.login_window.save_users(users)
            saved_users = self.login_window.load_users()
            saved_account = saved_users.get(username, {})
            saved_hash = saved_account.get('password', '') if isinstance(saved_account, dict) else ''

            if saved_hash != new_password_hash:
                raise RuntimeError('The new password was not saved correctly.')
            if saved_hash == old_password_hash:
                raise RuntimeError('The old password is still stored.')
        except Exception as exc:
            messagebox.showerror('Password Reset', f'Password reset could not be completed:\n\n{exc}', parent=self.window)
            return

        self.login_window.username.set(username)
        self.login_window.password.set('')
        messagebox.showinfo('Password Reset', 'Password reset successfully. The old password is no longer valid. You can now log in with your new password.', parent=self.window)
        self.window.destroy()
        self.login_window.password_entry.focus_set()


if __name__ == '__main__':
    root = Tk()
    Login_System(root)
    root.mainloop()
