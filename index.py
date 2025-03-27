import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import webbrowser

# Color Palette
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#34495e"
ACCENT_COLOR = "#3498db"
LIGHT_COLOR = "#ecf0f1"
DARK_COLOR = "#2c3e50"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#e74c3c"
INFO_COLOR = "#3498db"

# Fonts
HEADING_FONT = ("Roboto", 18, "bold")
LABEL_FONT = ("Open Sans", 12)
ENTRY_FONT = ("Open Sans", 11)
BUTTON_FONT = ("Open Sans", 10, "bold")

# Connecting to the Database
connector = sqlite3.connect("Expense_Tracker.db")
cursor = connector.cursor()

connector.execute(
    'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
)
connector.commit()

# Functions
def list_all_expenses():
    global connector, table

    table.delete(*table.get_children())

    all_data = connector.execute('SELECT * FROM ExpenseTracker')
    data = all_data.fetchall()

    for values in data:
        table.insert('', END, values=values)

def view_expense_details():
    global table
    global date, payee, desc, amnt, MoP

    if not table.selection():
        mb.showerror('No expense selected', 'Please select an expense from the table to view its details')
        return

    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']

    expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))

    date.set_date(expenditure_date)
    payee.set(values[2])
    desc.set(values[3])
    amnt.set(values[4])
    MoP.set(values[5])

def clear_fields():
    global desc, payee, amnt, MoP, date, table

    today_date = datetime.datetime.now().date()

    desc.set('')
    payee.set('')
    amnt.set(0.0)
    MoP.set('Cash')
    date.set_date(today_date)
    table.selection_remove(*table.selection())

def remove_expense():
    if not table.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return

    current_selected_expense = table.item(table.focus())
    values_selected = current_selected_expense['values']

    surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')

    if surety:
        connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
        connector.commit()

        list_all_expenses()
        mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

def remove_all_expenses():
    surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')

    if surety:
        table.delete(*table.get_children())

        connector.execute('DELETE FROM ExpenseTracker')
        connector.commit()

        clear_fields()
        list_all_expenses()
        mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
    else:
        mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')

def add_another_expense():
    global date, payee, desc, amnt, MoP
    global connector

    if not date.get() or not payee.get() or not desc.get() or not amnt.get() or not MoP.get():
        mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
    else:
        connector.execute(
            'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
            (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get())
        )
        connector.commit()

        clear_fields()
        list_all_expenses()
        mb.showinfo('Expense added', 'The expense has been added to the database')

def edit_expense():
    global table

    def edit_existing_expense():
        global date, amnt, desc, payee, MoP
        global connector, table

        current_selected_expense = table.item(table.focus())
        contents = current_selected_expense['values']

        connector.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
                          (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get(), contents[0]))
        connector.commit()

        clear_fields()
        list_all_expenses()

        mb.showinfo('Data edited', 'The data has been updated in the database')
        edit_btn.destroy()
        return

    if not table.selection():
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
        return

    view_expense_details()

    edit_btn = Button(data_entry_frame, text='CONFIRM EDIT', font=BUTTON_FONT, width=20,
                      bg=SUCCESS_COLOR, fg="white", command=edit_existing_expense)
    edit_btn.place(x=20, y=400)

def selected_expense_to_words():
    global table

    if not table.selection():
        mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
        return

    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']

    message = f'Your expense can be read like: \n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'

    mb.showinfo('Expense Summary', message)

def expense_to_words_before_adding():
    global date, desc, amnt, payee, MoP

    if not date.get() or not desc.get() or not amnt.get() or not payee.get() or not MoP.get():
        mb.showerror('Incomplete data', 'The data is incomplete, please fill all the fields first!')
        return

    message = f'Your expense can be read like: \n"You paid {amnt.get()} to {payee.get()} for {desc.get()} on {date.get_date()} via {MoP.get()}"'

    add_question = mb.askyesno('Confirm Expense', f'{message}\n\nShould I add it to the database?')

    if add_question:
        add_another_expense()

def open_help():
    mb.showinfo("Help", "1. Fill all fields to add an expense\n2. Select an expense to view/edit/delete\n3. Use 'Convert to words' to review before adding")

def open_about():
    mb.showinfo("About", "Expense Tracker v2.0\n\nA modern application to track your daily expenses\n\nDeveloped with Python and Tkinter")

def open_website():
    webbrowser.open("https://www.python.org")

# Initializing the GUI window
root = Tk()
root.title('Expense Tracker Pro')
root.geometry('1200x650')
root.resizable(0, 0)
root.configure(bg=LIGHT_COLOR)

# Custom title bar
title_frame = Frame(root, bg=PRIMARY_COLOR)
title_frame.pack(side=TOP, fill=X)

Label(title_frame, text='EXPENSE TRACKER PRO', font=HEADING_FONT, bg=PRIMARY_COLOR, fg="white").pack(side=LEFT, padx=10, pady=10)

# Menu Bar
menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Clear All", command=clear_fields)
file_menu.add_command(label="Exit", command=root.quit)

help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=open_help)
help_menu.add_command(label="About", command=open_about)
help_menu.add_command(label="Visit Python", command=open_website)

# StringVar and DoubleVar variables
desc = StringVar()
amnt = DoubleVar()
payee = StringVar()
MoP = StringVar(value='Cash')

# Frames
data_entry_frame = Frame(root, bg=LIGHT_COLOR, bd=2, relief=GROOVE)
data_entry_frame.place(x=20, y=60, width=300, height=580)

