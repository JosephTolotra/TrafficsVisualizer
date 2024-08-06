import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Calculator:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.root.title("Calculatrice")

        tk.Label(self.root, text="Nombre 1:").grid(row=0, column=0)
        self.entry1 = tk.Entry(self.root)
        self.entry1.grid(row=0, column=1)

        tk.Label(self.root, text="Nombre 2:").grid(row=1, column=0)
        self.entry2 = tk.Entry(self.root)
        self.entry2.grid(row=1, column=1)

        tk.Label(self.root, text="Nombre 3:").grid(row=2, column=0)
        self.entry3 = tk.Entry(self.root)
        self.entry3.grid(row=2, column=1)

        tk.Label(self.root, text="Opérateur:").grid(row=3, column=0)
        self.operator_combobox = ttk.Combobox(self.root, values=['+', '-', '*', '/'])
        self.operator_combobox.grid(row=3, column=1)
        self.operator_combobox.current(0)

        self.calculate_button = tk.Button(self.root, text="Calculer", command=self.calculate)
        self.calculate_button.grid(row=4, columnspan=2, pady=10)

    def calculate(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            num3 = float(self.entry3.get())
            operator = self.operator_combobox.get()

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

            self.callback(result)
            self.root.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root, lambda result: print(result))
    root.mainloop()
