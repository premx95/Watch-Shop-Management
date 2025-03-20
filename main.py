from tkinter import *
from STOCKSX import WatchInventorySystem
from BOOKINGXzzzzz import WatchBookingSystem
from TotalSaleXzzzzz import TotalSales
from losses import Losses
from EXPENSES_2 import expenses
from complain import complaint_repair_gui
from debtx import Debt

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Al Makkah Watch Management System")
        self.root.geometry("1200x700")

        # Create main container
        self.container = Frame(self.root)
        self.container.grid(row=1, column=0, sticky="nsew")

        # Allow the main container to expand
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create navbar
        self.create_navbar()

        self.frames = {}  # Dictionary to store different pages
        self.active_button = None  # Track the active button

        # Initialize first page
        self.add_page("Losses", Losses)
        self.add_page("Expenses", expenses)
        self.add_page("Complaints", complaint_repair_gui)
        self.add_page("Debt", Debt)
        self.add_page("Stocks and Inventory", WatchInventorySystem)
        self.add_page("Booking", WatchBookingSystem)
        self.add_page("Sales", TotalSales)

        # Show the Sales page initially and highlight its button
        self.show_frame("Sales")

    def add_page(self, name, page_function):
        # Create a new frame instance
        frame = page_function(self.container)
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")  # Ensures it expands properly

    def create_navbar(self):
        navbar = Frame(self.root, bg="gray")
        navbar.grid(row=0, column=0, sticky="ew")
        
        # Store buttons in a dictionary for later reference
        self.buttons = {}
        
        self.buttons["Sales"] = Button(navbar, text="SALES 🛒",
                                      command=lambda: self.show_frame("Sales"))
        self.buttons["Sales"].grid(row=0, column=0, padx=10, pady=5)
        
        self.buttons["Booking"] = Button(navbar, text="Bookings 📑",
                                        command=lambda: self.show_frame("Booking"))
        self.buttons["Booking"].grid(row=0, column=1, padx=10, pady=5)
        
        self.buttons["Stocks and Inventory"] = Button(navbar, text="Stocks and Inventory ",
                                                     command=lambda: self.show_frame("Stocks and Inventory"))
        self.buttons["Stocks and Inventory"].grid(row=0, column=2, padx=10, pady=5)
        
        self.buttons["Complaints"] = Button(navbar, text="COMPLAINTS AND REPAIRS 🛠️",
                                           command=lambda: self.show_frame("Complaints"))
        self.buttons["Complaints"].grid(row=0, column=3, padx=10, pady=5)
        
        self.buttons["Debt"] = Button(navbar, text="「 ✦ Debts ✦ 」📖",
                                     command=lambda: self.show_frame("Debt"))
        self.buttons["Debt"].grid(row=0, column=4, padx=10, pady=5)
        
        self.buttons["Expenses"] = Button(navbar, text="Expenses 💵",
                                         command=lambda: self.show_frame("Expenses"))
        self.buttons["Expenses"].grid(row=0, column=5, padx=10, pady=5)
        
        self.buttons["Losses"] = Button(navbar, text="Losses 📉",
                                       command=lambda: self.show_frame("Losses"))
        self.buttons["Losses"].grid(row=0, column=6, padx=10, pady=5)

    def show_frame(self, name):
        # First reset all buttons to normal background
        for button_name, button in self.buttons.items():
            button.config(bg="SystemButtonFace", fg="black")  # Default button color
        
        # Highlight the selected button
        self.buttons[name].config(bg="#007BFF", fg="white")  # Blue background with white text
        
        # Show the selected frame
        frame = self.frames[name]
        frame.tkraise()  # Raise the frame to the top

if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()