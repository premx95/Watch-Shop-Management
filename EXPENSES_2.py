import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk, Toplevel
from datetime import datetime

class expenses(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")

        self.initialize_db()
        self.expenses_gui()
        self.display_data()

    def expenses_gui(self):
        # Main Frame
        main_frame = tk.Frame(self, bg="lightgray")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Allow frame to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Entry Frame
        entry_frame = tk.Frame(main_frame)
        entry_frame.pack(pady=10)

        # Date Entry
        tk.Label(entry_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.date_entry = tk.Entry(entry_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Description Entry
        tk.Label(entry_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.desc_entry = tk.Entry(entry_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        # Type Dropdown
        tk.Label(entry_frame, text="Type:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(entry_frame, textvariable=self.type_var, values=["Rent", "Salary", "Electricity", "Water", "Internet", "Transport", "Others"])
        self.type_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.type_dropdown.set("Select Type")

        # Amount Entry
        tk.Label(entry_frame, text="Amount:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.amount_entry = tk.Entry(entry_frame)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Expense", bg="light green",command=self.insert_data).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete Expense", bg="#FF7F7F",command=self.delete_expense).grid(row=0, column=1, padx=5, pady=5)

        # Date Range Inputs
        tk.Label(btn_frame, text="From (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = tk.Entry(btn_frame)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(btn_frame, text="To (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5)
        self.end_date_entry = tk.Entry(btn_frame)
        self.end_date_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(btn_frame, text="Calculate Expense", bg="Violet",command=self.calculate_expense).grid(row=1, column=4, padx=5, pady=5)

        # self.treeview for Displaying Expenses
        self.tree_frame = tk.Frame(main_frame)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        columns = ('Date', 'Description', 'Type', 'Amount')
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', height=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)

        # Bottom Buttons
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Edit Expense", bg="Grey",command=self.edit_expense).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(bottom_frame, text="Update Expense", bg="Yellow",command=self.update_expense).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(bottom_frame, text="Reset Display", bg="Teal",command=self.reset_and_clear).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(bottom_frame, text="Monthly Totals", bg="Violet",command=self.monthly_expenses).grid(row=0, column=3, padx=5, pady=5)

        return main_frame
    # Initialize Database
    def initialize_db(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS expenses_table (
                    date INTEGER,
                    description TEXT,
                    type TEXT,
                    amount INTEGER
                    )''')
        conn.commit()
        conn.close()

    # Insert Data into Table
    def insert_data(self):
        date = self.date_entry.get()
        try:
            # Convert to standard format
            date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        description = self.desc_entry.get()
        expense_type = self.type_var.get()
        amount = self.amount_entry.get()

        if not (date and description and expense_type and amount):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            amount = int(amount)
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            c.execute('''INSERT INTO expenses_table (date, description, type, amount) VALUES (?, ?, ?, ?)''',
                    (date, description, expense_type, amount))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data inserted successfully!")
            self.display_data()
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Display Data in self.treeview
    def display_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM expenses_table ORDER BY DATE(date) DESC''')
        for row in c.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()

    #Edit Expenses by clicking on row
    def edit_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an item to edit.")
            return
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[0])

        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, values[1])

        self.type_dropdown.set(values[2])

        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[3])

    def reset_and_clear(self):
        # Clear the self.treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.display_data()

        # Clear the entry fields
        self.desc_entry.delete(0, tk.END)
        self.type_dropdown.set("Select Type")
        self.amount_entry.delete(0, tk.END)

        # Clear the date range fields
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)

    #update Expenses
    def update_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an item to update.")
            return
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        date = self.date_entry.get()
        description = self.desc_entry.get()
        expense_type = self.type_var.get()
        amount = self.amount_entry.get()

        if not (date and description and expense_type and amount):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            amount = int(amount)
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            
            # First find the rowid of the specific record
            c.execute('''SELECT rowid FROM expenses_table 
                        WHERE date=? AND description=? AND type=? AND amount=? 
                        LIMIT 1''', (values[0], values[1], values[2], values[3]))
            row = c.fetchone()
            
            if row:
                # Update using rowid to ensure only one record is updated
                c.execute('''UPDATE expenses_table 
                            SET date=?, description=?, type=?, amount=? 
                            WHERE rowid=?''', 
                            (date, description, expense_type, amount, row[0]))
                conn.commit()
                messagebox.showinfo("Success", "Data updated successfully!")
                self.display_data()
            else:
                messagebox.showerror("Error", "Record not found")
                
            conn.close()
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def monthly_expenses(self):
        # Database connection
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        c.execute('''SELECT strftime('%Y-%m', DATE(date)) AS month, SUM(amount) 
                    FROM expenses_table GROUP BY month ORDER BY DATE(date) DESC''')
        rows = c.fetchall()
        conn.close()

        # Create a new window for monthly losses
        monthly_win = Toplevel()
        monthly_win.title("Monthly Losses")
        monthly_win.geometry("400x400")

        Label(monthly_win, text="Monthly Losses", font=("Arial", 16, "bold")).pack(pady=10)

        # self.treeview to show the results
        monthly_tree= ttk.Treeview(monthly_win, columns=('Month', 'Total Amount'), show='headings')
        monthly_tree.heading('Month', text='Month')
        monthly_tree.heading('Total Amount', text='Total Amount (PKR)')
        monthly_tree.pack(pady=10, fill=BOTH, expand=True)

        # Insert monthly totals into self.treeview
        for row in rows:
            month = row[0]
            total_amount = row[1]
            monthly_tree.insert('', 'end', values=(month, total_amount))

        Button(monthly_win, text="Close", command=monthly_win.destroy).pack(pady=10)

    def calculate_expense(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        if not (start_date and end_date):
            messagebox.showerror("Error", "Please enter both start and end dates.")
            return
        try:
            formatted_date_start = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD
            formatted_date_end = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date {e}")
            return
        if not (formatted_date_start and formatted_date_end):
            messagebox.showerror("Error", "Please enter both start and end dates.")
            return

        try:
            # Query expenses grouped by type within the date range
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            c.execute('''SELECT type, SUM(amount) 
                        FROM expenses_table 
                        WHERE date BETWEEN ? AND ?
                        GROUP BY type''', (formatted_date_start, formatted_date_end))
            results = c.fetchall()

            # Calculate the total sum of all expenses within the date range
            c.execute('''SELECT SUM(amount) 
                        FROM expenses_table 
                        WHERE date BETWEEN ? AND ?''', (formatted_date_start, formatted_date_end))
            total_sum = c.fetchone()[0]
            conn.close()

            # Display results in a messagebox or print them
            if results:
                result_message = "\n".join([f"{row[0]}: {row[1]} PKR" for row in results])
                result_message += f"\n\nTotal: {total_sum} PKR"
                messagebox.showinfo("Expense Summary", f"Expenses from {formatted_date_start} to {formatted_date_end}:\n\n{result_message}")
            else:
                messagebox.showinfo("Expense Summary", "No expenses found for the selected date range.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #delete expenses and auto refresh the table
    def delete_expense(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select an expense to delete.")
            return

        try:
            values = self.tree.item(selected_item[0], 'values')

            # Confirm before deletion
            if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this expense?"):
                conn = sqlite3.connect('AL_Makkah_Watch.db')
                c = conn.cursor()

                # First find the rowid of the specific record
                c.execute('''SELECT rowid FROM expenses_table 
                            WHERE date=? AND description=? AND type=? AND amount=? 
                            LIMIT 1''', values)
                row = c.fetchone()
                
                if row:
                    # Delete using rowid to ensure only one record is deleted
                    c.execute('''DELETE FROM expenses_table WHERE rowid=?''', (row[0],))
                    conn.commit()
                    
                    # Remove from treeview
                    self.tree.delete(selected_item[0])
                    messagebox.showinfo("Success", "Expense deleted successfully!")
                else:
                    messagebox.showerror("Error", "Record not found")

                conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))