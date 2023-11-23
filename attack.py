import tkinter as tk
import struct
import binascii
from sha_256 import Sha256Hash  # Assuming your custom SHA-256 implementation is in a file named "sha256.py"

def sha256_padding(length):
    # Padding function for SHA-256
    padding = b'\x80'
    while (length + len(padding)) % 64 != 56:
        padding += b'\x00'
    return padding + struct.pack('>Q', length * 8)
IV = [
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
]
def calculate_sha256_attack():
    try:
    # Function to perform the length extension attack
        initialState = IV  # Initial state for SHA-256 after processing the original message
        originalLength = len(entry.get().encode('utf-8'))  # Original message length
        padding = sha256_padding(originalLength)
        append = append_entry.get()  # Get the text to append

        hasher = Sha256Hash(initialState, originalLength + len(padding))
        hasher.update(append.encode('utf-8'))
        hashed_text = binascii.hexlify(hasher.digest()).decode('utf-8')

        output.delete(0, tk.END)
        output.insert(tk.END, hashed_text)
    except Exception as e:
        print("Error occurred:", e)

def clear_input():
    entry.delete(0, tk.END)
    append_entry.delete(0, tk.END)
    output.delete(0, tk.END)

root = tk.Tk()
root.title("SHA-256 Hash Calculator")

# Input Field
label = tk.Label(root, text="Enter Hash:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Original Hash value 
og_button = tk.Button(root, text = "Perform SHA-256 encryption", command = Sha256Hash)
og_button.pack()

# Append Field
append_label = tk.Label(root, text="Enter Extra Data:")
append_label.pack()
append_entry = tk.Entry(root)
append_entry.pack()

# Calculate Button (for length extension attack)
attack_button = tk.Button(root, text="Perform Length Extension Attack", command=calculate_sha256_attack)
attack_button.pack()

# Output Field
output_label = tk.Label(root, text="SHA-256 Hash:")
output_label.pack()
output = tk.Entry(root)
output.pack()

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack()

root.mainloop()
