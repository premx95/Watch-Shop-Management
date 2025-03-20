import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
from datetime import datetime
import win32api
import tempfile

class TotalSales(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")

        # Set theme and colors
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2c3e50"  # Dark blue/gray
        self.bg_color = "#ecf0f1"  # Light gray
        self.accent_color = "#e74c3c"  # Red
        
        self.configure(bg=self.bg_color)
        
        # Create tables
        self.create_sales_table()
        
        # Setup UI
        self.setup_ui()

    def create_sales_table(self):
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        # Don't drop the table every time - this is what's causing your data loss
        # c.execute("""DROP TABLE IF EXISTS sales_table""")
        c.execute("""CREATE TABLE IF NOT EXISTS sales_table
                    (date TEXT, 
                     model_num TEXT,
                     quantity INTEGER,
                     Total_Price INTEGER,
                     profit_entry INTEGER,
                     payment_type TEXT)""")
        conn.commit()
        conn.close()

    def setup_ui(self):
        # Create header
        header_frame = tk.Frame(self, bg=self.secondary_color, height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="AL MAKKAH WATCH - SALES DASHBOARD", 
                              font=("Arial", 18, "bold"), bg=self.secondary_color, fg="white")
        title_label.pack(pady=10)
        
        # Main content frame
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Input frame
        input_frame = tk.LabelFrame(main_frame, text="Sales Information", font=("Arial", 12, "bold"), 
                                   bg=self.bg_color, fg=self.secondary_color, padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Create a consistent style for labels and entries
        label_style = {"font": ("Arial", 10), "bg": self.bg_color, "fg": self.secondary_color}
        entry_style = {"font": ("Arial", 10), "relief": tk.GROOVE, "bd": 2}
        button_style = {"font": ("Arial", 10, "bold"), "bg": self.primary_color, 
                       "fg": "white", "relief": tk.RAISED, "bd": 1, "padx": 10, "pady": 5}
        
        # Row 1
        row1 = tk.Frame(input_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(row1, text="Date (YYYY-MM-DD):", **label_style).pack(side=tk.LEFT, padx=5)
        self.date_entry = tk.Entry(row1, width=15, **entry_style)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.bind("<Return>", self.on_enter)
        
        tk.Label(row1, text="Model Number:", **label_style).pack(side=tk.LEFT, padx=5)
        self.model_num_entry = tk.Entry(row1, width=25, **entry_style)
        self.model_num_entry.pack(side=tk.LEFT, padx=5)
        self.model_num_entry.bind("<Return>", self.on_enter)
        
        tk.Label(row1, text="Quantity:", **label_style).pack(side=tk.LEFT, padx=5)
        self.quantity_entry = tk.Entry(row1, width=10, **entry_style)
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.bind("<Return>", self.on_enter)
        
        # Row 2
        row2 = tk.Frame(input_frame, bg=self.bg_color)
        row2.pack(fill=tk.X, pady=5)
        
        tk.Label(row2, text="Price:", **label_style).pack(side=tk.LEFT, padx=5)
        self.price_entry = tk.Entry(row2, width=15, **entry_style)
        self.price_entry.pack(side=tk.LEFT, padx=5)
        self.price_entry.bind("<Return>", self.on_enter)
        
        tk.Label(row2, text="Profit:", **label_style).pack(side=tk.LEFT, padx=5)
        self.profit_entry = tk.Entry(row2, width=15, **entry_style)
        self.profit_entry.pack(side=tk.LEFT, padx=5)
        self.profit_entry.bind("<Return>", self.on_enter)
        
        tk.Label(row2, text="Payment Type:", **label_style).pack(side=tk.LEFT, padx=5)
        self.payment_type_var = StringVar()
        payment_type_options = ["Cash", "Account"]
        
        self.payment_type_menu = ttk.Combobox(row2, textvariable=self.payment_type_var, values=payment_type_options, state="readonly")
        self.payment_type_menu.pack(side=tk.LEFT, padx=5)
        self.payment_type_var.set(payment_type_options[0])
        
        # Button Frame
        button_frame = tk.Frame(input_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=10)
        
        add_button = tk.Button(button_frame, text="Add Item", command=self.validate_inputs, bg="light green")
        add_button.pack(side=tk.LEFT, padx=400)
        
        
        
        # Bill items frame
        bill_label_frame = tk.LabelFrame(main_frame, text="Current Sale Items", font=("Arial", 12, "bold"), 
                                       bg=self.bg_color, fg=self.secondary_color)
        bill_label_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tree_view for bill items
        style = ttk.Style()
        style.configure("Treeview", background=self.bg_color, foreground=self.secondary_color, rowheight=25, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", self.primary_color)])
        
        # Create scrollbar
        tree_scroll = ttk.Scrollbar(bill_label_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.bill_frame = ttk.Treeview(bill_label_frame, columns=("Date", "Model Number", "Quantity", "Price", "Profit", "payment_type"), 
                                      show="headings", yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.bill_frame.yview)

                # BUTTON in bill frame
        self.bill_frame.pack(fill=tk.BOTH, expand=True)

        # Button frame (centered)
        button_frame = tk.Frame(bill_label_frame, bg=self.bg_color)
        button_frame.pack(pady=10)  # Center the frame

        # Buttons inside the frame, arranged in a row
        view_button = tk.Button(button_frame, text="View Sales Record", command=self.sales_record_table, bg="orange")
        view_button.pack(side=tk.LEFT, padx=10)  # Adds spacing between buttons

        delete_button = tk.Button(button_frame, text="Delete Selected Item", command=self.delete_item_from_bill, bg="#F44336")
        delete_button.pack(side=tk.LEFT, padx=10)

        print_button = tk.Button(button_frame, text="「 ✦ PRINT BILL ✦ 」", command=self.print_data, **button_style)
        print_button.pack(side=tk.LEFT, padx=10)
        

        # Configure treeview columns
        self.bill_frame.heading("Date", text="Date")
        self.bill_frame.heading("Model Number", text="Model Number")
        self.bill_frame.heading("Quantity", text="Quantity")
        self.bill_frame.heading("Price", text="Price")
        self.bill_frame.heading("Profit", text="Profit")
        self.bill_frame.heading("payment_type", text="Payment Type")
        
        # Set column widths
        self.bill_frame.column("Date", width=100)
        self.bill_frame.column("Model Number", width=150)
        self.bill_frame.column("Quantity", width=80)
        self.bill_frame.column("Price", width=100)
        self.bill_frame.column("Profit", width=100)
        self.bill_frame.column("payment_type", width=100)
        
        self.bill_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        
        # Status bar
        status_frame = tk.Frame(self, bg=self.secondary_color, height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = tk.Label(status_frame, text="Ready", font=("Arial", 9), bg=self.secondary_color, fg="white")
        status_label.pack(side=tk.LEFT, padx=10, pady=5)

    def delete_item_from_bill(self):
        deleting_item = self.bill_frame.selection()
        if deleting_item:
            if messagebox.askyesno("Delete item!", f"Are you sure you want to delete {deleting_item}?"):
                self.bill_frame.delete(deleting_item)
        else:
            messagebox.showinfo("Error", "Please select an item to delete.")

    def sales_record_table(self):
        # Create new window for sales record with improved design
        self.sales_record_window = tk.Toplevel()
        self.sales_record_window.title("Sales Record History")
        self.sales_record_window.geometry("1200x700")
        self.sales_record_window.configure(bg=self.bg_color)
        
        # Header
        header_frame = tk.Frame(self.sales_record_window, bg=self.secondary_color, height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="SALES RECORD HISTORY", 
                              font=("Arial", 18, "bold"), bg=self.secondary_color, fg="white")
        title_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.sales_record_window, bg=self.bg_color)

        daily_btn = tk.Button(button_frame, text="Daily Sales", command=self.daily_sales,
                               font=("Arial", 10, "bold"), bg=self.primary_color, fg="white", 
                               relief=tk.RAISED, bd=1, padx=10, pady=5)
        daily_btn.pack(side=tk.LEFT, padx=5)

        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        monthly_btn = tk.Button(button_frame, text="Monthly Profit Analysis", command=self.monthly_profit,
                               font=("Arial", 10, "bold"), bg=self.primary_color, fg="white", 
                               relief=tk.RAISED, bd=1, padx=10, pady=5)
        monthly_btn.pack(side=tk.LEFT, padx=5)

        yearly_btn = tk.Button(button_frame, text="Yearly Sales", command=self.yearly_sales,
                               font=("Arial", 10, "bold"), bg=self.primary_color, fg="white", 
                               relief=tk.RAISED, bd=1, padx=10, pady=5)
        yearly_btn.pack(side=tk.LEFT, padx=5)

        booked_sales = tk.Button(button_frame, text="Booked Sales", command=self.display_booked_sales,
                                font=("Arial", 10, "bold"), bg=self.primary_color, fg="white", 
                                relief=tk.RAISED, bd=1, padx=10, pady=5)
        booked_sales.pack(side=tk.LEFT, padx=5)
        
        per_Day_sales_button = tk.Button(button_frame, text="Per Day Sales", command=self.per_day_sales,
                                font=("Arial", 10, "bold"), bg=self.primary_color, fg="white", 
                                relief=tk.RAISED, bd=1, padx=10, pady=5)
        per_Day_sales_button.pack(side=tk.LEFT, padx=5)


        # Create frame for treeview
        records_frame = tk.Frame(self.sales_record_window, bg=self.bg_color)
        records_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollbar
        tree_scroll_y = ttk.Scrollbar(records_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(records_frame, orient="horizontal")
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", background=self.bg_color, foreground=self.secondary_color, rowheight=25, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", self.primary_color)])
        
        # Create treeview
        self.sales_record_frame = ttk.Treeview(records_frame, 
                                             columns=("Date", "Model Number", "Quantity", "Price", "Profit", "payment_type"), 
                                             show="headings", 
                                             yscrollcommand=tree_scroll_y.set,
                                             xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.sales_record_frame.yview)
        tree_scroll_x.config(command=self.sales_record_frame.xview)
        
        # Configure columns
        self.sales_record_frame.heading("Date", text="Date")
        self.sales_record_frame.heading("Model Number", text="Model Number")
        self.sales_record_frame.heading("Quantity", text="Quantity")
        self.sales_record_frame.heading("Price", text="Price")
        self.sales_record_frame.heading("Profit", text="Profit")
        self.sales_record_frame.heading("payment_type", text="Payment Type")
        
        self.sales_record_frame.column("Date", width=100)
        self.sales_record_frame.column("Model Number", width=150)
        self.sales_record_frame.column("Quantity", width=80)
        self.sales_record_frame.column("Price", width=100)
        self.sales_record_frame.column("Profit", width=100)
        self.sales_record_frame.column("payment_type", width=100)
        
        self.sales_record_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fetch data from database and display
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sales_table ORDER BY date DESC")
        sales_records = c.fetchall()
        for record in sales_records:
            self.sales_record_frame.insert("", "end", values=record)
        conn.close()
        
        # Status bar with summary
        status_frame = tk.Frame(self.sales_record_window, bg=self.secondary_color, height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Calculate totals for status bar
        total_records = len(sales_records)
        total_sales = sum(float(record[3]) for record in sales_records) if sales_records else 0
        total_profit = sum(float(record[4]) for record in sales_records) if sales_records else 0
        
        status_label = tk.Label(status_frame, 
                              text=f"Total Records: {total_records} | Total Sales: {total_sales:.2f} | Total Profit: {total_profit:.2f}", 
                              font=("Arial", 9), bg=self.secondary_color, fg="white")
        status_label.pack(side=tk.LEFT, padx=10, pady=5)

    def monthly_profit(self):
        # Create a stylish window for monthly analysis
        monthly_win = tk.Toplevel()
        monthly_win.title("Monthly Profit Analysis")
        monthly_win.geometry("500x500")
        monthly_win.configure(bg=self.bg_color)
        
        # Header
        header_frame = tk.Frame(monthly_win, bg=self.secondary_color, height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="MONTHLY PROFIT ANALYSIS", 
                             font=("Arial", 16, "bold"), bg=self.secondary_color, fg="white")
        title_label.pack(pady=10)
        
        # Database connection
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''SELECT strftime('%Y-%m', DATE(date)) AS month, SUM(profit_entry) 
                    FROM sales_table GROUP BY month ORDER BY DATE(date) DESC''')
        rows = c.fetchall()
        conn.close()
        
        # Create main frame
        main_frame = tk.Frame(monthly_win, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollbar
        tree_scroll = ttk.Scrollbar(main_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", background=self.bg_color, foreground=self.secondary_color, rowheight=25, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", self.primary_color)])
        
        # Create treeview
        tree = ttk.Treeview(main_frame, columns=('Month', 'Total Profit'), show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('Month', text='Month')
        tree.heading('Total Profit', text='Total Profit (PKR)')
        
        tree.column('Month', width=150, anchor='center')
        tree.column('Total Profit', width=200, anchor='center')
        
        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Insert monthly totals
        total_profit = 0
        for row in rows:
            month = row[0]
            profit = row[1]
            total_profit += profit
            tree.insert('', 'end', values=(month, f"{profit:,.2f}"))

        # Summary frame
        summary_frame = tk.Frame(monthly_win, bg=self.bg_color, padx=20, pady=10)
        summary_frame.pack(fill=tk.X)
        
        tk.Label(summary_frame, text=f"Total Profit All Time: {total_profit:,.2f} PKR", 
               font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.secondary_color).pack()
        
    def monthly_profit_bookings(self):
        # Create a stylish window for monthly analysis
        monthly_win = tk.Toplevel()
        monthly_win.title("Monthly Profit Analysis")
        monthly_win.geometry("500x500")
        monthly_win.configure(bg=self.bg_color)
        
        # Header
        header_frame = tk.Frame(monthly_win, bg=self.secondary_color, height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="MONTHLY PROFIT ANALYSIS", 
                             font=("Arial", 16, "bold"), bg=self.secondary_color, fg="white")
        title_label.pack(pady=10)
        
        # Database connection
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''SELECT strftime('%Y-%m', DATE(DATE)) AS month, SUM(PROFIT) 
                    FROM booked_sales GROUP BY month ORDER BY DATE(date) DESC''')
        rows = c.fetchall()
        conn.close()
        
        # Create main frame
        main_frame = tk.Frame(monthly_win, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollbar
        tree_scroll = ttk.Scrollbar(main_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", background=self.bg_color, foreground=self.secondary_color, rowheight=25, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", self.primary_color)])
        
        # Create treeview
        tree = ttk.Treeview(main_frame, columns=('Month', 'Total Profit'), show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('Month', text='Month')
        tree.heading('Total Profit', text='Total Profit (PKR)')
        
        tree.column('Month', width=150, anchor='center')
        tree.column('Total Profit', width=200, anchor='center')
        
        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Insert monthly totals
        total_profit = 0
        for row in rows:
            month = row[0]
            profit = row[1]
            total_profit += profit
            tree.insert('', 'end', values=(month, f"{profit:,.2f}"))

        # Summary frame
        summary_frame = tk.Frame(monthly_win, bg=self.bg_color, padx=20, pady=10)
        summary_frame.pack(fill=tk.X)
        
        tk.Label(summary_frame, text=f"Total Profit All Time: {total_profit:,.2f} PKR", 
               font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.secondary_color).pack()
        

    def display_booked_sales(self):
        # Create a new window for booking records
        self.new_window = tk.Toplevel(self)
        self.new_window.title("Booked sales")
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
             
        # Fetch data from the database and display in booking_records_tree
        try:
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()

            c.execute('SELECT * FROM booked_sales ORDER BY DATE DESC')   
            rows = c.fetchall()

            for row in rows:
                self.booking_records_tree.insert("", "end", values=row)

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error fetching the Details")  # Print error message if there's an issue     

        #       ADD BUTTON
        monthly_booking_profit = tk.Button(self.new_window, text="Monthly Bookings Profit", command=self.monthly_profit_bookings,
                                font=("Arial", 10, "bold"), bg=self.primary_color, fg="white", 
                                relief=tk.RAISED, bd=1, padx=10, pady=5)
        monthly_booking_profit.pack(side="left")
        
    def daily_sales(self):
        # Create a stylish window for monthly analysis
        monthly_win = tk.Toplevel()
        monthly_win.title("Per Day Sales Analysis")
        monthly_win.geometry("500x500")
        monthly_win.configure(bg=self.bg_color)
        
        # Header
        header_frame = tk.Frame(monthly_win, bg=self.secondary_color, height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Per Day Sales Analysis", 
                             font=("Arial", 16, "bold"), bg=self.secondary_color, fg="white")
        title_label.pack(pady=10)
        
        # Database connection
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''SELECT strftime('%Y-%m-%d', DATE(date)) AS day, SUM(profit_entry) 
                    FROM sales_table GROUP BY day ORDER BY DATE(date) DESC''')
        rows = c.fetchall()
        conn.close()
        
        # Create main frame
        main_frame = tk.Frame(monthly_win, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollbar
        tree_scroll = ttk.Scrollbar(main_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", background=self.bg_color, foreground=self.secondary_color, rowheight=25, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", self.primary_color)])
        
        # Create treeview
        tree = ttk.Treeview(main_frame, columns=('Date', 'Total Profit'), show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('Date', text='Date')
        tree.heading('Total Profit', text='Total Profit (PKR)')
        
        tree.column('Date', width=150, anchor='center')
        tree.column('Total Profit', width=200, anchor='center')
        
        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Insert monthly totals
        total_profit = 0
        for row in rows:
            date = row[0]
            profit = row[1]
            total_profit += profit
            tree.insert('', 'end', values=(date, f"{profit:,.2f}"))

        # Summary frame
        summary_frame = tk.Frame(monthly_win, bg=self.bg_color, padx=20, pady=10)
        summary_frame.pack(fill=tk.X)
        
        tk.Label(summary_frame, text=f"Total Profit All Time: {total_profit:,.2f} PKR", 
               font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.secondary_color).pack()

    def yearly_sales(self):
        # Create a stylish window for monthly analysis
        monthly_win = tk.Toplevel()
        monthly_win.title("Per year Sales Analysis")
        monthly_win.geometry("500x500")
        monthly_win.configure(bg=self.bg_color)
        
        # Header
        header_frame = tk.Frame(monthly_win, bg=self.secondary_color, height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Per Year Sales Analysis", 
                             font=("Arial", 16, "bold"), bg=self.secondary_color, fg="white")
        title_label.pack(pady=10)
        
        # Database connection
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''SELECT strftime('%Y', DATE(date)) AS year, SUM(profit_entry) 
                    FROM sales_table GROUP BY year ORDER BY DATE(date) DESC''')
        rows = c.fetchall()
        conn.close()
        
        # Create main frame
        main_frame = tk.Frame(monthly_win, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollbar
        tree_scroll = ttk.Scrollbar(main_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", background=self.bg_color, foreground=self.secondary_color, rowheight=25, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", self.primary_color)])
        
        # Create treeview
        tree = ttk.Treeview(main_frame, columns=('Year', 'Total Profit'), show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('Year', text='Year')
        tree.heading('Total Profit', text='Total Profit (PKR)')
        
        tree.column('Year', width=150, anchor='center')
        tree.column('Total Profit', width=200, anchor='center')
        
        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Insert monthly totals
        total_profit = 0
        for row in rows:
            Year = row[0]
            profit = row[1]
            total_profit += profit
            tree.insert('', 'end', values=(Year, f"{profit:,.2f}"))

        # Summary frame
        summary_frame = tk.Frame(monthly_win, bg=self.bg_color, padx=20, pady=10)
        summary_frame.pack(fill=tk.X)
        
        tk.Label(summary_frame, text=f"Total Profit All Time: {total_profit:,.2f} PKR", 
               font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.secondary_color).pack()

    def save_sales_record(self):
        # Save sales record to database
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        for child in self.bill_frame.get_children():
            values = self.bill_frame.item(child, "values")
            c.execute("INSERT INTO sales_table VALUES (?, ?, ?, ?, ?, ?)", values)
            c.execute("UPDATE all_items_table SET quantity = quantity - ? WHERE model_num = ?", (values[2], values[1]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Sales record saved successfully.")

    def print_data(self):

        #before printing the check_availability of the quantity of the model_num
        for item in self.bill_frame.get_children():
            values = self.bill_frame.item(item, "values")
            model_num = values[1]
            quantity = int(values[2])
            
            # Verify stock availability one final time
            conn = sqlite3.connect('AL_Makkah_Watch.db')
            c = conn.cursor()
            try:
                c.execute("SELECT quantity FROM all_items_table WHERE model_num = ?", (model_num,))
                result = c.fetchone()
                if result:
                    qty_in_stock = result[0]
                    if qty_in_stock < quantity:
                        messagebox.showerror("Error", 
                            f"Model {model_num} only has {qty_in_stock} items available.")
                        conn.close()
                        return
                else:
                    messagebox.showerror("Error", f"Model {model_num} not found in inventory.")
                    conn.close()
                    return
            finally:
                conn.close()

            bill_content = ""
            total_amount = int(0)
            # Get current date
            date = datetime.now().strftime("%d-%b-%Y")

            # Header
            bill_content += "========================================\n"
            bill_content += "       Al Makkah Watch Sales Bill     \n"
            bill_content += "========================================\n"
            bill_content += f"Printed on: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}\n"
            bill_content += "----------------------------------------\n"
            bill_content += "Model No      Quantity      Price  \n"
            bill_content += "----------------------------------------\n"
            for item in self.bill_frame.get_children():
                values = self.bill_frame.item(item, "values")
                bill_content += f"{values[1]:<13} {values[2]:<13} {values[3]:<13}\n"
                total_amount += int(values[3]) if values[3] else 0
            payment_type = values[5]
            bill_content += "----------------------------------------\n"
            bill_content += f"Total Amount: {total_amount}\n"
            bill_content += f"Payment Type: {payment_type}\n"
            bill_content += "========================================\n"
            bill_content += "     Thank You for Your Purchase!      \n"
            bill_content += "========================================\n"
            bill_content += "سمارٹ واچ واپس یا تبدیل نہ ہو گی۔\n"
            bill_content += "سمارٹ واچ پر گارنٹی لاگو نہیں۔\n"
            bill_content += "گارنٹی والی آئٹم کی گارنٹی صرف مشینری تک محدود ہو گی۔\n"
            bill_content += "بغیر بل کے کوئی کلیم قابل قبول نہیں۔\n"

        if not self.bill_frame.get_children():
            messagebox.showwarning("Warning", "No bill content to print.")
            return

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
            
        self.save_sales_record()
        self.bill_frame.delete(*self.bill_frame.get_children())

    def insert_item_into_bill_tree(self):
        date = self.date_entry.get()
        model_num = self.model_num_entry.get()
        qty = self.quantity_entry.get()
        if int(qty) < 0:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return
        watch_price = self.price_entry.get()
        profit = self.profit_entry.get()
        payment_type = self.payment_type_var.get()
        
        # if model_num exist in bill_label_frame, update the quantity,PRICE and profit
        for child in self.bill_frame.get_children():
            values = self.bill_frame.item(child, "values")
            if values[1] == model_num:
                self.bill_frame.item(child, values=(values[0], values[1], str(int(values
                [2]) + int(qty)), str(int(values[3]) + int(watch_price)), str(int(values[4]) + int(profit)), values[5]))
                break
        else:
            self.bill_frame.insert("", "end", values=(date, model_num, qty, watch_price, profit, payment_type))
            

        # Clear entries after insertion
        self.model_num_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.profit_entry.delete(0, tk.END)
        self.model_num_entry.focus()

    def validate_inputs(self):
        if not self.validate_date(self.date_entry.get()):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
            
        # Validate model number
        qty = self.check_availability()
        if qty != True:
            return

        try:
            int(self.price_entry.get())
        except:
            messagebox.showerror("Error", "Price must be a number")
            return

        try:
            int(self.profit_entry.get())
        except:
            messagebox.showerror("Error", "Profit must be a number")
            return
            
        self.insert_item_into_bill_tree() 
    
    def on_enter(self, event):
        widget = event.widget
        widget.tk_focusNext().focus()
        
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def per_day_sales(self):
        # Create a stylish window for monthly analysis
        monthly_win = tk.Toplevel()
        monthly_win.title("Per Day Sales Analysis")
        monthly_win.geometry("500x500")
        monthly_win.configure(bg=self.bg_color)
        
        # Header
        header_frame = tk.Frame(monthly_win, bg=self.secondary_color, height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Per Day Sales Analysis", 
                            font=("Arial", 16, "bold"), bg=self.secondary_color, fg="white")
        title_label.pack(pady=10)
        
        # Database connection
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        c.execute('''SELECT strftime('%Y-%m-%d', DATE(date)) AS day, 
                    SUM(Total_Price), 
                    COUNT(*) AS total_sales
             FROM sales_table 
             GROUP BY day 
             ORDER BY DATE(date) DESC''')
        rows = c.fetchall()
        conn.close()
        
        # Create main frame
        main_frame = tk.Frame(monthly_win, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create scrollbar
        tree_scroll = ttk.Scrollbar(main_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", background=self.bg_color, foreground=self.secondary_color, rowheight=25, fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", self.primary_color)])
        
        # Create treeview
        tree = ttk.Treeview(main_frame, columns=('Date', 'Total Price', 'No Of Sales'), show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('Date', text='Date')
        tree.heading('Total Price', text='Total Price (PKR)')
        tree.heading('No Of Sales', text='No Of Sales')
        
        tree.column('Date', width=150, anchor='center')
        tree.column('Total Price', width=200, anchor='center')
        tree.column('No Of Sales', width=150, anchor='center')

        
        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Insert monthly totals
        total_price = 0
        for row in rows:
            date = row[0]
            price = row[1]
            sales = row[2]
            total_price += price
            tree.insert('', 'end', values=(date, f"{price:,.2f}", sales))

        # Summary frame
        summary_frame = tk.Frame(monthly_win, bg=self.bg_color, padx=20, pady=10)
        summary_frame.pack(fill=tk.X)
        
        tk.Label(summary_frame, text=f"Total Sales All time: {total_price:,.2f} PKR", 
            font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.secondary_color).pack()
        
    def check_availability(self):
        model_num = self.model_num_entry.get()
        if not model_num:
            messagebox.showerror("Error", "Please enter a Model Number.")
            return
            
        conn = sqlite3.connect('AL_Makkah_Watch.db')
        c = conn.cursor()
        
        qty_in_stock = None
        
        try:
            c.execute("SELECT * FROM all_items_table WHERE model_num =?", (model_num,))
            result = c.fetchone()
            if result:
                qty_in_stock = result[1]
                if qty_in_stock <= 0:
                    messagebox.showerror("Error", f"Model number: {model_num} out of stock.")
                    return None
                if int(self.quantity_entry.get()) > qty_in_stock:
                    messagebox.showerror("Error", f"Only {qty_in_stock} items available, cancel bookings or add stock")
                    return None
            else:
                messagebox.showerror("Error", f"{model_num} not found")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"{model_num} not found")
            return None
        finally:
            conn.close()
            
        return True
