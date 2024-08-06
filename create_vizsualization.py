import tkinter as tk
from tkinter import ttk
import seaborn as sns
from column_mapping import column_mapping
from process import (make_current_plot)

import config

# Fonction pour ouvrir la fenêtre de création de visualisation
def open_create_window(fig_upper, canvas_s3, df):
    create_window = tk.Toplevel()
    create_window.title("Créer une visualisation")
    create_window.geometry("500x300")
    create_window.configure(bg="#2c3e50")

    # Style pour les labels et les boutons
    style = ttk.Style()
    style.configure("TLabel", foreground="white", background="#2c3e50", font=("Helvetica", 12))
    style.configure("TButton", foreground="#2c3e50", background="white", font=("Helvetica", 12, "bold"))

    # Ajout d'un cadre pour un meilleur agencement
    frame = tk.Frame(create_window, padx=10, pady=10, bg="#34495e")
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # Création des étiquettes et des entrées pour saisir les informations
    ttk.Label(frame, text="Titre :", anchor="w").grid(row=0, column=0, sticky="w", pady=5, padx=5)
    ttk.Label(frame, text="Diagramme :", anchor="w").grid(row=1, column=0, sticky="w", pady=5, padx=5)
    ttk.Label(frame, text="Axe de x :", anchor="w").grid(row=2, column=0, sticky="w", pady=5, padx=5)
    ttk.Label(frame, text="Axe de y :", anchor="w").grid(row=3, column=0, sticky="w", pady=5, padx=5)

    entry_name = tk.Entry(frame, font=("Helvetica", 12))
    entry_name.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

    # Ajouter une combobox pour sélectionner l'intervalle de temps pour l'axe x
    columnx_options = [value for key, value in column_mapping.items()]
    selected_columnx = tk.StringVar()
    selected_columnx.set('') 
    columnx_combobox = ttk.Combobox(frame, textvariable=selected_columnx, values=columnx_options, state='readonly', font=("Helvetica", 12))
    columnx_combobox.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

    # Ajouter une combobox pour sélectionner l'intervalle de temps pour l'axe y
    columny_options = [value for key, value in column_mapping.items()]
    selected_columny = tk.StringVar()
    selected_columny.set('') 
    columny_combobox = ttk.Combobox(frame, textvariable=selected_columny, values=columny_options, state='readonly', font=("Helvetica", 12))
    columny_combobox.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

    # Ajouter une combobox pour sélectionner le type de diagramme
    diagram_options = ["Line", "Count", "Histogramme", "Bar", "Box", "Courbe"]
    selected_diagram = tk.StringVar()
    selected_diagram.set('Line')  # Définir l'option par défaut
    diagram_combobox = ttk.Combobox(frame, textvariable=selected_diagram, values=diagram_options, state='readonly', font=("Helvetica", 12))
    diagram_combobox.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

    def on_create_visualization(fig_upper,canvas_s3,df):
        diagram_char=diagram_combobox.get()
        title=entry_name.get() 
        xlabel=columnx_combobox.get()
        ylabel=columny_combobox.get()
        create_window.destroy()
        diagram_dic={
            "Line":sns.lineplot,
            "Count":sns.countplot,
            "Histogramme":sns.histplot,
            "Bar":sns.barplot,
            "Box":sns.boxplot,
            "Courbe":sns.kdeplot
        }
        inverted_column_mapping = {value: key for key, value in column_mapping.items()}
        kwargs={
        'x': inverted_column_mapping.get(xlabel),
        'y': inverted_column_mapping.get(ylabel)
        }
        accessories=[]
        diagram_fonc = diagram_dic[diagram_char]
        
        def simple_diag(df):
            return df,diagram_fonc,title,xlabel,ylabel,accessories,kwargs
        
        config.current_plot=simple_diag   # Fonction appelée lors du clic sur le bouton "OK"
        print("Tonga ato amn le zalah ty ve??")
        make_current_plot(fig_upper,canvas_s3,df,simple_diag)
        

    # Bouton "OK" pour valider les informations saisies
    btn = ttk.Button(frame, text="Créer une simple visualisation ", command=lambda:on_create_visualization(fig_upper,canvas_s3,df))
    btn.grid(row=4, columnspan=2, pady=10)

    # Ajouter un peu d'espace autour des widgets
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(4, weight=1)