buttons_frame = Frame(root, bg=LIGHT_COLOR, bd=2, relief=GROOVE)
buttons_frame.place(x=340, y=60, width=830, height=100)

tree_frame = Frame(root, bg=LIGHT_COLOR, bd=2, relief=GROOVE)
tree_frame.place(x=340, y=180, width=830, height=460)

# Data Entry Frame
Label(data_entry_frame, text='ADD NEW EXPENSE', font=("Roboto", 14, "bold"), bg=LIGHT_COLOR).pack(pady=10)

# Date
date_frame = Frame(data_entry_frame, bg=LIGHT_COLOR)
date_frame.pack(pady=5, padx=10, fill=X)
Label(date_frame, text='Date:', font=LABEL_FONT, bg=LIGHT_COLOR).pack(side=LEFT)
date = DateEntry(date_frame, date=datetime.datetime.now().date(), font=ENTRY_FONT,
                background=PRIMARY_COLOR, foreground='white', borderwidth=2)
date.pack(side=RIGHT, fill=X, expand=True)

# Payee
payee_frame = Frame(data_entry_frame, bg=LIGHT_COLOR)
payee_frame.pack(pady=5, padx=10, fill=X)
Label(payee_frame, text='Payee:', font=LABEL_FONT, bg=LIGHT_COLOR).pack(side=LEFT)
Entry(payee_frame, font=ENTRY_FONT, width=25, textvariable=payee, bd=2).pack(side=RIGHT, fill=X, expand=True)

# Description
desc_frame = Frame(data_entry_frame, bg=LIGHT_COLOR)
desc_frame.pack(pady=5, padx=10, fill=X)
Label(desc_frame, text='Description:', font=LABEL_FONT, bg=LIGHT_COLOR).pack(side=LEFT)
Entry(desc_frame, font=ENTRY_FONT, width=25, textvariable=desc, bd=2).pack(side=RIGHT, fill=X, expand=True)

# Amount
amount_frame = Frame(data_entry_frame, bg=LIGHT_COLOR)
amount_frame.pack(pady=5, padx=10, fill=X)
Label(amount_frame, text='Amount:', font=LABEL_FONT, bg=LIGHT_COLOR).pack(side=LEFT)
Entry(amount_frame, font=ENTRY_FONT, width=15, textvariable=amnt, bd=2).pack(side=RIGHT, fill=X, expand=True)

# Mode of Payment
mop_frame = Frame(data_entry_frame, bg=LIGHT_COLOR)
mop_frame.pack(pady=5, padx=10, fill=X)
Label(mop_frame, text='Payment Mode:', font=LABEL_FONT, bg=LIGHT_COLOR).pack(side=LEFT)
dd1 = OptionMenu(mop_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
dd1.config(font=ENTRY_FONT, bg=PRIMARY_COLOR, fg="white", activebackground=ACCENT_COLOR, bd=2)
dd1.pack(side=RIGHT, fill=X, expand=True)

# Buttons in Data Entry Frame
Button(data_entry_frame, text='Add Expense', command=add_another_expense, font=BUTTON_FONT,
       bg=SUCCESS_COLOR, fg="white", width=20).pack(pady=10)

Button(data_entry_frame, text='Preview Expense', command=expense_to_words_before_adding, font=BUTTON_FONT,
       bg=INFO_COLOR, fg="white", width=20).pack(pady=5)

Button(data_entry_frame, text='Clear Fields', command=clear_fields, font=BUTTON_FONT,
       bg=WARNING_COLOR, fg="white", width=20).pack(pady=10)

# Buttons' Frame
Button(buttons_frame, text='Delete Selected', font=BUTTON_FONT, width=20,
       bg=WARNING_COLOR, fg="white", command=remove_expense).place(x=20, y=20)

Button(buttons_frame, text='View Details', font=BUTTON_FONT, width=20,
       bg=INFO_COLOR, fg="white", command=view_expense_details).place(x=200, y=20)

Button(buttons_frame, text='Edit Selected', command=edit_expense, font=BUTTON_FONT, width=20,
       bg=SUCCESS_COLOR, fg="white").place(x=380, y=20)

Button(buttons_frame, text='Delete All Expenses', font=BUTTON_FONT, width=20,
       bg=WARNING_COLOR, fg="white", command=remove_all_expenses).place(x=560, y=20)

Button(buttons_frame, text='Expense Summary', font=BUTTON_FONT, width=20,
       bg=INFO_COLOR, fg="white", command=selected_expense_to_words).place(x=380, y=60)

# Treeview Frame
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background=LIGHT_COLOR,
                foreground=DARK_COLOR,
                rowheight=25,
                fieldbackground=LIGHT_COLOR,
                font=("Open Sans", 10))
style.map('Treeview', background=[('selected', ACCENT_COLOR)])

style.configure("Treeview.Heading",
                background=PRIMARY_COLOR,
                foreground="white",
                font=("Open Sans", 11, "bold"))

table = ttk.Treeview(tree_frame, selectmode=BROWSE,
                     columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'))

X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='ID', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Payment Mode', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=100, stretch=NO)  # Date column
table.column('#3', width=150, stretch=NO)  # Payee column
table.column('#4', width=250, stretch=NO)  # Description column
table.column('#5', width=100, stretch=NO)  # Amount column
table.column('#6', width=150, stretch=NO)  # Mode of Payment column

table.pack(fill=BOTH, expand=1)

# Status Bar
status = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W, font=("Open Sans", 10))
status.pack(side=BOTTOM, fill=X)

# Initialize
list_all_expenses()

# Finalizing the GUI window
root.update()
root.mainloop()