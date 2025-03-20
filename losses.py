import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk, Toplevel
from tkinter import *
import tkinter as tk

class Losses(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")
        
        # Initialize database
        self.create_losses_table()

        self.losses_gui()
        
    def create_losses_table(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS losses_table (
                    date INTEGER,
                    description TEXT,
                    amount INTEGER
                    )''')
        conn.commit()
        conn.close()
        
    def insert_losses(self, date, description, amount):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''INSERT INTO losses_table (date, description, amount) VALUES (?, ?, ?)''', (date, description, amount))
        conn.commit()
        conn.close()
        
    def insert_losses_gui(self, date, description, amount, tree):
        if date and description and amount:
            try:
                # Convert to standard format
                date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return
            try:
                amount = int(amount)
                self.insert_losses(date, description, amount)
                messagebox.showinfo("Success", "Data inserted successfully!")
            except ValueError:
                messagebox.showerror("Error", "Amount must be an integer.")
        else:
            messagebox.showerror("Error", "All fields are required.")
        self.display_losses(tree)
        
    def display_losses(self, tree):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('SELECT * FROM losses_table ORDER BY date DESC')    
        rows = c.fetchall()
        conn.close()

        # Clear existing rows
        for item in tree.get_children():
            tree.delete(item)

        # Insert new rows
        for row in rows:
            tree.insert('', 'end', values=row)
            
    def show_description(self, event):
        selected_item = event.widget.selection()
        if selected_item:
            description = event.widget.item(selected_item[0], 'values')[1]
            messagebox.showinfo("Full Description", description)
            
    def monthly_losses(self):
        # Database connection
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''SELECT strftime('%Y-%m', DATE(date)) AS month, SUM(amount) 
                     FROM losses_table GROUP BY month ORDER BY DATE(date) DESC''')
        rows = c.fetchall()
        conn.close()

        # Create a new window for monthly losses
        monthly_win = Toplevel()
        monthly_win.title("Monthly Losses")
        monthly_win.geometry("400x400")

        Label(monthly_win, text="Monthly Losses", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Treeview to show the results
        tree = ttk.Treeview(monthly_win, columns=('Month', 'Total Amount'), show='headings')
        tree.heading('Month', text='Month')
        tree.heading('Total Amount', text='Total Amount (PKR)')
        tree.grid(row=1, column=0, pady=10, sticky=(N, S, E, W))
        
        # Configure grid to expand
        monthly_win.grid_rowconfigure(1, weight=1)
        monthly_win.grid_columnconfigure(0, weight=1)

        # Insert monthly totals into Treeview
        for row in rows:
            month = row[0]
            total_amount = row[1]
            tree.insert('', 'end', values=(month, total_amount))

        Button(monthly_win, text="Close", command=monthly_win.destroy).grid(row=2, column=0, pady=10)
        
    def calculate_losses(self, start_date_entry, end_date_entry):
        try:
            # Convert user input date to YYYY-MM-DD
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            formatted_date_start = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD
            formatted_date_end = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        if not (formatted_date_start and formatted_date_end):
            messagebox.showerror("Error", "Please enter both start and end dates.")
            return

        try:
            # Query expenses grouped by type within the date range
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            c.execute('''SELECT SUM(amount) 
                         FROM losses_table 
                         WHERE date BETWEEN ? AND ? ''', (formatted_date_start, formatted_date_end))
            results = c.fetchall()
            conn.close()
            print(results)
            # Display results in a messagebox or print them
            if results:
                messagebox.showinfo("Loss Summary", f"Losses from {formatted_date_start} to {formatted_date_end}:\n\n{results[0][0]} PKR")
            else:
                messagebox.showinfo("Loss Summary", "No Losses found for the selected date range.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def delete_loss(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return

        try:
            # Fetch the selected row's data
            selected_item = selected_item[0]
            values = tree.item(selected_item, 'values')
            date, description, amount = values[0], values[1], values[2]

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", 
                f"Are you sure you want to delete {description} on {date} with amount {amount} PKR?")
                
            if confirm:
                conn = sqlite3.connect('AL_Makkah_Watch.db')
                c = conn.cursor()
                
                # First find the rowid of the specific record
                c.execute('''SELECT rowid FROM losses_table 
                            WHERE date = ? AND description = ? AND amount = ? 
                            LIMIT 1''', (date, description, amount))
                row = c.fetchone()
                
                if row:
                    # Delete using rowid to ensure only one record is deleted
                    c.execute('''DELETE FROM losses_table WHERE rowid = ?''', (row[0],))
                    conn.commit()
                    messagebox.showinfo("Success", "Loss deleted successfully.")
                    self.display_losses(tree)  # Refresh the table
                else:
                    messagebox.showerror("Error", "Record not found")
                    
                conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def edit_losses(self, tree, date_entry, description_entry, amount_entry):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to edit.")
            return

        # Fetch the selected row's data
        selected_item = selected_item[0]
        values = tree.item(selected_item, 'values')
        
        # Clear and insert values into entry fields
        date_entry.delete(0, tk.END)
        date_entry.insert(0, values[0])
        
        description_entry.delete(0, tk.END)
        description_entry.insert(0, values[1])
        
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[2])

    def update_losses(self, tree, date_entry, description_entry, amount_entry):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to update.")
            return

        # Get original values
        old_values = tree.item(selected_item[0], 'values')
        
        # Get new values
        new_date = date_entry.get()
        new_description = description_entry.get()
        new_amount = amount_entry.get()

        if not (new_date and new_description and new_amount):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            new_amount = int(new_amount)
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            
            # First find the rowid of the specific record
            c.execute('''SELECT rowid FROM losses_table 
                        WHERE date = ? AND description = ? AND amount = ? 
                        LIMIT 1''', old_values)
            row = c.fetchone()
            
            if row:
                # Update using rowid to ensure only one record is updated
                c.execute('''UPDATE losses_table 
                            SET date = ?, description = ?, amount = ? 
                            WHERE rowid = ?''', 
                            (new_date, new_description, new_amount, row[0]))
                conn.commit()
                messagebox.showinfo("Success", "Loss updated successfully.")
                self.display_losses(tree)  # Refresh the table
            else:
                messagebox.showerror("Error", "Record not found")
                
            conn.close()
            
        except ValueError:
            messagebox.showerror("Error", "Amount must be an integer.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def losses_gui(self):
        # Set up grid configuration for self
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Entry frame
        entry_frame = Frame(self)
        entry_frame.grid(row=0, column=0, pady=10, sticky='ew')

        Label(entry_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2)
        date_entry = Entry(entry_frame)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=0, column=1, padx=5, pady=2)

        Label(entry_frame, text="Description:").grid(row=1, column=0, padx=5, pady=2)
        description_entry = Entry(entry_frame)
        description_entry.grid(row=1, column=1, padx=5, pady=2)

        Label(entry_frame, text="Amount (PKR):").grid(row=2, column=0, padx=5, pady=2)
        amount_entry = Entry(entry_frame)
        amount_entry.grid(row=2, column=1, padx=5, pady=2)

        Button(entry_frame, background = "light green", text="Add Loss", 
               command=lambda: self.insert_losses_gui(date_entry.get(), description_entry.get(), amount_entry.get(), tree)).grid(row=3, column=0, columnspan=2, pady=5)
        Button(entry_frame, text="Delete Loss", background = "#FF7F7F",
               command=lambda: self.delete_loss(tree)).grid(row=3, column=2, padx=5)
               
        # Add Date Range Inputs
        Label(entry_frame, text="From (YYYY-MM-DD):").grid(row=5, column=0, padx=1, pady=0)
        start_date_entry = Entry(entry_frame)
        start_date_entry.grid(row=5, column=1, padx=1, pady=0)

        Label(entry_frame, text="To (YYYY-MM-DD):").grid(row=5, column=2, padx=1, pady=0)
        end_date_entry = Entry(entry_frame)
        end_date_entry.grid(row=5, column=3, padx=1, pady=0)
        Button(entry_frame, text="Calculate Losses", bg="violet",
               command=lambda: self.calculate_losses(start_date_entry, end_date_entry)).grid(row=5, column=4, padx=10)
               
        # Treeview for displaying losses
        tree_frame = Frame(self)
        tree_frame.grid(row=1, column=0, sticky='nsew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        tree = ttk.Treeview(tree_frame, columns=('Date', 'Description', 'Amount'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Description', text='Description')
        tree.heading('Amount', text='Amount (PKR)')
        tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar
        scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)

        # Bind double-click event to show full description
        tree.bind("<Double-1>", self.show_description)

        # Button frame
        button_frame = Frame(self)
        button_frame.grid(row=2, column=0, pady=10)

        Button(button_frame, text="Refresh Data", background="Teal", 
               command=lambda: self.display_losses(tree)).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Monthly Totals", background="Violet", 
               command=self.monthly_losses).grid(row=0, column=1, padx=5)
                # Replace the Edit Loss button with these two buttons
        Button(button_frame, text="Edit Loss", background="Grey",
            command=lambda: self.edit_losses(tree, date_entry, description_entry, amount_entry)
            ).grid(row=0, column=2, padx=5)
            
        Button(button_frame, text="Update Loss", background="Yellow",
            command=lambda: self.update_losses(tree, date_entry, description_entry, amount_entry)
            ).grid(row=0, column=3, padx=5)
        # Initialize display
        self.display_losses(tree)
