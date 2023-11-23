import tkinter as tk
from RSA import rsa_generate
from Weiner import weiner_attack

def perform_attack():
    # Get the key size from the user
    keysize = int(entry_keysize.get())

    # Generate 'e', 'n', and 'd' using rsa_generate function
    e, n, generated_d = rsa_generate(keysize)

    # Update GUI with generated 'e' and 'n' for user reference
    label_generated_values.config(text=f"Generated 'e': {e}, 'n': {n}")

    # Execute the Weiner attack with generated 'e' and 'n' to obtain 'd'
    d = weiner_attack(e, n)

    # Check if the obtained 'd' matches the generated 'd' and update GUI accordingly
    if d is not None and d == generated_d:
        result_label.config(text=f"Attack successful! Private key 'd': {d}")
    else:
        result_label.config(text="Attack unsuccessful or incorrect 'd'")

# Create the main window
root = tk.Tk()
root.title("Wiener Attack GUI")

# Labels and entry for key size
label_keysize = tk.Label(root, text="Enter key size:")
label_keysize.pack()

entry_keysize = tk.Entry(root)
entry_keysize.pack()

# Button to execute the attack
attack_button = tk.Button(root, text="Execute Attack", command=perform_attack)
attack_button.pack()

# Display area for generated 'e' and 'n'
label_generated_values = tk.Label(root, text="")
label_generated_values.pack()

# Display area for the attack result
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
