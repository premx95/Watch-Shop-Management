import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import win32api
import tempfile

class WatchBookingSystem(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(bg="#f0f0f0")
        self.bind_all("<Return>", self.on_enter)

        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", background="#f0f0f0", font=("TIMES NEW ROMAN", 10))
        style.configure("TButton", font=("TIMES NEW ROMAN", 10))
        style.configure("TEntry", font=("TIMES NEW ROMAN", 10))
        style.configure("TTreeview", rowheight=25)

        # Create main frames
        self.create_search_frame()
        self.create_booking_frame()
        #self.create_bill_frame()
        self.create_booking_records_frame()

        # Initialize database
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        #c.execute('''drop table if exists booking_record_table''')
        # Booking record table
        #c.execute('''DROP TABLE IF EXISTS booking_record_table_db''')
        c.execute('''CREATE TABLE IF NOT EXISTS booking_record_table_db
                    (DATE TEXT, 
                    MODEL_NUM TEXT,
                    WATCH_TYPE TEXT,
                    QUANTITY INTEGER,
                    CUSTOMER_NAME TEXT, 
                    CONTACT_NUM TEXT,
                    PAID_AMOUNT INTEGER,
                    REMAINING_AMOUNT INTEGER,
                    TOTAL_AMOUNT REAL,
                    PAYMENT_TYPE TEXT,
                    PROFIT TEXT)''')
        #c.execute('''DROP TABLE IF EXISTS booked_sales''')
        c.execute("""CREATE TABLE IF NOT EXISTS booked_sales (
                    DATE TEXT,
                    MODEL_NUM TEXT,
                    WATCH_TYPE TEXT,
                    QUANTITY INTEGER,
                    CUSTOMER_NAME TEXT, 
                    CONTACT_NUM TEXT,
                    PAID_AMOUNT INTEGER,
                    REMAINING_AMOUNT INTEGER,
                    TOTAL_AMOUNT REAL,
                    PAYMENT_TYPE TEXT,
                    PROFIT TEXT)
                    """)
        
        conn.commit()
        conn.close()

    def create_search_frame(self):
        search_frame = tk.LabelFrame(self, text="Search Watches", font=("TIMES NEW ROMAN", 12, "bold"), bg="#f0f0f0")
        search_frame.place(x=20, y=20, width=450, height=75)

        # Search Entry
        tk.Label(search_frame, text="Model Number:*", font=("TIMES NEW ROMAN", 10), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=1, sticky="w")
        self.search_entry_root = tk.Entry(search_frame, font=("TIMES NEW ROMAN", 10), width=30)
        self.search_entry_root.grid(row=0, column=1, padx=10, pady=10)

        # Search Button
        tk.Button(search_frame, text="Check Availability", command=self.check_availability, 
                  font=("TIMES NEW ROMAN", 10), bg="#4CAF50", fg="white").grid(row=0, column=2, padx=10, pady=10)

    def create_booking_frame(self):
        booking_frame = tk.LabelFrame(self, text="Enter Booking Details", font=("TIMES NEW ROMAN", 12, "bold"), bg="#f0f0f0")
        booking_frame.place(x=20, y=120, width=950, height=230)

        # Date Entry
        tk.Label(booking_frame, text="Date (YYYY-MM-DD)", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN", 12), width=25)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Customer Name Entry
        tk.Label(booking_frame, text="Customer Name", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        self.customer_name_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN", 12), width=25)
        self.customer_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Contact Number Entry
        tk.Label(booking_frame, text="Contact Number", font=("TIMES NEW ROMAN",
            12), bg="#f0f0f0").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.contact_num_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN", 12), width=25)
        self.contact_num_entry.grid(row=1, column=3, padx=10, pady=5)

        # Model Number Entry
        tk.Label(booking_frame, text="Model Number", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        self.model_num_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN",12), width=25)  
        self.model_num_entry.grid(row=2, column=1, padx=10, pady=5)

        # Watch Type Entry
        tk.Label(booking_frame, text="Watch Type", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=2, column=2, padx=10, pady=5, sticky="w")
        self.watch_type_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN",12), width=25)    
        self.watch_type_entry.grid(row=2, column=3, padx=10, pady=5)

        # Quantity Entry
        tk.Label(booking_frame, text="Quantity", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        self.quantity_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN", 12), width=25)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        # Paid Amount Entry
        tk.Label(booking_frame, text="Paid Amount", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=3, column=2, padx=10, pady=5, sticky="w")
        self.paid_amount_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN", 12), width=25)
        self.paid_amount_entry.grid(row=3, column=3, padx=10, pady=5)

        # Remaining Amount Entry
        tk.Label(booking_frame, text="Remaining Amount", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=4, column=0, padx=10, pady=5, sticky="w")
        self.remaining_amount_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN", 12), width=25)
        self.remaining_amount_entry.grid(row=4, column=1, padx=10, pady=5)

        # Total Amount Entry
        tk.Label(booking_frame, text="Total Amount", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=4, column=2, padx=10, pady=5, sticky="w")
        self.total_amount_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN", 12), width=25)
        self.total_amount_entry.grid(row=4, column=3, padx=10, pady=5)

        #Profit Entry
        tk.Label(booking_frame, text="Profit", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=5, column=0, padx=10, pady=5, sticky="w")
        self.profit_entry = tk.Entry(booking_frame, font=("TIMES NEW ROMAN",12), width=25)
        self.profit_entry.grid(row=5, column=1, padx=10, pady=5)

        # Payment Type
        tk.Label(booking_frame, text="Payment Type", font=("TIMES NEW ROMAN", 12), bg="#f0f0f0").grid(
            row=5, column=2, padx=10, pady=5, sticky="w")
        self.payment_type_var = tk.StringVar(value="Cash")
        payment_types = ["Cash", "Account"]
        self.payment_type_dropdown = ttk.Combobox(booking_frame, textvariable=self.payment_type_var, values=payment_types, state="readonly", width=22)
        self.payment_type_dropdown.grid(row=5, column=3, padx=10, pady=5)  

        # Buttons    
        tk.Button(booking_frame, text="Add Item", command=self.add_booking, 
                  font=("TIMES NEW ROMAN", 10), bg="LIGHT GREEN", fg="white").grid(row=5, column=4, padx=10, pady=2)
    
    #print bill details
    def print_bill_details(self):
        #before printing the check_availability of the quantity of the model_num
        if not self.booking_tree.get_children():
            messagebox.showwarning("Warning", "No bill content to print.")
            return
        for item in self.booking_tree.get_children():
            values = self.booking_tree.item(item, "values")
            if not values:
                messagebox.showwarning("Warning", "No bill content to print.")
                return
            model_num = values[1]
            quantity = values[3]
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            c.execute(f"SELECT QUANTITY FROM all_items_table WHERE MODEL_NUM = ?", (model_num,))
            qty = c.fetchone()
            if int(quantity) > qty[0]:
                messagebox.showerror("Error", f"only {qty[0]} watches are available in stock.")
                return
            conn.close()
        total_amount= int(0)
        rem_amount =  int(0)

        # Get the bill content from the Treeview
        bill_content = ""
        # Header

        bill_content += "========================================\n"
        bill_content += "    New Al Makkah Watch Booking Bill    \n"
        bill_content += "========================================\n"
        bill_content += f"Printed on: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}\n"
        bill_content += "Shop Address: Sitara Market, Street # 2\n"
        bill_content += "block # 4, Ameen Bazaar, Sargodha.\n"
        bill_content += "Phone: 0300-8706154\n"
        bill_content += "----------------------------------------\n"
        bill_content += "Model No      Quantity      Watch Type  \n"
        bill_content += "----------------------------------------\n"
        for item in self.booking_tree.get_children():
            values = self.booking_tree.item(item, 'values')
            bill_content += f"{values[1]:<13} {values[3]:<13} {values[2]:<13}\n"
            total_amount += int(values[6])
            rem_amount += int(values[7])
        payment_type = values[9]
        bill_content += "----------------------------------------\n"
        bill_content += f"Paid Amount: {total_amount}\n"
        bill_content += f"Remaining Amount: {rem_amount}\n"
        bill_content += f"Payment Type: {payment_type}\n"
        bill_content += "========================================\n"
        bill_content += "     Thank You for Your Purchase!      \n"
        bill_content += "========================================\n"
        bill_content += "سمارٹ واچ واپس یا تبدیل نہ ہو گی۔\n"
        bill_content += "سمارٹ واچ پر گارنٹی لاگو نہیں۔\n"
        bill_content += "گارنٹی والی آئٹم کی گارنٹی صرف مشینری تک محدود ہو گی۔\n"
        bill_content += "بغیر بل کے کوئی کلیم قابل قبول نہیں۔\n"
        bill_content += "تیس دن کے بعد بکنگ کینسل کر دی جائے گی۔\n"

        
            # Save the bill to a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write(bill_content)
            temp_file_path = f.name

        # Send the file to the default printer
        try:
            win32api.ShellExecute(0, "print", temp_file_path, None, ".", 0)
            messagebox.showinfo("Success", "Bill sent to printer successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print bill: {str(e)}")

        for item in self.booking_tree.get_children():
            values = self.booking_tree.item(item, "values")
            date, model_num, watch_type, quantity, customer_name, contact_num, paid_amount, remaining_amount, total_amount, payment_type,profit = values
            self.insert_booking_record(date, model_num, watch_type, quantity, customer_name, contact_num, paid_amount, remaining_amount, total_amount, payment_type,profit)

        for item in self.booking_tree.get_children():
                self.booking_tree.delete(item)

        self.contact_num_entry.delete(0, tk.END)
        self.customer_name_entry.delete(0, tk.END)
                
    def create_booking_records_frame(self):
        records_frame = tk.LabelFrame(self, text="Bill Details", font=("TIMES NEW ROMAN", 10), bg="#f0f0f0")
        records_frame.place(x=20, y=360, width=1330, height=300)

        # Columns for booking records
        columns = ("Date", "Model Number", "Watch Type", "Quantity", "Customer Name", 
                "Contact Number", "Paid Amount", "Remaining Amount", "Total Amount", "Payment Type","Profit")
        
        self.booking_tree = ttk.Treeview(records_frame, columns=columns, show="headings")
        
        for col in columns:
            self.booking_tree.heading(col, text=col)
            self.booking_tree.column(col, width=120, anchor="center")
        
        self.booking_tree.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.booking_tree.yview)
        self.booking_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=4, sticky="ns")

        # Configure grid weights
        records_frame.grid_rowconfigure(0, weight=1)
        records_frame.grid_columnconfigure(0, weight=1)
        records_frame.grid_columnconfigure(1, weight=1)
        records_frame.grid_columnconfigure(2, weight=1)
        records_frame.grid_columnconfigure(3, weight=1)

        # Buttons
        button_frame = tk.Frame(records_frame, bg="#f0f0f0")
        button_frame.grid(row=1, column=0, columnspan=5, pady=10)

        tk.Button(button_frame, text="View Booking Records", command=self.display_only_booking_records, 
                font=("TIMES NEW ROMAN", 10), bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete Selected Item", command=self.delete_booking_record, 
                font=("TIMES NEW ROMAN", 10), bg="#F44336", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="「 ✦ Print Bill ✦ 」🖶", command=self.print_bill_details,
                font=("TIMES NEW ROMAN", 10), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)
            
    def on_enter(self, event):
        widget = event.widget
        widget.tk_focusNext().focus()

    def display_only_booking_records(self):
        # Create a new window for booking records
        self.new_window = tk.Toplevel(self)
        self.new_window.title("Booking Records")
        self.new_window.geometry("800x600")
        self.new_window.configure(bg="#f0f0f0")

        # Create a Treeview widget
        columns = ("Date", "Model Number", "Watch Type", "Quantity", "Customer Name",
                "Contact Number", "Paid Amount", "Remaining Amount", "Total Amount", "Payment Type","Profit")
        self.booking_records_tree = ttk.Treeview(self.new_window, columns=columns, show="headings")

        for col in columns:
            self.booking_records_tree.heading(col, text=col)
            self.booking_records_tree.column(col, width=100)

        self.booking_records_tree.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Add a scrollbar to the Treeview
        scrollbar = tk.Scrollbar(self.new_window, orient=tk.VERTICAL, command=self.booking_records_tree.yview)
        self.booking_records_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # SEARCH SECTION
        search_frame = tk.Frame(self.new_window, bg="#f0f0f0")
        search_frame.pack(pady=(5, 10))

        tk.Label(search_frame, text="Search by Customer Name:", font=("TIMES NEW ROMAN", 10), bg="#f0f0f0").grid(row=0, column=0, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=("TIMES NEW ROMAN", 10), width=30)
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="Search", command=self.search_booking_record,
                font=("TIMES NEW ROMAN", 10), bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)

        # BUTTONS SECTION
        button_frame = tk.Frame(self.new_window, bg="#f0f0f0")
        button_frame.pack(pady=10)

        cancel_button = tk.Button(button_frame, text="Cancel Booking", command=self.cancel_selected_booking_record,
                                font=("TIMES NEW ROMAN", 10), bg="#F44336", fg="white", width=15)
        cancel_button.grid(row=0, column=0, padx=10)

        print_button = tk.Button(button_frame, text="「 ✦ Print Bill ✦ 」🖶", command=self.proceed_booking,
                                font=("TIMES NEW ROMAN", 10), bg="#2196F3", fg="white", width=15)
        print_button.grid(row=0, column=1, padx=10)


                
        # Fetch data from the database and display in booking_records_tree
        try:
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()

            c.execute('SELECT * FROM booking_record_table_db ORDER BY DATE DESC')   
            rows = c.fetchall()

            for row in rows:
                self.booking_records_tree.insert("", "end", values=row)

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error fetching the Details")  # Print error message if there's an issue       
    
    def search_booking_record(self):
        customer_name = self.search_entry.get()
        #print(customer_name)
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM booking_record_table_db WHERE CUSTOMER_NAME LIKE ?", (f"%{customer_name}%",))
        results = c.fetchall()
        #print(results)
        conn.close()

        # Clear the Treeview
        for item in self.booking_records_tree.get_children():
            self.booking_records_tree.delete(item)
        
        # Insert the search results into the Treeview
        for row in results:
            self.booking_records_tree.insert("", "end", values=row)
    
    #proceed_booking to print the bill
    def proceed_booking(self):
        # Get selected items
        selected_items = self.booking_records_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select an item to print.")
            return

        bill_content = ""
        total_amount = 0
        # Header
        bill_content += "========================================\n"
        bill_content += "       Al Makkah Watch Booking Bill     \n"
        bill_content += "========================================\n"
        bill_content += f"Printed on: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}\n"
        bill_content += "Shop Address: Sitara Market, Street # 2\n"
        bill_content += "block # 4, Ameen Bazaar, Sargodha.\n"
        bill_content += "Phone: 0300-8706154\n"
        bill_content += "----------------------------------------\n"
        bill_content += "Model No      Quantity      Watch Type  \n"
        bill_content += "----------------------------------------\n"
        for item_id in selected_items:
            values = self.booking_records_tree.item(item_id, 'values')
            bill_content += f"{values[1]:<13} {values[3]:<13} {values[2]:<13}\n"
            total_amount += int(values[7]) if values[7] else 0
        payment_type = values[9]
        bill_content += "----------------------------------------\n"
        bill_content += f"Amount Paid: {total_amount}\n"
        bill_content += f"Payment Type: {payment_type}\n"
        bill_content += "========================================\n"
        bill_content += "     Thank You for Your Purchase!      \n"
        bill_content += "========================================\n"
        bill_content += "سمارٹ واچ واپس یا تبدیل نہ ہو گی۔\n"
        bill_content += "سمارٹ واچ پر گارنٹی لاگو نہیں۔\n"
        bill_content += "گارنٹی والی آئٹم کی گارنٹی صرف مشینری تک محدود ہو گی۔\n"
        bill_content += "بغیر بل کے کوئی کلیم قابل قبول نہیں۔\n"


        
            # Save the bill to a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write(bill_content)
            temp_file_path = f.name

        # Send the file to the default printer
        try:
            win32api.ShellExecute(0, "print", temp_file_path, None, ".", 0)
            messagebox.showinfo("Success", "Bill sent to printer successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print bill: {str(e)}")
        

        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        for item_id in selected_items:
            c.execute("INSERT INTO booked_sales(DATE, MODEL_NUM, WATCH_TYPE, QUANTITY, CUSTOMER_NAME, CONTACT_NUM, PAID_AMOUNT, REMAINING_AMOUNT, TOTAL_AMOUNT, PAYMENT_TYPE, PROFIT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.booking_records_tree.item(item_id, 'values'))
            c.execute("DELETE FROM booking_record_table_db WHERE DATE = ? AND MODEL_NUM = ? AND WATCH_TYPE = ? AND QUANTITY = ? AND CUSTOMER_NAME = ? AND CONTACT_NUM = ? AND PAID_AMOUNT = ? AND REMAINING_AMOUNT = ? AND TOTAL_AMOUNT = ? AND PAYMENT_TYPE = ? AND PROFIT = ?", self.booking_records_tree.item(item_id, 'values'))
        conn.commit()
        # Delete the selected items from the Treeview
        for item_id in selected_items:
            self.booking_records_tree.delete(item_id)
    #def save_booking_into_sales(self):


    def insert_booking_record(self, date, model_num, watch_type, quantity, customer_name, contact_num, paid_amount, remaining_amount, total_amount, payment_type, profit):
        try:
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()

            c.execute('''INSERT INTO booking_record_table_db  
                        (DATE, MODEL_NUM, WATCH_TYPE, QUANTITY, CUSTOMER_NAME, CONTACT_NUM, PAID_AMOUNT, REMAINING_AMOUNT, TOTAL_AMOUNT, PAYMENT_TYPE, PROFIT)
                        VALUES (?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?)''',
                    (date, model_num, watch_type, quantity, customer_name, contact_num, paid_amount, remaining_amount, total_amount, payment_type, profit))
            c.execute(f'UPDATE all_items_table SET QUANTITY = QUANTITY - {quantity} WHERE MODEL_NUM = ?', (model_num,))
            conn.commit()
            conn.close()
        
        except sqlite3.Error as e:
            messagebox.showerror("Error inserting data", str(e))  # Print error message if there's an issue
        
        return

    #CANCEL SELECTED ROW FROM TREEVIEW OF BOOKING RECORDS
    def cancel_selected_booking_record(self):
        try:
            selected_item = self.booking_records_tree.selection()[0]
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a record to delete.")
                return
            #ask confirmation
            if messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking record?"):
                values = self.booking_records_tree.item(selected_item, 'values')
                date = values[0]
                model_num = values[1]
                watch_type = values[2]
                quantity = values[3]
                customer_name = values[4]
                contact_num = values[5]
                paid_amount = values[6]
                remaining_amount = values[7]
                total_amount = values[8]
                payment_type = values[9]
                profit = values[10]



                conn = sqlite3.connect('AL_Makkah_Watch.db')
                c = conn.cursor()
                
                # Delete the specific record from the booking_record_table_db
                c.execute('''DELETE FROM booking_record_table_db 
                            WHERE DATE = ? AND MODEL_NUM = ? AND WATCH_TYPE = ? AND QUANTITY = ? AND CUSTOMER_NAME = ? 
                            AND CONTACT_NUM = ? AND PAID_AMOUNT = ? AND REMAINING_AMOUNT = ? AND TOTAL_AMOUNT = ? AND PAYMENT_TYPE = ? AND PROFIT = ?
                            ''', 
                        (date, model_num, watch_type, quantity, customer_name, contact_num, paid_amount, remaining_amount, total_amount, payment_type, profit))
                
                # Update the quantity in the all_items_table
                c.execute('UPDATE all_items_table SET QUANTITY = QUANTITY + ? WHERE MODEL_NUM = ?', (quantity, model_num))
                
                conn.commit()
                conn.close()
                
                # Remove the item from the Treeview
                self.booking_records_tree.delete(selected_item)

        except IndexError:
            messagebox.showwarning("Warning", "Please select a record to delete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_availability(self):
        model_num_x = self.search_entry_root.get()  # Fetch the model number from the entry widget
        
        if not model_num_x:
            messagebox.showerror("Error", "Please enter a model number to search.")
            return
        
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()        
        try:
            c.execute("SELECT * FROM all_items_table WHERE model_num = ?", (model_num_x,))
            qty = c.fetchall()
            
            if qty:
                # Create a new window to display the results
                result_window = tk.Toplevel(self)
                result_window.title("Search Results")
                result_window.geometry("800x400")
                
                # Create a Treeview widget to display the results
                columns = ("Model Number", "Quantity")
                result_tree = ttk.Treeview(result_window, columns=columns, show="headings")
                
                for col in columns:
                    result_tree.heading(col, text=col)
                    result_tree.column(col, width=100)
                
                for qty in qty:
                    result_tree.insert("", "end", values=qty)
                
                result_tree.pack(fill="both", expand=True)
                
                # Add a scrollbar to the Treeview
                scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=result_tree.yview)
                result_tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side="right", fill="y")
                
                # Display total quantity
                total_label = tk.Label(result_window, text=f"Total quantity available for model number {qty[0]}: {qty[1]}", font=("TIMES NEW ROMAN", 12))
                total_label.pack(pady=10)
            else:
                messagebox.showinfo("Availability", f"No watches found matching model number {qty[0]}.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Model num donot exist Enter exact model num")
        
        finally:
            conn.close()

    def add_booking(self):
    
        # Validate inputs
        required_fields = [
            self.model_num_entry, self.customer_name_entry, self.contact_num_entry,
            self.watch_type_entry, self.quantity_entry, self.paid_amount_entry,self.remaining_amount_entry,
            self.total_amount_entry, self.date_entry
        ]
        
        for field in required_fields:
            if not field.get().strip():
                messagebox.showerror("Error", "All fields must be filled.")
                return
        model_num = required_fields[0].get().strip()
        quantity = required_fields[4].get().strip()
        if int(quantity) < 0:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM all_items_table WHERE MODEL_NUM = ?", (model_num,))
        if c.fetchone() is None:
            messagebox.showerror("Error", "Model Number does not exist.")
            return
        c.execute(f"SELECT QUANTITY FROM all_items_table WHERE MODEL_NUM = ?", (model_num,))
        qty = c.fetchone()
        conn.close()
        if int(quantity) > qty[0]:
            messagebox.showerror("Error", f"only {qty[0]} watches are available in stock.")
            return
        else:
            self.display_booking_records()

    def display_booking_records(self):
        # Get input values correctly as strings (not tuples)
        date = self.date_entry.get().strip()
        model_num = self.model_num_entry.get().strip()
        watch_type = self.watch_type_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        customer_name = self.customer_name_entry.get().strip()
        contact_num = self.contact_num_entry.get().strip()
        paid_amount = self.paid_amount_entry.get().strip()
        remaining_amount = self.remaining_amount_entry.get().strip()
        total_amount = self.total_amount_entry.get().strip()
        payment_type = self.payment_type_var.get().strip()
        profit = self.profit_entry.get().strip()

        # if model_num exist in bill_tree, update the quantity a
        for item in self.booking_tree.get_children():
            values = self.booking_tree.item(item, "values")
            if values[1] == model_num:
                total_qty = int(values[3]) + int(quantity)
                conn = sqlite3.connect('AL_Makkah_Watch.db')
                c = conn.cursor()
                c.execute("SELECT QUANTITY FROM all_items_table WHERE MODEL_NUM = ?", (model_num,))
                qty_in_db = c.fetchone()
                if qty_in_db[0] < total_qty:
                    messagebox.showerror("Error", f"Quantity Exceeding Available quantity in stock.")
                    return
                # Update the quantity and watch type    
                self.booking_tree.item(item, values=(
                values[0], 
                values[1], 
                values[2],
                str(int(values[3]) + int(quantity)),
                values[4], 
                values[5], 
                str(int(values[6]) + int(paid_amount) ),           # Remove the = sign
                str(int(values[7]) + int(remaining_amount)),      # Remove the = sign
                str(int(values[8]) + int(total_amount)),         # Remove the = sign
                values[9],                    # Remove the = sign
                str(int(values[10]) + int(profit))
                ))
                self.model_num_entry.delete(0, tk.END)
                self.watch_type_entry.delete(0, tk.END)
                self.total_amount_entry.delete(0, tk.END)
                self.remaining_amount_entry.delete(0, tk.END)
                self.paid_amount_entry.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
                self.profit_entry.delete(0, tk.END)
                return
            # clear the entry fields
        self.model_num_entry.delete(0, tk.END)
        self.watch_type_entry.delete(0, tk.END)
        self.total_amount_entry.delete(0, tk.END)
        self.remaining_amount_entry.delete(0, tk.END)
        self.paid_amount_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.profit_entry.delete(0, tk.END)
        # Insert new item into Treeview (ensuring a new row is created)    
        self.booking_tree.insert("", "end", values=(
        date, model_num, watch_type, quantity, 
        customer_name, contact_num, paid_amount, 
        remaining_amount, total_amount, payment_type, profit
    ))
   
    def delete_booking_record(self):
        selling_items = self.booking_tree.selection()
        
        if not selling_items:
            messagebox.showwarning("Warning", "Please select an Item to delete.")
            return
        
        # Remove from Treeview
        self.booking_tree.delete(selling_items)

        messagebox.showinfo("Success", "Item deleted successfully!")