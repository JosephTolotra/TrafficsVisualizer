import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import *

from column_mapping import column_mapping

def display_data_window(df,title):

    # Fonction pour obtenir la description d'une colonne à partir de son nom
    def get_column_description(column_name):
        return column_mapping.get(column_name, column_name)  # Retourne le nom de la colonne 
    # Fonction de tri des colonnes
    def sort_column(tree, data, col, reverse):
        data.sort_values(by=col, ascending=not reverse, inplace=True)
        for item in tree.get_children():
            tree.delete(item)
        for index, row in data.iterrows():
            tree.insert("", "end", values=list(row))
        tree.heading(col, command=lambda: sort_column(tree, data, col, not reverse))

    # Création une nouvelle fenêtre
    dwindow = tk.Toplevel()
    dwindow.title(title)

    # Création d' un tableau (Treeview) pour afficher les données
    tree = ttk.Treeview(dwindow)
    tree['columns'] = list(df.columns)
    tree['show'] = 'headings'  # Supprimer la première colonne vide

    # Ajouter les en-têtes de colonnes avec les descriptions correspondantes et les commandes de tri
    for col in df.columns:
        col_description = get_column_description(col)
        tree.heading(col, text=col_description, command=lambda _col=col: sort_column(tree, df, _col, False))
        tree.column(col, width=100)

    # Ajouter une barre de défilement verticale
    scrollbar = ttk.Scrollbar(dwindow, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscroll=scrollbar.set)

    # Ajouter les données
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    tree.pack(fill=tk.BOTH, expand=True)

    # scroll horizontale
    x_scrollbar = ttk.Scrollbar(dwindow, orient='horizontal', command=tree.xview)
    tree.configure(xscrollcommand=x_scrollbar.set)
    x_scrollbar.pack(fill='x')
