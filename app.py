import hashlib
import tkinter as tk
import struct
import binascii
from sha1 import Sha1Hash  # Assuming your custom SHA1 implementation is in a file named "sha1.py"

def sha1padding(length):
    # Function to generate padding for the SHA-1 length extension attack
    # ... (Your sha1padding function implementation goes here)
    padding = b""
    blocksize = 64
    r = (length % blocksize)
    padding = padding + b'\x80'
    if(r >= 56 and r <=59):
        padding = padding + (64*b'\x00')
    while r != 59:
        padding = padding + b'\x00'
        r = (r + 1) % 64 

    bitlength = length*8
    padding = padding + struct.pack(">i",bitlength)
    return padding

def calculate_sha1_attack():
    # Function to perform the length extension attack
    initialState = "67452301efcdab8998badcfe10325476c3d2e1f0"  # Initial state for normal SHA1 computation
    originalLength = len(entry.get().encode('utf-8'))  # Original message length
    padding = sha1padding(originalLength)
    append = append_entry.get()  # Get the text to append

    hasher = Sha1Hash(initialState, originalLength + len(padding))
    hasher.update(bytes(append, 'utf-8'))
    hashed_text = binascii.hexlify(hasher.digest()).decode('utf-8')

    output.delete(0, tk.END)
    output.insert(tk.END, hashed_text)

def clear_input():
    entry.delete(0, tk.END)
    append_entry.delete(0, tk.END)
    output.delete(0, tk.END)  # Clear input and output fields

root = tk.Tk()
root.title("SHA-1 Hash Calculator")

# Input Field
label = tk.Label(root, text="Enter text:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Append Field
append_label = tk.Label(root, text="Text to append:")
append_label.pack()
append_entry = tk.Entry(root)
append_entry.pack()

# Calculate Button (for length extension attack)
attack_button = tk.Button(root, text="Perform Length Extension Attack", command=calculate_sha1_attack)
attack_button.pack()

# Output Field
output_label = tk.Label(root, text="SHA-1 Hash:")
output_label.pack()
output = tk.Entry(root)
output.pack()

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack()

root.mainloop()

