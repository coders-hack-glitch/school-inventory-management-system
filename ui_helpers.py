from tkinter import *
from tkinter import ttk

COLORS = {
    'navy': '#123E5A',
    'blue': '#0B8FC4',
    'blue_dark': '#076B94',
    'bg': '#F3F7FA',
    'card': '#FFFFFF',
    'text': '#253746',
    'muted': '#6D7B88',
    'border': '#D8E2E8',
    'success': '#1F9D67',
    'danger': '#D9534F',
    'warning': '#E89B24',
    'soft_blue': '#E7F4FA',
    'soft_green': '#E8F7F0',
    'soft_red': '#FCEDEC',
    'soft_orange': '#FFF4E2',
}


def center_window(window, width, height):
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = max((screen_w - width) // 2, 0)
    y = max((screen_h - height) // 2, 0)
    window.geometry(f'{width}x{height}+{x}+{y}')


def setup_window(window, title, geometry='1120x700'):
    window.title(title)
    window.configure(bg=COLORS['bg'])
    window.resizable(False, False)
    try:
        width, height = (int(v) for v in geometry.split('x')[0:2])
    except Exception:
        width, height = 1120, 700
    center_window(window, width, height)


def add_header(parent, title, subtitle=None):
    header = Frame(parent, bg=COLORS['bg'], height=88)
    header.pack(fill='x')
    header.pack_propagate(False)

    Label(
        header,
        text=title,
        font=('Segoe UI', 24, 'bold'),
        bg=COLORS['bg'],
        fg=COLORS['text']
    ).pack(anchor='w', padx=36, pady=(20, 0))

    if subtitle:
        Label(
            header,
            text=subtitle,
            font=('Segoe UI', 10),
            bg=COLORS['bg'],
            fg=COLORS['muted']
        ).pack(anchor='w', padx=38, pady=(3, 0))

    return header


def card(parent, width=None, height=None, bg=None):
    frame = Frame(
        parent,
        bg=bg or COLORS['card'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )

    if width or height:
        frame.configure(
            width=width or 1,
            height=height or 1
        )
        frame.pack_propagate(False)

    return frame


def styled_entry(parent, variable=None, width=30, show=None):
    entry = Entry(
        parent,
        textvariable=variable,
        width=width,
        show=show,
        font=('Segoe UI', 11),
        bg='#F7FAFC',
        fg=COLORS['text'],
        relief='flat',
        highlightthickness=1,
        highlightbackground=COLORS['border'],
        highlightcolor=COLORS['blue']
    )

    return entry


def button(parent, text, command, kind='primary', width=16):
    palette = {
        'primary': (
            COLORS['blue'],
            COLORS['blue_dark'],
            'white'
        ),
        'success': (
            COLORS['success'],
            '#17784F',
            'white'
        ),
        'danger': (
            COLORS['danger'],
            '#B83E3A',
            'white'
        ),
        'warning': (
            COLORS['warning'],
            '#C27A0E',
            'white'
        ),
        'secondary': (
            '#E8EEF2',
            '#D8E2E8',
            COLORS['text']
        ),
        'dark': (
            COLORS['navy'],
            '#0D2F45',
            'white'
        ),
    }

    bg, active, fg = palette[kind]

    return Button(
        parent,
        text=text,
        command=command,
        width=width,
        font=('Segoe UI', 10, 'bold'),
        bg=bg,
        fg=fg,
        activebackground=active,
        activeforeground=fg,
        relief='flat',
        bd=0,
        cursor='hand2'
    )


def configure_treeview_style():
    style = ttk.Style()

    try:
        style.theme_use('clam')
    except Exception:
        pass

    style.configure(
        'Modern.Treeview',
        background='white',
        foreground=COLORS['text'],
        rowheight=34,
        fieldbackground='white',
        font=('Segoe UI', 10),
        borderwidth=0
    )

    style.configure(
        'Modern.Treeview.Heading',
        background=COLORS['navy'],
        foreground='white',
        font=('Segoe UI', 10, 'bold'),
        relief='flat'
    )

    style.map(
        'Modern.Treeview',
        background=[('selected', '#DCEFF7')],
        foreground=[('selected', COLORS['text'])]
    )

    return style