# length_extension_demo.py
import hashlib
import tkinter as tk

def simulate_length_extension_attack(original_hash, extra_data):
    # This is a simulation and does not perform a real length extension attack
    # It simply hashes the extra data and appends it to the original hash
    new_hash = hashlib.sha256(extra_data.encode()).hexdigest()
    return original_hash + new_hash

def create_gui():
    root = tk.Tk()
    root.title("Length Extension Attack Simulation")

    def on_submit():
        original_hash = hash_entry.get()
        extra_data = data_entry.get()
        result = simulate_length_extension_attack(original_hash, extra_data)
        result_label.config(text="Simulated Extended Hash: " + result)

    tk.Label(root, text="Enter Original Hash:").pack()
    hash_entry = tk.Entry(root)
    hash_entry.pack()

    tk.Label(root, text="Enter Extra Data:").pack()
    data_entry = tk.Entry(root)
    data_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
