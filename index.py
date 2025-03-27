import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

# Theme Colors - Light Mode
LIGHT_THEME = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'bg': '#ecf0f1',
    'text': '#2c3e50',
    'entry_bg': 'white',
    'entry_fg': 'black',
    'button_bg': '#3498db',
    'button_fg': 'white',
    'success': '#2ecc71',
    'warning': '#e74c3c',
    'info': '#3498db'
}

# Theme Colors - Dark Mode
DARK_THEME = {
    'primary': '#212121',
    'secondary': '#424242',
    'accent': '#1976D2',
    'bg': '#121212',
    'text': '#E0E0E0',
    'entry_bg': '#424242',
    'entry_fg': 'white',
    'button_bg': '#1976D2',
    'button_fg': 'white',
    'success': '#388E3C',
    'warning': '#D32F2F',
    'info': '#1976D2'
}

# Current theme and fullscreen state
current_theme = LIGHT_THEME
is_fullscreen = False

# Functions
def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)
    if not is_fullscreen:
        root.geometry('1200x650')

def maximize_window():
    root.state('zoomed')

def toggle_theme():
    global current_theme
    if current_theme == LIGHT_THEME:
        current_theme = DARK_THEME
        theme_btn.config(text='☀️ Light Mode')
    else:
        current_theme = LIGHT_THEME
        theme_btn.config(text='🌙 Dark Mode')
    apply_theme()

def apply_theme():
    root.config(bg=current_theme['bg'])
    title_frame.config(bg=current_theme['primary'])
    title_label.config(bg=current_theme['primary'], fg='white')
    data_entry_frame.config(bg=current_theme['bg'])
    buttons_frame.config(bg=current_theme['bg'])
    tree_frame.config(bg=current_theme['bg'])
    status.config(bg=current_theme['secondary'], fg='white')

    for widget in data_entry_frame.winfo_children():
        if isinstance(widget, (Label, Frame)):
            widget.config(bg=current_theme['bg'], fg=current_theme['text'])
        elif isinstance(widget, Entry):
            widget.config(bg=current_theme['entry_bg'], fg=current_theme['entry_fg'])

# Initialize the GUI window
root = Tk()
root.title('Expense Tracker')
root.geometry('1200x650')
root.resizable(1, 1)  # Allow resizing

# Title bar with controls
title_frame = Frame(root, bg=current_theme['primary'])
title_frame.pack(side=TOP, fill=X)

title_label = Label(title_frame, text='EXPENSE TRACKER', font=("Roboto", 14, "bold"),
                   bg=current_theme['primary'], fg="white")
title_label.pack(side=LEFT, padx=10, pady=10)

# Window control buttons
control_buttons = Frame(title_frame, bg=current_theme['primary'])
control_buttons.pack(side=RIGHT, padx=5)

theme_btn = Button(control_buttons, text='🌙 Dark Mode', font=("Arial", 8),
                  command=toggle_theme, bd=0, highlightthickness=0)
theme_btn.pack(side=LEFT, padx=2)

maximize_btn = Button(control_buttons, text='🗖', font=("Arial", 10),
                     command=maximize_window, bd=0, highlightthickness=0)
maximize_btn.pack(side=LEFT, padx=2)

fullscreen_btn = Button(control_buttons, text='⛶', font=("Arial", 10),
                       command=toggle_fullscreen, bd=0, highlightthickness=0)
fullscreen_btn.pack(side=LEFT, padx=2)

# Main application frames
data_entry_frame = Frame(root, bg=current_theme['bg'], bd=2, relief=GROOVE)
data_entry_frame.place(x=20, y=60, width=300, height=580)

buttons_frame = Frame(root, bg=current_theme['bg'], bd=2, relief=GROOVE)
buttons_frame.place(x=340, y=60, width=830, height=100)

tree_frame = Frame(root, bg=current_theme['bg'], bd=2, relief=GROOVE)
tree_frame.place(x=340, y=180, width=830, height=460)

# Data Entry Frame Content
Label(data_entry_frame, text='ADD NEW EXPENSE', font=("Roboto", 14, "bold"),
     bg=current_theme['bg'], fg=current_theme['text']).pack(pady=10)

# Date Frame
date_frame = Frame(data_entry_frame, bg=current_theme['bg'])
date_frame.pack(pady=5, padx=10, fill=X)
Label(date_frame, text='Date:', font=("Open Sans", 12), bg=current_theme['bg']).pack(side=LEFT)
date = DateEntry(date_frame, date=datetime.datetime.now().date(), font=("Open Sans", 11),
                background=current_theme['primary'], foreground='white', borderwidth=2)
date.pack(side=RIGHT, fill=X, expand=True)

# [Add other data entry widgets here...]

# Buttons Frame Content
Button(buttons_frame, text='Add Expense', font=("Open Sans", 10, "bold"),
      bg=current_theme['success'], fg="white", width=15).place(x=20, y=20)

Button(buttons_frame, text='Delete Expense', font=("Open Sans", 10, "bold"),
      bg=current_theme['warning'], fg="white", width=15).place(x=180, y=20)

# [Add other control buttons here...]

# Treeview Frame Content
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
               background=current_theme['bg'],
               foreground=current_theme['text'],
               rowheight=25,
               fieldbackground=current_theme['bg'],
               font=("Open Sans", 10))
style.map('Treeview', background=[('selected', current_theme['accent'])])

style.configure("Treeview.Heading",
               background=current_theme['primary'],
               foreground="white",
               font=("Open Sans", 11, "bold"))

table = ttk.Treeview(tree_frame, selectmode=BROWSE,
                    columns=('ID', 'Date', 'Description', 'Amount', 'Category'))

# [Configure treeview columns and headings...]

# Status bar
status = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W,
              font=("Open Sans", 10), bg=current_theme['secondary'], fg='white')
status.pack(side=BOTTOM, fill=X)

# Apply initial theme
apply_theme()

# Keyboard shortcut for F11 fullscreen
root.bind('<F11>', lambda e: toggle_fullscreen())

root.mainloop()