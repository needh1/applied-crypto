import tkinter as tk
import struct
import binascii
import matplotlib
matplotlib.use('TkAgg')  # This must be done before importing pyplot
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from sha_256 import Sha256Hash  # Assuming your custom SHA-256 implementation is in a file named "sha256.py"

# Compute hash of the entire extended message
def compute_direct_hash(original_message, padding, append):
    hasher = Sha256Hash()
    hasher.update(original_message)
    hasher.update(padding)
    hasher.update(append)
    return binascii.hexlify(hasher.digest()).decode('utf-8')

# Padding function for SHA-256n,jli
def sha256_padding(length):
    padding = b'\x80'
    while (length + len(padding)) % 64 != 56:
        padding += b'\x00'
    return padding + struct.pack('>Q', length * 8)

# Function to perform the length extension attack
def calculate_sha256_attack():
    try:
        originalMessage = entry.get().encode('utf-8')
        originalLength = len(originalMessage)  # Original message length
        padding = sha256_padding(originalLength)
        append = append_entry.get().encode('utf-8')  # Get the text to append

    # hashing original message 
        original_hasher = Sha256Hash()
        original_hasher.update(originalMessage)
        original_hashed_text = binascii.hexlify(original_hasher.digest()).decode('utf-8')
        og_output.delete(0, tk.END)
        og_output.insert(tk.END, original_hashed_text)
    
        initialState = original_hashed_text

    # perform the length extension attack
        hasher = Sha256Hash(initialState, originalLength + len(padding))
        hasher.update(append)
        hashed_text = binascii.hexlify(hasher.digest()).decode('utf-8')

    # Direct hash calculation for verification
        direct_hash = compute_direct_hash(originalMessage, padding, append)
        direct_hash_output.delete(0, tk.END)
        direct_hash_output.insert(tk.END, direct_hash)

    
    # Compare hashes for result
        if hashed_text == direct_hash:
            result = "Attack Successful: Hashes Match (System is Insecure)"
        else:
            result = "Attack Failed: Hashes Do Not Match (System is Secure)"

        output.delete(0, tk.END)
        output.insert(tk.END, hashed_text)
        status_label.config(text=result)
        
    except Exception as e:
        print("Error occurred:", e)

# clear output
def clear_input():
    entry.delete(0, tk.END)
    append_entry.delete(0, tk.END)
    output.delete(0, tk.END)
    og_output.delete(0, tk.END)

root = tk.Tk()
root.title("SHA-256 Hash Calculator")

# Input Field
label = tk.Label(root, text="Enter original message:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Input Field 2
append_label = tk.Label(root, text="Enter additional data:")
append_label.pack()
append_entry = tk.Entry(root)
append_entry.pack()

# Calculate Button (for length extension attack)
attack_button = tk.Button(root, text="Perform Length Extension Attack", command=calculate_sha256_attack)
attack_button.pack()

# Output Field for Original Hash
original_hash_label = tk.Label(root, text="Original Message SHA-256 Hash:")
original_hash_label.pack()
og_output = tk.Entry(root)
og_output.pack()

# Direct Hash Output Field
direct_hash_label = tk.Label(root, text="Direct Hash:")
direct_hash_label.pack()
direct_hash_output = tk.Entry(root)
direct_hash_output.pack()

# Output Field for Extended Hash
output_label = tk.Label(root, text="SHA-256 Hash:")
output_label.pack()
output = tk.Entry(root)
output.pack()

# status label
status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack()

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack()

# visualisation circular buffer 
def visualize_circular_buffer():
    global bufferSize, buffer 
    bufferSize = 64
    buffer = [0]* bufferSize

    originalMessage = entry.get().encode('utf-8')
    additionalData = append_entry.get().encode('utf-8')

    for i in range(len(originalMessage)):
        buffer[i % bufferSize] = originalMessage[i]

    fig, ax = plt.subplots()
    ax.set_xlim(-1, bufferSize)
    ax.set_ylim(0, 1.5)

    bar = ax.bar(range(bufferSize), [0] * bufferSize, align='center', width = 0.8)

    def update(frame):
        if frame < len(additionalData):
            buffer[frame % bufferSize] = additionalData[frame]

        for i, b in enumerate(buffer):
            bar[i].set_height(1 if b != 0 else 0)
            bar[i].set_color('green' if b != 0 else 'gray')
        return bar
    
    ani = FuncAnimation(fig, update, frames=range(max(len(originalMessage), len(additionalData))), blit=True, repeat=False)
    plt.title('Circular Buffer Visualization - SHA-256 Length Extension Attack')
    plt.xlabel('Buffer Index')
    plt.ylabel('Value')  # Optionally add a y-label
    plt.yticks([0, 1], ['0', '1'])  # Set y-ticks to correspond to the possible values in the buffer
    plt.tight_layout()  # Automatically adjust subplot params to give specified padding
    plt.show()

 # Circular buffer visualization button
buffer_visualization_button = tk.Button(root, text="Visualize Circular Buffer", command=visualize_circular_buffer)
buffer_visualization_button.pack()

# hash comparision bar chart
def hash_comparison_chart():
    original_hash = og_output.get()
    extended_hash = output.get()
    direct_hash = direct_hash_output.get()
    
    hash_lengths = [len(original_hash), len(extended_hash), len(direct_hash)]
    labels = ['Original Hash', 'Extended Hash', 'Direct Hash']
    
    fig, ax = plt.subplots()
    ax.bar(labels, hash_lengths, color=['blue', 'orange', 'green'])
    
    plt.title('Hash Length Comparison')
    plt.ylabel('Length of Hash Value')
    plt.tight_layout()
    plt.show()

# Hash Comparison Visualization Button
hash_comparison_button = tk.Button(root, text="Hash Comparison Chart", command=hash_comparison_chart)
hash_comparison_button.pack()

# message length line chart 
def message_length_graph():
    message = entry.get().encode('utf-8')
    additional_data = append_entry.get().encode('utf-8')
    message_lengths = list(range(len(message), len(message) + len(additional_data) + 1))
    hash_values = []

    for i in range(len(additional_data) + 1):
        hasher = Sha256Hash()
        hasher.update(message + additional_data[:i])
        hash_values.append(int(binascii.hexlify(hasher.digest()), 16))

    fig, ax = plt.subplots()
    ax.plot(message_lengths, hash_values, 'o-')
    
    plt.title('Hash Value vs. Message Length')
    plt.xlabel('Message Length')
    plt.ylabel('Hash Value')
    plt.tight_layout()
    plt.show()

# Message Length Visualization Button
message_length_button = tk.Button(root, text="Message Length Graph", command=message_length_graph)
message_length_button.pack()


root.mainloop()