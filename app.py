import hashlib
import tkinter as tk

def calculate_sha1():
    input_text = entry.get()
    sha1 = hashlib.sha1()
    sha1.update(input_text.encode('utf-8'))
    hashed_text = sha1.hexdigest()
    output.delete(0, tk.END)
    output.insert(tk.END, hashed_text)

def clear_input():
    entry.delete(0, tk.END)
    output.delete(0, tk.END)  # Clear both input and output fields

root = tk.Tk()
root.title("SHA-1 Hash Calculator")

# Input Field
label = tk.Label(root, text="Enter text:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Calculate Button
calculate_button = tk.Button(root, text="Calculate SHA-1", command=calculate_sha1)
calculate_button.pack()

# Output Field
output_label = tk.Label(root, text="SHA-1 Hash:")
output_label.pack()
output = tk.Entry(root)
output.pack()

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack()

root.mainloop()
