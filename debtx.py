import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class Debt(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")
       
        self.initialize_db()
        self.initialize_gui()
        self.display_data()
        
    def initialize_db(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS debt_account_table (
                    lender_name TEXT PRIMARY KEY,
                    contact TEXT,
                    purpose TEXT,
                    debt_date integer,
                    debt_amount INTEGER
                    )''')
        #c.execute('''DROP TABLE IF Exists installment_table''')
        c.execute('''CREATE TABLE IF NOT EXISTS installment_table (
                    lender_name TEXT,
                    installment_number INTEGER,
                    paid_amount INTEGER,
                    remaining_amount INTEGER,
                    date integer,
                    PRIMARY KEY (lender_name, installment_number), --Composite Key
                    FOREIGN KEY (lender_name) REFERENCES debt_account_table(lender_name)
                    )''')
        conn.commit()
        conn.close()

    def initialize_gui(self):
        # Entry Frame
        self.entry_frame = tk.LabelFrame(self, text="Add New Debt Entry")
        self.entry_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.grid_columnconfigure(0, weight=1)

        # Fields setup
        self.fields = ["Lender Name", "Contact", "Purpose", "Date: (YYYY-MM-DD)", "Debt Amount"]
        self.entries = {}
        
        for i, field in enumerate(self.fields):
            tk.Label(self.entry_frame, text=f"{field}:").grid(row=i // 2, column=(i % 2) * 2, sticky="e", padx=5, pady=2)
            entry = tk.Entry(self.entry_frame)
            entry.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=1, ipadx=20)
            self.entries[field] = entry
            # Add current date to the Date field
            if field == "Date: (YYYY-MM-DD)":
                entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Search section
        tk.Label(self.entry_frame, text="Search Lender: ", font=("Arial", 10, "bold")).grid(row=3, column=5, columnspan=4, pady=10)
        self.search_entry = tk.Entry(self.entry_frame)
        self.search_entry.grid(row=3, column=9, columnspan=4, pady=10)
        
        # Buttons
        tk.Button(self.entry_frame, text="Search", background="light Blue", 
                 command=lambda: self.search_lender(self.search_entry.get())).grid(row=3, column=13, columnspan=4, pady=10)
        tk.Button(self.entry_frame, text="Refresh Display", background="Teal",
                 command=self.display_data).grid(row=3, column=17, columnspan=4, pady=0, padx=20)
        tk.Button(self.entry_frame, text="Add Debt Entry", bg="Light Green",
                 command=self.insert_data).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.entry_frame, text="Delete Debt Entry", bg="#FF7F7F",
                 command=self.delete_data_from_debt_account).grid(row=3, column=2, columnspan=2, pady=10)

        # Debt Frame
        self.debt_frame = tk.LabelFrame(self, text="Debt Account Records")
        self.debt_frame.grid(row=1, column=0, padx=5, pady=1, sticky="nsew")

        # Treeview and Scrollbar
        self.debt_tree_frame = tk.Frame(self.debt_frame)
        self.debt_tree_frame.grid(row=0, column=0, sticky="nsew")
        self.debt_frame.grid_columnconfigure(0, weight=1)
        self.debt_frame.grid_rowconfigure(0, weight=1)

        self.debt_tree = ttk.Treeview(self.debt_tree_frame, columns=self.fields, show="headings", height=8)
        for col in self.fields:
            self.debt_tree.heading(col, text=col)
            self.debt_tree.column(col, width=100)

        self.debt_vsb = ttk.Scrollbar(self.debt_tree_frame, orient="vertical", command=self.debt_tree.yview)
        self.debt_tree.configure(yscrollcommand=self.debt_vsb.set)

        self.debt_tree.grid(row=0, column=0, sticky="nsew")
        self.debt_vsb.grid(row=0, column=1, sticky="ns")
        self.debt_tree_frame.grid_columnconfigure(0, weight=1)
        self.debt_tree_frame.grid_rowconfigure(0, weight=1)

        self.debt_tree.bind("<Double-1>", self.show_installment_table)

        # Installment Frame
        self.installment_frame = tk.LabelFrame(self, text="Installment Details")
        self.installment_frame.grid(row=2, column=0, padx=5, pady=1, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

    def delete_data_from_debt_account(self):
        selected_item = self.debt_tree.selection()
        if not selected_item:
            return

        lender_name = self.debt_tree.item(selected_item[0], 'values')[0]

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("DELETE FROM debt_account_table WHERE lender_name = ?", (lender_name,))
        c.execute("DELETE FROM installment_table WHERE lender_name = ?", (lender_name,))
        conn.commit()
        conn.close()
        self.display_data()

    def search_lender(self, lender_name):
        if not lender_name:
            messagebox.showerror("Error", "Lender Name is required.")
            return
        try:
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            c.execute("SELECT * FROM debt_account_table WHERE lender_name = ?", (lender_name,))
            for row in c.fetchall():
                for row_id in self.debt_tree.get_children():
                    self.debt_tree.delete(row_id)
                self.debt_tree.insert('', 'end', values=row)
            conn.close()
        except Exception:
            messagebox.showerror("Error", "Lender not found")

    def show_installment_table(self, event):
        selected_item = self.debt_tree.selection()
        if not selected_item:
            return

        lender_name = self.debt_tree.item(selected_item[0], 'values')[0]

        for widget in self.installment_frame.winfo_children():
            widget.destroy()

        tk.Label(self.installment_frame, text=f"Installments of {lender_name}", 
                font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

        columns = ["Installment Number", "Paid Amount", "Remaining Amount", "Date"]

        # Frame for treeview and scrollbar
        tree_frame = tk.Frame(self.installment_frame)
        tree_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.installment_frame.grid_columnconfigure(0, weight=1)

        self.installment_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=7)
        for col in columns:
            self.installment_tree.heading(col, text=col)
            self.installment_tree.column(col, width=100)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.installment_tree.yview)
        self.installment_tree.configure(yscrollcommand=vsb.set)

        self.installment_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        tree_frame.grid_columnconfigure(0, weight=1)

        # Fetch Installments from Database
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT installment_number, paid_amount, remaining_amount, date FROM installment_table WHERE lender_name = ?", 
                 (lender_name,))
        for row in c.fetchall():
            self.installment_tree.insert("", "end", values=row)
        conn.close()

        # Installment Entry Form
        entry_frame = tk.Frame(self.installment_frame)
        entry_frame.grid(row=2, column=0, pady=2)

        labels = ["Installment:", "Paid Amount:", "Remaining Amount:", "Date: (YYYY-MM-DD)"]
        entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(entry_frame, text=label).grid(row=0, column=i*2, padx=5)
            entry = tk.Entry(entry_frame)
            entry.grid(row=0, column=i*2+1, padx=5)
            entries[label] = entry

            if label == "Date: (YYYY-MM-DD)":
                entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def add_installment():
                    # Use the entries dictionary that was defined above
            installment_number = entries["Installment:"].get()
            paid_amount = entries["Paid Amount:"].get()
            remaining_amount = entries["Remaining Amount:"].get()
            date = entries["Date: (YYYY-MM-DD)"].get()

            if installment_number and paid_amount and remaining_amount and date:
                try:
                    conn = sqlite3.connect('AL_Makkah_Watch.db')
                    c = conn.cursor()
                    c.execute('''INSERT INTO installment_table (lender_name, installment_number, paid_amount, remaining_amount, date)
                                VALUES (?, ?, ?, ?, ?)''',
                            (lender_name, int(installment_number), int(paid_amount), int(remaining_amount), date))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Installment added successfully.")
                    self.show_installment_table(event)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add installment: {e}")
                finally:
                    conn.close()
            else:
                messagebox.showerror("Error", "All fields must be filled.")
                
          

        def delete_installment():
            selected_installment = self.installment_tree.selection()
            if not selected_installment:
                messagebox.showerror("Error", "Please select an installment to delete.")
                return
            installment_number = self.installment_tree.item(selected_installment[0], 'values')[0]
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            c.execute("DELETE FROM installment_table WHERE lender_name = ? AND installment_number = ?",
                     (lender_name, installment_number))
            conn.commit()
            conn.close()
            self.display_installment()
            messagebox.showinfo("Success", "Installment deleted successfully.")
            self.show_installment_table(event)

        tk.Button(entry_frame, text="Add Installment", bg="Light Green",
                 command=add_installment).grid(row=0, column=8, padx=5)
        tk.Button(entry_frame, text="Delete Installment", bg="#F44336",
                 command=delete_installment).grid(row=0, column=9, padx=5)

    def installment_exists(self, lender_name, installment_number):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM installment_table WHERE lender_name = ? AND installment_number = ?",
                 (lender_name, installment_number))
        return c.fetchone() is not None

    def lender_exists(self, lender_name):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM debt_account_table WHERE lender_name = ?", (lender_name,))
        return c.fetchone() is not None

    def insert_data(self):
        lender_name = self.entries["Lender Name"].get()
        if not lender_name:
            messagebox.showerror("Error", "Lender Name is required.")
            return
        
        try:
            debt_date = self.entries["Date: (YYYY-MM-DD)"].get()
            formatted_date = datetime.strptime(debt_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        try:
            if self.lender_exists(lender_name):
                messagebox.showerror("Error", "Lender already exists.")
                return
                
            values = (
                lender_name,
                self.entries["Contact"].get(),
                self.entries["Purpose"].get(),
                formatted_date,
                int(self.entries["Debt Amount"].get()) if self.entries["Debt Amount"].get() else 0
            )
            
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            c.execute('''INSERT INTO debt_account_table VALUES (?,?,?,?,?)''', values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data inserted successfully.")
            self.display_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert data: {e}")

    def display_data(self):
        for row in self.debt_tree.get_children():
            self.debt_tree.delete(row)

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM debt_account_table ORDER BY DATE(debt_date) DESC")
        for row in c.fetchall():
            self.debt_tree.insert('', 'end', values=row)
        conn.close()
    
    #display installment table
    def display_installment(self):
        for row in self.installment_tree.get_children():
            self.installment_tree.delete(row)

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM installment_table ORDER BY DATE(date) DESC")
        for row in c.fetchall():
            self.installment_tree.insert('', 'end', values=row)
        conn.close()

