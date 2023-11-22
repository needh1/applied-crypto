import hashpumpy
import hashlib
import tkinter as tk
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def calculate_mac_length_extension():
    entry_text = entry.get()
    message = entry_text.encode('utf-8')

    password = os.urandom(16)

    addition_text = additional_entry.get()
    addition = addition_text.encode('utf-8')

    # Compute the original hash for H(Password || Message)
    m = hashlib.sha1()
    m.update(password + message)
    og_hash = m.hexdigest()

    original_output.config(state='normal')
    original_output.delete('1.0', tk.END)
    original_output.insert('1.0', f"Original MAC: {og_hash}")
    original_output.config(state='disabled')

    # Calculate new hash and message
    new_hash, new_message = hashpumpy.hashpump(og_hash, message, addition, len(password))

    '''print("New hash: ", new_hash)
    print("New message: ", new_message)'''

    m = hashlib.sha1()
    m.update(password + new_message)
    extended_mac = m.hexdigest()

    new_hash_output.config(state='normal')
    new_hash_output.delete('1.0', tk.END)
    new_hash_output.insert('1.0', f"New Hash: {new_hash}")
    new_hash_output.config(state='disabled')

    extended_output.config(state='normal')
    extended_output.delete('1.0', tk.END)
    extended_output.insert('1.0', f"Extended MAC: {extended_mac}")
    extended_output.config(state='disabled')

    if new_hash == extended_mac:
        status_label.config(text="ATTACK SUCCESSFUL! MACs Match (Insecure)")
    else:
        status_label.config(text="Attack Failed! MACs Don't Match (Secure)")


buffer_size = 0
buffer = []

def visualize_circular_buffer():
    # Your code to initialize data and circular buffer here...
    global buffer_size, buffer

    original_message = entry.get().encode('utf-8')
    additional_data = additional_entry.get().encode('utf-8')
    password = os.urandom(16)

    buffer_size = len(original_message) + len(additional_data)
    buffer = list(original_message) + [' '] * len(additional_data)

    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, buffer_size - 0.5)
    ax.set_ylim(0, 2)
    #ax.set_aspect('equal')

    bar = ax.bar(range(buffer_size), [0] * buffer_size, align='center')  # Initialize empty bars

    def update(frame):
        global buffer

        '''if frame < len(additional_data):
            buffer = buffer[1:] + [additional_data[frame]]'''
        # Your code to update circular buffer here...

        for i, b in enumerate(buffer):
            if b != ' ':
                bar[i].set_height(1)  # Set the height of bars to 1 for added data
                bar[i].set_color('blue')
            else:
                bar[i].set_height(0)  # Set the height of bars to 0 for original message
                bar[i].set_color('red')
        return bar

    ani = FuncAnimation(fig, update, frames=buffer_size, blit=True, repeat=False)
    plt.title('Circular Buffer Visualization - Length Extension Attack')
    plt.xlabel('Buffer Index')
    plt.yticks([])
    plt.show()

def clear_input():
    print("clear")
    entry.delete(0, tk.END)
    additional_entry.delete(0, tk.END)
    original_output.config(state='normal')
    original_output.delete('1.0', tk.END)
    original_output.config(state='disabled')
    extended_output.config(state='normal')
    extended_output.delete('1.0', tk.END)
    extended_output.config(state='disabled')
    new_hash_output.config(state='normal')
    new_hash_output.delete('1.0', tk.END)
    new_hash_output.config(state='disabled')


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

# New Hash Output Field with Additional Data
new_hash_output_label = tk.Label(root, text="New Hash:")
new_hash_output_label.pack()
new_hash_output = tk.Text(root, height =1, width=50, state='disabled')
new_hash_output.pack()

# Extended MAC Output Field
extended_output_label = tk.Label(root, text="Extended MAC:")
extended_output_label.pack()
extended_output = tk.Text(root, height=1, width=50, state='disabled')
extended_output.pack()

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack()

# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack()

# Create a button to trigger circular buffer visualization
buffer_visualization_button = tk.Button(root, text="Visualize Circular Buffer", command=visualize_circular_buffer)
buffer_visualization_button.pack()

root.mainloop()