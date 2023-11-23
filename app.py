import tkinter as tk
import struct
#import binascii
import os
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

def calculate_mac_length_extension():
    original_message = entry.get()  # Get the original message from user input
    additional_data = additional_entry.get()  # Get additional data from user input

    # Generate a random key (16 bytes) for the MAC
    key = os.urandom(16)

    # Calculate the initial state and original message length for SHA1 computation
    initial_state = "67452301efcdab8998badcfe10325476c3d2e1f0"  # Initial state for normal SHA1 computation
    original_message_length = len(original_message.encode('utf-8'))

    # Generate padding for the original message
    padding = sha1padding(original_message_length)

    # Compute the MAC for the original message using SHA-1
    hasher = Sha1Hash(initial_state, original_message_length + len(padding))
    hasher.update(key + bytes(original_message, 'utf-8'))  # Key is prepended to the message
    original_mac = hasher.hexdigest()

    # Simulate length extension attack by appending additional data
    hasher2 = Sha1Hash(initial_state, original_message_length + len(key) + len(sha1padding(len(key) + original_message_length)))
    hasher2.update(bytes(additional_data, 'utf-8'))  # Append additional data to the original message
    extended_mac = hasher2.hexdigest()

    # Display the results in separate output fields
    original_output.config(state='normal')
    original_output.delete('1.0', tk.END)
    original_output.insert('1.0', f"Original MAC: {original_mac}")
    original_output.config(state='disabled')

    extended_output.config(state='normal')
    extended_output.delete('1.0', tk.END)
    extended_output.insert('1.0', f"Extended MAC: {extended_mac}")
    extended_output.config(state='disabled')

def clear_input():
    entry.delete(0, tk.END)
    additional_entry.delete(0, tk.END)
    original_output.config(state='normal')
    original_output.delete('1.0', tk.END)
    original_output.config(state='disabled')
    extended_output.config(state='normal')
    extended_output.delete('1.0', tk.END)
    extended_output.config(state='disabled')


root = tk.Tk()
root.title("MAC Length Extension Attack")

# Input Field for Original Message
label = tk.Label(root, text="Enter original message:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Input Field for Additional Data
additional_label = tk.Label(root, text="Enter additional data:")
additional_label.pack()
additional_entry = tk.Entry(root)
additional_entry.pack()

# Calculate Button (for length extension attack)
attack_button = tk.Button(root, text="Perform MAC Length Extension Attack", command=calculate_mac_length_extension)
attack_button.pack()

# Original MAC Output Field
original_output_label = tk.Label(root, text="Original MAC:")
original_output_label.pack()
original_output = tk.Text(root, height=1, width=50, state='disabled')
original_output.pack()

# Extended MAC Output Field
extended_output_label = tk.Label(root, text="Extended MAC:")
extended_output_label.pack()
extended_output = tk.Text(root, height=1, width=50, state='disabled')
extended_output.pack()

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack()

root.mainloop()