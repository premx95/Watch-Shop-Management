import tkinter as tk
import random
import string

# Function to generate a password based on user preferences
def generate_password():
    # Get the desired password length from the entry widget
    try:
        password_length = int(length_entry.get())
        if password_length <= 0:
            result_label.config(text="Please enter a positive number")
            return
    except ValueError:
        result_label.config(text="Please enter a valid number")
        return
    
    # Initialize an empty character pool
    char_pool = ""
    
    # Add character types to the pool based on user selection
    if include_lowercase.get():
        char_pool += string.ascii_lowercase  # abcdefghijklmnopqrstuvwxyz
    if include_uppercase.get():
        char_pool += string.ascii_uppercase  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    if include_numbers.get():
        char_pool += string.digits  # 0123456789
    if include_symbols.get():
        char_pool += string.punctuation  # !@#$%^&*()-_=+[]{}|;:,.<>?/
    
    # Check if at least one character type is selected
    if not char_pool:
        result_label.config(text="Please select at least one character type")
        return
    
    # Generate password by randomly selecting characters from the pool
    password = ""
    for _ in range(password_length):
        # Choose a random character from the pool and add it to the password
        password += random.choice(char_pool)
    
    # Update the result label with the generated password
    result_label.config(text=password)
    
    # Copy password to clipboard
    window.clipboard_clear()
    window.clipboard_append(password)
    
    # Show a message that password was copied
    copy_label.config(text="Password copied to clipboard!")

# Create the main window
window = tk.Tk()
window.title("Password Generator")
window.geometry("1000x750")
window.resizable(False, False)

# Create a frame to hold the content
main_frame = tk.Frame(window, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# Create title label
title_label = tk.Label(main_frame, text="Strong Password Generator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Create length selection section
length_frame = tk.Frame(main_frame)
length_frame.pack(pady=15, fill="x")

length_label = tk.Label(length_frame, text="Password Length:", font=("Arial", 12))
length_label.pack(side="left", padx=5)

length_entry = tk.Entry(length_frame, width=5, font=("Arial", 12))
length_entry.pack(side="left", padx=5)
length_entry.insert(0, "12")  # Default length

# Create character options with checkboxes
options_label = tk.Label(main_frame, text="Include:", font=("Arial", 12))
options_label.pack(anchor="w", pady=(15, 5))

# Create variables to track checkbox states
include_lowercase = tk.BooleanVar(value=True)
include_uppercase = tk.BooleanVar(value=True)
include_numbers = tk.BooleanVar(value=True)
include_symbols = tk.BooleanVar(value=True)

# Create and place checkboxes
lowercase_check = tk.Checkbutton(main_frame, text="Lowercase Letters (a-z)", 
                                variable=include_lowercase, font=("Arial", 11))
lowercase_check.pack(anchor="w", pady=2)

uppercase_check = tk.Checkbutton(main_frame, text="Uppercase Letters (A-Z)", 
                                variable=include_uppercase, font=("Arial", 11))
uppercase_check.pack(anchor="w", pady=2)

numbers_check = tk.Checkbutton(main_frame, text="Numbers (0-9)", 
                               variable=include_numbers, font=("Arial", 11))
numbers_check.pack(anchor="w", pady=2)

symbols_check = tk.Checkbutton(main_frame, text="Special Characters (!@#$%...)", 
                              variable=include_symbols, font=("Arial", 11))
symbols_check.pack(anchor="w", pady=2)

# Create generate button
generate_button = tk.Button(main_frame, text="Generate Password", 
                          command=generate_password, font=("Arial", 12, "bold"),
                          bg="#4CAF50", fg="white", padx=10, pady=5)
generate_button.pack(pady=20)

# Create label to display the generated password
result_label = tk.Label(main_frame, text="", font=("Arial", 14), 
                       bg="#f0f0f0", padx=10, pady=10, relief="sunken", width=25)
result_label.pack(pady=10)

# Create label to show copy confirmation
copy_label = tk.Label(main_frame, text="", font=("Arial", 10, "italic"), fg="#555555")
copy_label.pack(pady=5)

# Add a helpful text at the bottom
help_text = tk.Label(main_frame, text="For a strong password, use at least 12 characters\nwith a mix of all character types.", 
                    font=("Arial", 10), fg="#555555")
help_text.pack(pady=10)

# Start the main event loop
window.mainloop()