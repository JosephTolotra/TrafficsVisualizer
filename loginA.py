import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk

# Fonction pour vérifier les informations d'identification
def verify_login():
    username = username_entry.get()
    password = password_entry.get()

    # Exemple d'informations d'identification (à remplacer par une véritable vérification)
    correct_username = "user"
    correct_password = "password"

    if username == correct_username and password == correct_password:
        messagebox.showinfo("Bienvenue! \n Cliquez sur Ok et veuillez attendre quelque seconde!!")
        root.destroy()  # Ferme la fenêtre de login
        subprocess.run(["python", "main.py"])  # Remplace "python3" par "python" si nécessaire
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Traffic visualizer")

# Dimensions de la fenêtre
root.geometry("800x600")
root.resizable(False, False)

# Ajouter une image de fond
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Créer un cadre pour le formulaire de login
login_frame = tk.Frame(root, bg='whitesmoke', bd=5)
login_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=430)


# Textes supplémentaires
welcome_label = tk.Label(login_frame, text="Bienvenue dans le programme de visualisation..", font=("Arial", 12), bg='whitesmoke', fg='#333')
welcome_label.pack(pady=10)
instruction_label = tk.Label(login_frame, text="Veuillez entrer votre identifiant!", font=("Arial", 10), bg='whitesmoke', fg='#333')
instruction_label.pack(pady=5)


# Titre
title_label = tk.Label(login_frame, text="Login", font=("Arial", 24, "bold"), bg='whitesmoke', fg='#333')
title_label.pack(pady=20)

# Champ du nom d'utilisateur
username_label = tk.Label(login_frame, text="Nom d'utilisateur", font=("Arial", 12), bg='whitesmoke', fg='#333')
username_label.pack(pady=5)
username_entry = tk.Entry(login_frame, font=("Arial", 12), bd=2, relief="solid")
username_entry.pack(pady=5, padx=20, fill='x')

# Champ du mot de passe
password_label = tk.Label(login_frame, text="Mot de passe", font=("Arial", 12), bg='whitesmoke', fg='#333')
password_label.pack(pady=5)
password_entry = tk.Entry(login_frame, font=("Arial", 12), show='*', bd=2, relief="solid")
password_entry.pack(pady=5, padx=20, fill='x')

# Fonction pour les effets de survol du bouton
def on_enter(event):
    login_button.config(bg='#333', fg='whitesmoke')

def on_leave(event):
    login_button.config(bg='#4CAF50', fg='whitesmoke')

# Bouton de login
login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), command=verify_login, bg='#4CAF50', fg='whitesmoke', bd=0, padx=10, pady=5)
login_button.pack(pady=20)

author_label = tk.Label(login_frame, text="@by J & O", font=("Arial", 7), bg='whitesmoke', fg='#333')
author_label.pack(pady=5)

# Ajouter des événements de survol au bouton
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

root.mainloop()
