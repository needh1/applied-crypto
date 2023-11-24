import tkinter as tk
import RSA 
#import Weiner
#import rsa

def perform_attack():
    # Get the key size from the user
    try:
        keysize = int(entry_keysize.get())
        if keysize <=0:
            raise ValueError("key must be positive")
        
        # Generate 'e', 'n', and 'd' using rsa_generate function
        e, n, generated_d = RSA.rsa_generate(keysize)

        # Generate RSA keys using rsa library
        #(public_key, private_key) = rsa.newkeys(keysize)

        '''e = public_key.e
        n = public_key.n
        d = private_key.d'''

        # Update GUI with generated 'e' and 'n' for user reference
        generated_values_text.delete(1.0, tk.END)  # Clear previous values
        generated_values_text.insert(tk.END, f"Generated 'e': {e}\n'n': {n}\n'd': {generated_d}")


        # Execute the Weiner attack with generated 'e' and 'n' to obtain 'd'
        #attack_d = Weiner.weiner_attack(e, n)

        # Check if the obtained 'd' matches the generated 'd' and update GUI accordingly
        '''if d is not None and d == generated_d:
            result_label.config(text=f"Attack successful! Private key 'd': {d}")
        else:
            result_label.config(text="Attack unsuccessful or incorrect 'd'")'''
        
        '''if attack_d is not None and attack_d == generated_d:
            result_label.config(text=f"Attack successful! Private key 'd': {attack_d}")
        else:
            result_label.config(text="Attack unsuccessful or incorrect 'd'")'''
    except ValueError as ve:
        result_label.config(text = f"Error: {ve}")
    except Exception as e:
        result_label.config(text = f"Unexpected Error: {e}")
        
# Create the main window
root = tk.Tk()
root.title("RSA Implementation GUI")

label_keysize = tk.Label(root, text="Enter key size:")
label_keysize.pack()

entry_keysize = tk.Entry(root)
entry_keysize.pack()

attack_button = tk.Button(root, text="RSA Values", command=perform_attack)
attack_button.pack()

generated_values_text = tk.Text(root, height=10, width=40)
generated_values_text.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()