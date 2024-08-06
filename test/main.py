import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from subprocess import Popen, PIPE
import pickle

def open_calculator():
    process = Popen(['python', 'test.py'], stdout=PIPE)
    process.communicate()

    # Load the result from the file
    try:
        with open('result.pkl', 'rb') as f:
            result = pickle.load(f)
            result_label.config(text=f"Résultat: {result}")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Impossible de trouver le fichier de résultat")

root = tk.Tk()
root.title("Main")

result_label = tk.Label(root, text="Résultat: ")
result_label.pack(pady=10)

open_calc_button = tk.Button(root, text="Ouvrir Calculatrice", command=open_calculator)
open_calc_button.pack(pady=10)

root.mainloop()
