import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

class WatchInventorySystem(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")

        
        # Create tables
        self.create_database_tables()
        
        # Setup UI
        self.setup_ui()
        
        # Load data
        self.refresh_stock_table()

    def create_database_tables(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        # Modified stock table to only have provider_name as PRIMARY KEY
        #c.execute('''DROP TABLE IF EXISTS stock_table''')
        c.execute('''CREATE TABLE IF NOT EXISTS stock_table
                 (date TEXT NOT NULL, provider_name TEXT PRIMARY KEY, quantity INTEGER, total_price INTEGER)''')
        #c.execute('''DROP TABLE IF EXISTS all_items_table''')
        c.execute('''CREATE TABLE IF NOT EXISTS all_items_table (
                model_num TEXT PRIMARY KEY,
                quantity INTEGER,
                parchasing_price INTEGER
                )''')
        conn.commit()
        conn.close()

    def setup_ui(self):
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create frames for tabs
        self.stock_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.details_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.reports_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        
        # Add frames to notebook
        self.notebook.add(self.stock_frame, text="Providers Management")
        self.notebook.add(self.details_frame, text="Watch Details")
        self.notebook.add(self.reports_frame, text="Reports")
        
        # Setup each tab
        self.setup_stock_tab()
        self.setup_details_tab()
        self.setup_reports_tab()

    def setup_stock_tab(self):
        # Left panel for form
        form_frame = tk.LabelFrame(self.stock_frame, text="Add New Provider", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 12, "bold"))
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Date
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.bind("<Return>", self.on_enter)

        
        # Provider name
        tk.Label(form_frame, text="Provider Name:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.provider_name_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.provider_name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.provider_name_entry.bind("<Return>", self.on_enter)
        
        # Quantity
        tk.Label(form_frame, text="Total Quantity:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.pro_quantity_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.pro_quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        self.pro_quantity_entry.bind("<Return>", self.on_enter)
        
        # Total price
        tk.Label(form_frame, text="Total Price:", bg="#f0f0f0", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.total_price_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.total_price_entry.grid(row=3, column=1, padx=5, pady=5)
        self.total_price_entry.bind("<Return>", self.on_enter)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="#f0f0f0")
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        tk.Button(button_frame, text="Add Provider", command=self.add_provider, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0,column=1, padx=5)
                 
        tk.Button(button_frame, text="Delete Provider", command=self.delete_provider,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0,column=2, padx=5)
        
        tk.Button(button_frame, text="Search", command=self.search_provider,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0,column=3, padx=5)
        
        tk.Button(button_frame, text="Refresh", command=self.refresh_stock_table,
                 bg="Teal", fg="black", font=("Arial", 10, "bold"), width=15).grid(row=1,column=1, padx=5,pady=10)

        # Right panel for treeview
        table_frame = tk.LabelFrame(self.stock_frame, text="Providers List", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 12, "bold"))
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview
        columns = ("Date", "Provider Name", "Quantity", "Total Price")
        self.provider_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Define headings
        for col in columns:
            self.provider_tree.heading(col, text=col)
            self.provider_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.provider_tree.yview)
        self.provider_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.provider_tree.pack(fill="both", expand=True)
        
        # Bind double-click event
        self.provider_tree.bind("<Double-1>", self.on_provider_double_click)

    def setup_details_tab(self):
        # Create frames
        self.provider_select_frame = tk.LabelFrame(self.details_frame, text="Select Provider", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.provider_select_frame.pack(fill="x", padx=10, pady=10)
        
        # Provider selection
        tk.Label(self.provider_select_frame, text="Provider Name:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left", padx=5)
        
        self.provider_var = tk.StringVar()
        self.provider_dropdown = ttk.Combobox(self.provider_select_frame, textvariable=self.provider_var, width=30, font=("Arial", 10))
        self.provider_dropdown.pack(side="left", padx=5)
        self.provider_dropdown.bind("<<ComboboxSelected>>", self.on_provider_selected)
        
        # Create panels
        left_panel = tk.Frame(self.details_frame, bg="#f0f0f0")
        left_panel.pack(side="left", fill="both", padx=1, pady=10)
        
        right_panel = tk.Frame(self.details_frame, bg="#f0f0f0",)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Form for adding watch details
        form_frame = tk.LabelFrame(left_panel, text="Add Watch Details", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 12, "bold"))
        form_frame.pack(fill="both", padx=1, pady=10)
        
        # Model number
        tk.Label(form_frame, text="Model Number:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.model_num_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.model_num_entry.grid(row=0, column=1, padx=5, pady=5)
        self.model_num_entry.bind("<Return>", self.on_enter)
        
        # Type of watch
        tk.Label(form_frame, text="Type of Watch:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.type_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)
        self.type_entry.bind("<Return>", self.on_enter)
        
        # Purchase price
        tk.Label(form_frame, text="Purchasing Price Per unit:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.purchase_price_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.purchase_price_entry.grid(row=2, column=1, padx=5, pady=5)
        self.purchase_price_entry.bind("<Return>", self.on_enter)
        
        # Selling price
        tk.Label(form_frame, text="Selling Price Per unit:", bg="#f0f0f0", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.selling_price_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.selling_price_entry.grid(row=3, column=1, padx=5, pady=5)
        self.selling_price_entry.bind("<Return>", self.on_enter)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", bg="#f0f0f0", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        self.quantity_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.quantity_entry.grid(row=4, column=1, padx=5, pady=5)
        self.quantity_entry.bind("<Return>", self.on_enter)
        
        # Booking status
        self.booking_var = tk.BooleanVar()
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="#f0f0f0")
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        tk.Button(button_frame, text="Add Watch", command=self.add_watch_details,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(button_frame, text="Delete Watch", command=self.delete_watch,
                 bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(button_frame, text="Search", command=self.search_watch_globally,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Button(button_frame, text="Refresh Display ", command=lambda: self.refresh_details_table(self.provider_var.get()),
                    bg="Teal", fg="black", font=("Arial", 10, "bold"), width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text = "Complete Stock", command=self.display_all_item_table,
                    bg = "Orange", fg="black", font=("Arial", 10, "bold"), width=15).grid(row=1, column=1, padx=5, pady=5)
        # Table frame
        table_frame = tk.LabelFrame(right_panel, text="Watch Details", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 10))
        table_frame.place(x=1, y=1, width=890, height=500)

        
        # Create Treeview
        columns = ("Model Number", "Type", "Purchasing Price", "Selling Price ", "Booking Status","Quantity", "Provider")
        self.details_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 8, "bold"))
        
        # Define headings
        for col in columns:
            self.details_tree.heading(col, text=col)
            self.details_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.details_tree.yview)
        self.details_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.details_tree.pack(fill="both", expand=True)
        
        # Update provider dropdown
        self.update_provider_dropdown()
    

    def setup_reports_tab(self):
        # Summary frame
        summary_frame = tk.LabelFrame(self.reports_frame, text="Inventory Summary", padx=20, pady=20, bg="#f0f0f0", font=("Arial", 12, "bold"))
        summary_frame.pack(fill="both", padx=20, pady=20)
        
        # Summary labels
        tk.Label(summary_frame, text="Total Watches in Stock:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=10)
        self.total_watches_label = tk.Label(summary_frame, text="0", bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.total_watches_label.grid(row=0, column=1, sticky="w", pady=10)
        
        tk.Label(summary_frame, text="Total Inventory Value:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=10)
        self.total_value_label = tk.Label(summary_frame, text="$0", bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.total_value_label.grid(row=1, column=1, sticky="w", pady=10)
        
        # Refresh button
        tk.Button(summary_frame, text="Refresh Summary", command=self.update_summary,
                 bg="Teal", fg="white", font=("Arial", 10, "bold"), width=15).grid(row=2, column=0, columnspan=2, pady=15)
        
        # Initialize summary
        self.update_summary()

    def display_all_item_table(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM all_items_table ORDER BY Quantity DESC")
        items = c.fetchall()
        conn.close()

        self.all_item_table_window = tk.Toplevel()
        self.all_item_table_window.title("Complete Stock")
        self.all_item_table_window.geometry("800x400")

        frame = tk.Frame(self.all_item_table_window)
        frame.pack(fill="both", expand=True)

        # Fix column names (ensure consistency)
        self.all_item_tree = ttk.Treeview(frame, columns=("Model Number", "Quantity", "Purchasing Price"), show="headings")

        # Define correct headings
        self.all_item_tree.heading("Model Number", text="Model Number")
        self.all_item_tree.heading("Quantity", text="Quantity")
        self.all_item_tree.heading("Purchasing Price", text="Unit Purchasing Price")  # Correct reference

        # Set column widths
        self.all_item_tree.column("Model Number", width=200)
        self.all_item_tree.column("Quantity", width=100)
        self.all_item_tree.column("Purchasing Price", width=150)  # Correct reference

        # Add vertical scrollbar
        scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=self.all_item_tree.yview)
        self.all_item_tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_y.pack(side="right", fill="y")
        self.all_item_tree.pack(side="left", fill="both", expand=True)

        # Clear and insert items
        self.all_item_tree.delete(*self.all_item_tree.get_children())

        for item in items:
            self.all_item_tree.insert("", "end", values=item)

    def on_enter(self, event):
        widget = event.widget
        widget.tk_focusNext().focus()

    def add_provider(self):
        date = self.date_entry.get()
        provider_name = self.provider_name_entry.get()
        
        try:
            pro_quantity = int(self.pro_quantity_entry.get())
            if int(pro_quantity) < 0:
                messagebox.showerror("Error", "Quantity must be a positive integer.")
                return
            total_price = int(self.total_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity and Total Price must be numbers.")
            return
            
        if not provider_name:
            messagebox.showerror("Error", "Provider Name is required.")
            return
            
        try:
            # Convert to standard format
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return
            
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        try:
            # Check if provider already exists
            c.execute("SELECT provider_name FROM stock_table WHERE provider_name = ?", (provider_name,))
            # Drop the existing details table if it exists
            #c.execute(f"DROP TABLE IF EXISTS {provider_name}_details")
            # If provider doesn't exist, insert a new record
            c.execute("INSERT INTO stock_table VALUES (?, ?, ?, ?)", (date, provider_name, pro_quantity, total_price))
            # Create details table for this provider
            #c.execute(f"DROP TABLE IF EXISTS {provider_name}_details")
            c.execute(f'''CREATE TABLE IF NOT EXISTS {provider_name}_details
                            (model_num TEXT,
                            type_of_watch TEXT,
                            purchasing_price INTEGER,
                            selling_price INTEGER,
                            booking BOOLEAN,
                            quantity INTEGER,
                            provider_x TEXT)''') 
            conn.commit()
            messagebox.showinfo("Success", f"Provider '{provider_name}' added successfully.")
            
            self.refresh_stock_table()
            self.update_provider_dropdown()
            #self.clear_provider_form()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()

    def delete_provider(self):
        selected_items = self.provider_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a provider to delete.") 
            return
            
        provider_name = self.provider_tree.item(selected_items[0])['values'][1]
        
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete provider '{provider_name}' and all associated watch details?"):
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            try:
                c.execute(f"SELECT model_num, quantity FROM {provider_name}_details")
                results = c.fetchall()
                for i in results:
                    # update all_items_table
                    c.execute("UPDATE all_items_table SET quantity = quantity - ? WHERE model_num =?", (i[1], i[0]))

            except Exception as e:
                messagebox.showerror("Error", f"Failed to check for watch details table: {str(e)}")
                return
            try:
                c.execute(f"DELETE FROM stock_table WHERE provider_name = ?", (provider_name,))
                c.execute(f"DROP TABLE IF EXISTS {provider_name}_details")
                conn.commit()
                messagebox.showinfo("Success", f"Provider '{provider_name}' deleted successfully.")
                self.refresh_stock_table()
                self.update_provider_dropdown()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to delete provider: {str(e)}")
            finally:
                conn.close()

    def search_provider(self):
        provider_name = self.provider_name_entry.get()
        
        if not provider_name:
            messagebox.showerror("Error", "Please enter a provider name to search.")
            return
            
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        try:
            c.execute("SELECT * FROM stock_table WHERE provider_name LIKE ?", (f"%{provider_name}%",))
            rows = c.fetchall()
            
            if not rows:
                messagebox.showinfo("Search Result", f"No providers found matching '{provider_name}'.")
                return
                
            # Clear the treeview
            for item in self.provider_tree.get_children():
                self.provider_tree.delete(item)
                
            # Insert matching rows
            for row in rows:
                self.provider_tree.insert("", "end", values=row)
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
        finally:
            conn.close()

    def add_watch_details(self):
        provider_name = self.provider_var.get()
        model_num = self.model_num_entry.get()
        watch_type = self.type_entry.get()

        
        try:
            quantity = int(self.quantity_entry.get())
            if int(quantity) < 0:
                messagebox.showerror("Error", "Quantity must be a positive integer.")
                return
            purchase_price = int(self.purchase_price_entry.get())
            selling_price = self.selling_price_entry.get()
        except ValueError:
            messagebox.showerror("Error", "Prices must be numbers.")
            return
            
        if not provider_name or not model_num or not watch_type or not purchase_price:
            messagebox.showerror("Error", "Provider Name, Model Number, Type, prices, and quantity are required.")
            return
            
        booking = 1 if self.booking_var.get() else 0
        
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        try:
            # Directly insert the new watch details without checking for existing model numbers
            c.execute(f'''INSERT INTO {provider_name}_details 
                            (model_num, type_of_watch, purchasing_price, selling_price, booking, quantity, provider_x)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                        (model_num, watch_type, purchase_price, selling_price, booking, quantity, provider_name))
            conn.commit()
            messagebox.showinfo("Success", f"Watch details for model '{model_num}' added successfully.")
            
            self.refresh_details_table(provider_name)
            self.update_summary()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add watch details: {str(e)}")
        finally:
            conn.close()
        
        self.add_into_all_item_table(model_num, quantity,purchase_price)
    
    def add_into_all_item_table(self, model_num, quantity,Unit_Purchasing_Price):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM all_items_table WHERE model_num =?", (model_num,))
        if c.fetchone() is not None:
            c.execute("UPDATE all_items_table SET quantity = quantity + ? WHERE model_num =?", (quantity, model_num))
            c.execute("UPDATE all_items_table SET parchasing_price = ? WHERE model_num =?", (Unit_Purchasing_Price, model_num))
        else:
            c.execute("INSERT INTO all_items_table VALUES (?,?,?)", (model_num, quantity,Unit_Purchasing_Price))
        conn.commit()
        conn.close()

    def delete_watch(self):
        selected_items = self.details_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a watch to delete.")
            return
            
        provider_name = self.provider_var.get()
        selected_item = selected_items[0]
        # Fetch the quantity of the selected item
        quantity = int(self.details_tree.item(selected_item, 'values')[5])
        model_num = self.details_tree.item(selected_item, 'values')[0]
        
        # Fetch the rowid of the selected item
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        try:
            c.execute(f"SELECT rowid FROM {provider_name}_details WHERE model_num = ? LIMIT 1", (model_num,))
            rowid = c.fetchone()[0]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to fetch rowid: {str(e)}")
            conn.close()
            return
        
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete model '{model_num}' from {provider_name}_details?"):
            try:
                c.execute(f"DELETE FROM {provider_name}_details WHERE rowid = ?", (rowid,))
                conn.commit()
                messagebox.showinfo("Success", f"Watch model '{model_num}' deleted successfully.")
                self.refresh_details_table(provider_name)
                self.update_summary()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Failed to delete watch: {str(e)}")
            finally:
                conn.close()
        
        self.remove_from_all_item_table(model_num, quantity)

    def remove_from_all_item_table(self, model_num, quantity):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM all_items_table WHERE model_num = ?", (model_num,))
        item = c.fetchone()
        if item is not None:
            c.execute("UPDATE all_items_table SET quantity = quantity - ? WHERE model_num = ?", (quantity, model_num))
            # deleting the item if quantity becomes zero
            if item[1] == 0:
                c.execute("DELETE FROM all_items_table WHERE model_num =?", (model_num,))
        conn.commit()
        conn.close()

    def search_watch_globally(self):
        model_num = self.model_num_entry.get()
        
        if not model_num:
            messagebox.showerror("Error", "Please enter a model number to search.")
            return
        
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        try:
            # Clear the treeview
            for item in self.details_tree.get_children():
                self.details_tree.delete(item)
            
            # Search across all provider tables
            c.execute("SELECT provider_name FROM stock_table")
            providers = c.fetchall()
            
            found = False
            for provider in providers:
                provider_name = provider[0]
                c.execute(f"SELECT * FROM {provider_name}_details WHERE model_num LIKE ?", (f"%{model_num}%",))
                rows = c.fetchall()
                
                if rows:
                    found = True
                    for row in rows:
                        booking_status = "Yes" if row[4] else "No"
                        self.details_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], booking_status, row[5], row[6]))
            
            if not found:
                messagebox.showinfo("Search Result", f"No watches found matching model '{model_num}'.")
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
        finally:
            conn.close()

    def on_provider_double_click(self, event):
        selected_items = self.provider_tree.selection()
        if not selected_items:
            return
            
        provider_name = self.provider_tree.item(selected_items[0])['values'][1]
        
        # Switch to details tab
        self.notebook.select(self.details_frame)
        
        # Set the provider and show details
        self.provider_var.set(provider_name)
        self.refresh_details_table(provider_name)

    def on_provider_selected(self, event):
        provider_name = self.provider_var.get()
        if provider_name:
            self.refresh_details_table(provider_name)

    def refresh_stock_table(self):
        # Clear the treeview
        for item in self.provider_tree.get_children():
            self.provider_tree.delete(item)
            
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        try:
            c.execute("SELECT * FROM stock_table ORDER BY date DESC")
            rows = c.fetchall()
            
            for row in rows:
                self.provider_tree.insert("", "end", values=row)
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load providers: {str(e)}")
        finally:
            conn.close()

    # refresh and clear watch details
    def refresh_details_table(self, provider_name):
    # Clear the treeview
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        
        if not provider_name:
            return
            
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        try:
            c.execute(f"SELECT * FROM {provider_name}_details")
            rows = c.fetchall()
            
            for row in rows:
                booking_status = "Yes" if row[4] else "No"
                # Make sure to include the quantity (row[5]) in the values tuple
                self.details_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], booking_status, row[5], row[6]))
                
        except sqlite3.OperationalError:
            # Table might not exist yet
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load watch details: {str(e)}")
        finally:
            conn.close()

    def update_provider_dropdown(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        try:
            c.execute("SELECT provider_name FROM stock_table")
            providers = [row[0] for row in c.fetchall()]
            
            self.provider_dropdown['values'] = providers
            
            # If current selection is not in the list, clear it
            if self.provider_var.get() not in providers:
                self.provider_var.set("")
                
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load providers: {str(e)}")
        finally:
            conn.close()

    def update_summary(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        total_watches = 0
        total_value = 0
        
        try:        
            # Sum up the purchasing prices
            
            c.execute(f"SELECT SUM(parchasing_price * quantity), SUM(quantity) FROM all_items_table")
            total_value, total_watches = c.fetchone()
            #total_value = c.fetchone()[0]
            #total_watches = total_values[1]
            
            self.total_watches_label.config(text=str(total_watches))
            self.total_value_label.config(text=f"PKR: {total_value:}")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to update summary: {str(e)}")
        finally:
            conn.close()

    def clear_watch_form(self):
        self.model_num_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)
        self.selling_price_entry.delete(0, tk.END)
        self.booking_var.set(False)
        self.quantity_entry.delete(0, tk.END)
