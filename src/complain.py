import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class complaint_repair_gui(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")

        self.initialize_db()
        self.complaint_repair_gui()
        self.display_data()
    # Database Initialization
    def initialize_db(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS complain_table (
                    date INTEGER,
                    model_num TEXT ,
                    customer_name TEXT,
                    contact_num TEXT,
                    description TEXT,
                    status TEXT,
                    paid_unpaid TEXT,
                    amount INTEGER
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS repair_table (
                    date INTEGER,
                    model_num TEXT ,
                    customer_name TEXT,
                    contact_num TEXT,
                    description TEXT,
                    status TEXT,
                    amount INTEGER
                    )''')
        conn.commit()
        conn.close()

    def show_description(self, event):
            tree = event.widget
            selected_item = tree.selection()
            if selected_item:
                # Get values for the selected item
                values = tree.item(selected_item[0])['values']
                if values:
                    # Description is in the 5th column (index 4)
                    description = values[4]
                    if description:
                        # Create a more detailed message box
                        messagebox.showinfo("Full Description", 
                                        f"Model: {values[1]}\n"
                                        f"Customer: {values[2]}\n"
                                        f"Description: {description}")

    # Insert Data into Table 
    def insert_data(self):
        model_num = self.model_entry.get().strip()
        table = self.table_var.get()
        
        # Validation
        if not table:
            messagebox.showerror("Error", "Please select a table.")
            return
        if not model_num:
            messagebox.showerror("Error", "Model Number is required.")
            return
            
        try:
            formatted_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return 

        # Prepare values based on table type
        if table == 'Complain':
            values = (
                formatted_date,
                model_num,
                self.name_entry.get(),
                self.contact_entry.get(),
                self.desc_entry.get(),
                self.status_var.get(),
                self.paid_var.get(),  # Only for Complain table
                self.amount_entry.get() if self.amount_entry.get() else 0
            )
            query = "INSERT INTO complain_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        else:  # Repair table
            values = (
                formatted_date,
                model_num,
                self.name_entry.get(),
                self.contact_entry.get(),
                self.desc_entry.get(),
                self.status_var.get(),
                self.amount_entry.get() if self.amount_entry.get() else 0
            )
            query = "INSERT INTO repair_table VALUES (?, ?, ?, ?, ?, ?, ?)"

        try:
            with sqlite3.connect('AL_Makkah_Watch.db') as conn:
                c = conn.cursor()
                c.execute(query, values)
                conn.commit()
                
            messagebox.showinfo("Success", f"{table} added successfully!")
            self.display_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # model_num exists function
    def model_num_exists(self,model_num, table):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        if table == "Complain":
            c.execute("SELECT * FROM complain_table WHERE model_num = ?", (model_num,))
        else:
            c.execute("SELECT * FROM repair_table WHERE model_num = ?", (model_num,))
        row = c.fetchone()
        conn.close()
        return row

    # Display Data (inserting records with tags)
    def display_data(self):
        for row in self.complain_tree.get_children():
            self.complain_tree.delete(row)
        for row in self.repair_tree.get_children():
            self.repair_tree.delete(row)

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()

        # -- Complain Table
        c.execute("SELECT ROWID,* FROM complain_table ORDER BY DATE(date) DESC")
        for row in c.fetchall():
            # CHANGED: use iid=row[1] instead of tags=(row[1],)
            self.complain_tree.insert('', 'end', iid=row[0], values=row[1:])

        # -- Repair Table
        c.execute("SELECT ROWID, * FROM repair_table")
        for row in c.fetchall():
            # CHANGED: use iid=row[1]
            self.repair_tree.insert('', 'end', iid=row[0], values=row[1:])

        conn.close()

    # Delete Selected Entry using the stored tag
    def delete_entry(self,tree, table):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return

        # CHANGED: Get the item ID (iid) directly
        selected_iid = tree.selection()[0]

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute(f"DELETE FROM {table} WHERE ROWID = ?", (selected_iid,))
        conn.commit()
        conn.close()
        self.display_data()


    # Common Search Function (updated to insert with tags)
    def search_data(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a model number to search.")
            return

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM complain_table WHERE customer_name LIKE ?", ('%' + query + '%',))
        complain_results = c.fetchall()

        c.execute("SELECT * FROM repair_table WHERE customer_name LIKE ?", ('%' + query + '%',))
        repair_results = c.fetchall()
        conn.close()

        # Clear both treeviews
        for row in self.complain_tree.get_children():
            self.complain_tree.delete(row)
        for row in self.repair_tree.get_children():
            self.repair_tree.delete(row)

        # Insert results into each treeview with tags
        for row in complain_results:
            self.complain_tree.insert('', 'end', values=row, tags=(row[1],))
        for row in repair_results:
            self.repair_tree.insert('', 'end', values=row, tags=(row[1],))



    def load_selected_data(self,tree, table):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to edit.")
            return

        # Store the ROWID of selected item
        global selected_rowid, selected_table
        selected_rowid = selected_item[0]  # This is the ROWID
        selected_table = table

        row_values = tree.item(selected_item[0], 'values')
        
        self.date_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.status_var.set(row_values[5])
        self.amount_entry.delete(0, tk.END)

        self.date_entry.insert(0, row_values[0])
        self.model_entry.insert(0, row_values[1])
        self.name_entry.insert(0, row_values[2])
        self.contact_entry.insert(0, row_values[3])
        self.desc_entry.insert(0, row_values[4])
        self.amount_entry.insert(0, row_values[-1])

    
        

    def update_entry(self):
        try:
            if not selected_rowid:
                messagebox.showwarning("Warning", "No record selected for update.")
                return
            
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
                
            updated_values = (
                self.date_entry.get(),
                self.model_entry.get(),
                self.name_entry.get(),
                self.contact_entry.get(),
                self.desc_entry.get(),
                self.status_var.get(),
                self.amount_entry.get(),
                selected_rowid  # Using ROWID for WHERE clause
            )

            update_query = f"UPDATE {selected_table} SET date=?, model_num=?, customer_name=?, contact_num=?, description=?, status=?, amount=? WHERE ROWID=?"
            c.execute(update_query, updated_values)
                
            conn.commit()    
            conn.close()
            messagebox.showinfo("Success", "Record updated successfully!")
            self.display_data()
        
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def complaint_repair_gui(self):
        # Create the main frame inside self
        main_frame = tk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")  # Ensures expansion

        # Make main_frame expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a frame for the selection of table
        frame = tk.Frame(main_frame)
        frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        tk.Label(frame, text="Select Table:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        style = ttk.Style()
                # Define custom style
        style = ttk.Style()
        style.configure("Custom.TRadiobutton",
                        font=("Arial", 11, "bold"),
                        background="#f5f5f5",  # Same as frame background
                        foreground="#333",  # Dark text
                        padding=10,
                        relief="ridge")  # Add border

        # Change selected state color
        style.map("Custom.TRadiobutton",
                background=[("active", "#ddd"), ("selected", "#eedd82")],  # Hover and selected colors
                foreground=[("selected", "white")])  # White text when selected

        # Variable for selection
        self.table_var = tk.StringVar(value='Complain')

        # Styled Radio Buttons
        ttk.Radiobutton(frame, text="Complain", variable=self.table_var, value='Complain', style="Custom.TRadiobutton").grid(row=0, column=1, padx=10, pady=5)
        ttk.Radiobutton(frame, text="Repair", variable=self.table_var, value='Repair', style="Custom.TRadiobutton").grid(row=0, column=2, padx=10, pady=5)

        # Entry Frame for adding data
        entry_frame = tk.LabelFrame(main_frame, text="Add New Entry")
        entry_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

            
        self.search_entry = tk.Entry(entry_frame)
        self.search_entry.grid(row=2, column=6, padx= 5, pady = 5)
        tk.Label(entry_frame, text="Search By Customer Name:").grid(row=2, column=5, padx= 10, pady = 5)
        tk.Button(entry_frame, text="Search", command=self.search_data, bg = "Light Blue").grid(row=2, column=7, padx= 5, pady = 5)

        fields = [
            ("Date (YYYY-MM-DD)", 0, 0),
            ("Model Number", 0, 2),
            ("Customer Name", 1, 0),
            ("Contact Number", 1, 2),
            ("Description", 2, 0),
            ("Amount", 2, 2)
        ]

        entries = {}

        for label_text, row, col in fields:
            tk.Label(entry_frame, text=label_text).grid(row=row, column=col, sticky="e", padx=5, pady=2)
            entry = tk.Entry(entry_frame)
            entry.grid(row=row, column=col + 1, sticky="ew", padx=5, pady=2)
            entries[label_text] = entry  # Store references if needed
            
            # Store entries as instance variables
            if "Date" in label_text:
                self.date_entry = entry
                self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            elif "Model" in label_text:
                self.model_entry = entry
            elif "Customer" in label_text:
                self.name_entry = entry
            elif "Contact" in label_text:
                self.contact_entry = entry
            elif "Description" in label_text:
                self.desc_entry = entry
            elif "Amount" in label_text:
                self.amount_entry = entry

        # Status and Paid/Unpaid Fields (Now aligned properly)
        tk.Label(entry_frame, text="Status:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        self.status_var = tk.StringVar(value="Pending")
        tk.OptionMenu(entry_frame, self.status_var, "Pending", "Completed").grid(row=3, column=1, sticky="ew", padx=5, pady=
        2)
        
        # Paid/Unpaid Field
        tk.Label(entry_frame, text="Paid/Unpaid:").grid(row=3, column=2, sticky="e", padx=5, pady=2)
        self.paid_var = tk.StringVar(value="Paid")
        tk.OptionMenu(entry_frame, self.paid_var, "Paid", "Unpaid").grid(row=3, column=3, sticky="ew", padx=5, pady=2)


        # Add Entry Button (Aligned to the right)
        tk.Button(entry_frame, text="Add Entry", bg="Light Green",command=self.insert_data).grid(row=4, column=2, sticky="e", padx=5, pady=5)

        # Ensure all columns stretch properly
        for i in range(4):
            entry_frame.columnconfigure(i, weight=1)
                
        # Treeview Function
        def create_tree(columns, label, row):
            frame = tk.LabelFrame(main_frame, text=label)
            frame.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

            tree_scroll = tk.Scrollbar(frame, orient="vertical")
            tree_scroll.grid(row=0, column=1, sticky="ns")

            tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
            tree.grid(row=0, column=0, sticky="nsew")

            # Bind double-click event to show full description
            tree.bind("<Double-Button-1>", self.show_description) 

            tree_scroll.config(command=tree.yview)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            return tree

        # Tables
        columns = ["Date", "Model", "Name", "Contact", "Description", "Status", "Paid", "Amount"]
        columnsx = ["Date", "Model", "Name", "Contact", "Description", "Status", "Amount"]
        self.complain_tree = create_tree( columns, "Complaint Records", row=2)
        self.repair_tree = create_tree(columnsx, "Repair Records", row=3) 
        # *Fixed: Button Frame with Proper Resizing*
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5, padx=10)



        button_texts = [
            ("Delete Complaint", "#FF7F7F"),
            ("Delete Repair", "#FF7F7F"),
            ("Refresh Display", "Teal"),
            ("Edit Complaint", "Grey"),
            ("Edit Repair", "Grey"),
            ("Update Entry", "Yellow")
        ]
        button_commands = [
        (lambda: self.delete_entry(self.complain_tree, "complain_table")),  # Delete Complaint
        (lambda: self.delete_entry(self.repair_tree, "repair_table")),      # Delete Repair
        (self.display_data),                                               # Reset Display
        (lambda: self.load_selected_data(self.complain_tree, "complain_table")),  # Edit Complaint
        (lambda: self.load_selected_data(self.repair_tree, "repair_table")),      # Edit Repair
        (self.update_entry)                                                # Update Entry
                     ]

        for i, ((text, color), cmd) in enumerate(zip(button_texts, button_commands)):
            tk.Button(button_frame, text=text, bg=color, command=cmd).grid(
                row=0, column=i, padx=5, pady=5, sticky="ew")
     
        for i in range(len(button_texts)):
            button_frame.columnconfigure(i, weight=1)  # Ensures buttons stretch properly

        # *Ensure Full Resizing*
        main_frame.grid_rowconfigure(2, weight=1)  # Complaint Table expands
        main_frame.grid_rowconfigure(3, weight=1)  # Repair Table expands
        main_frame.grid_rowconfigure(4, weight=0)  # Buttons fixed at bottom
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)


            