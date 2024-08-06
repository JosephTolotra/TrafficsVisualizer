import tkinter as tk
from tkinter import simpledialog
import test

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main")
        
        self.result_label = tk.Label(self.root, text="Résultat: ")
        self.result_label.pack(pady=10)
        
        self.open_calc_button = tk.Button(self.root, text="Ouvrir Calculatrice", command=self.open_calculator)
        self.open_calc_button.pack(pady=10)

    def open_calculator(self):
        self.calc_window = tk.Toplevel(self.root)
        self.calculator = calcul.Calculator(self.calc_window, self.update_result)
    
    def update_result(self, result):
        self.result_label.config(text=f"Résultat: {result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
