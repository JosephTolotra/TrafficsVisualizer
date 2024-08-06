import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        num3 = float(entry3.get())
        operator = operator_combobox.get()

        if operator == '+':
            result = num1 + num2 + num3
        elif operator == '-':
            result = num1 - num2 - num3
        elif operator == '*':
            result = num1 * num2 * num3
        elif operator == '/':
            result = num1 / num2 / num3
        else:
            raise ValueError("Opérateur non valide")

        with open('result.pkl', 'wb') as f:
            pickle.dump(result, f)

        root.destroy()
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

root = tk.Tk()
root.title("Calculatrice")

tk.Label(root, text="Nombre 1:").grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

tk.Label(root, text="Nombre 2:").grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

tk.Label(root, text="Nombre 3:").grid(row=2, column=0)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1)

tk.Label(root, text="Opérateur:").grid(row=3, column=0)
operator_combobox = ttk.Combobox(root, values=['+', '-', '*', '/'])
operator_combobox.grid(row=3, column=1)
operator_combobox.current(0)

calculate_button = tk.Button(root, text="Calculer", command=calculate)
calculate_button.grid(row=4, columnspan=2, pady=10)

root.mainloop()
