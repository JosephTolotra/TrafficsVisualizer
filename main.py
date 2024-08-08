import tkinter as tk
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as messagebox
from tkinter import *
# from subprocess import Popen, PIPE
# import pickle
from column_mapping import column_mapping
import os
import config
from saluer import (predict)
from create_vizsualization import (open_create_window)
from process import (load_data,lower_seaborn_plot,pie_create_matplot,update_diagrams,make_current_plot)
from diag_fonct import (line_plot,
                        traffic_by_protocol,
                        traffic_histogram, 
                        distribution_protocole,
                        quantite_protocole,
                        donnees_protocole, 
                        duree_protocole, 
                        quantite_temps,
                        dureevsquantite,
                        heatmap_correlation,
                        IPS_frequente,
                        IPD_frequente,
                        prS_frequente,
                        prD_frequente,
                        flux_interface,
                        duree_flux,
                        entrant_sortie,
                        flag_tcp,
                        flux_direction,
                        duree_packet, 
                        sa_da,
                        traffic_anormaux,
                        density_traffic,
                        comparaison )

#Chemin vers les données
data_general='./data/data_netflow.csv'
data_predict='./data/liste_packets.csv'
data_last_two_min= './data/last_csv.csv'

#Variable global
current_interval="24h"
current_plot=config.current_plot
current_pie_color='white'
last_modified_time=0
selection=0


df_default=pd.read_csv(data_general)
df_last_five=pd.read_csv(data_last_two_min)
dfPred=predict(df_last_five)


current_df=load_data(current_interval,df_default)
current_dfPred=load_data(current_interval,dfPred)

print("DF LAST FIVE:",df_last_five)
print("DF PRED :", dfPred)
print("DF CURRENT PRED:", current_dfPred)

def main():
    
    # Fonction pour obtenir la résolution de l'écran et configurer la fenêtre
    def setup_window(root):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Traffic visualizer")
    setup_window(root)

    # Calculer les dimensions pour les deux parties
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    left_width = int(screen_width * 0.22)
    right_width = screen_width - left_width

    #******************************************************************************************************************************

    # Fonctions de menu
    def show_about():
        messagebox.showinfo("À propos", "Ceci est une application de visualisation de trafic.")

    def exit_app():
        root.quit()

    # Barre de navigation
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Menu Fichier
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Fichier", menu=file_menu)
    file_menu.add_command(label="Quitter", command=exit_app)

    # Menu Aide
    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Aide", menu=help_menu)
    help_menu.add_command(label="À propos", command=show_about)

    def on_create():

        global current_interval,current_df
        open_create_window(fig_upper, canvas_s3, current_df)
    # Menu "Option"
    option_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Option", menu=option_menu)
    # Ajout de l'option "Créer une visualisation" dans le menu "Option"
    option_menu.add_command(label="Créer une visualisation", command= lambda: on_create())
    #***********************************************************************************************************************************
    # Créer et configurer le cadre de gauche
    left_frame = tk.Frame(root,bg="#2c3e50", width=left_width, height=screen_height, bd=1, relief="solid")
    left_frame.place(x=0, y=0)

    # Calculer les hauteurs pour les deux parties de la section gauche
    left_upper_height = int(screen_height * 0.25)
    left_lower_height = int(screen_height * 0.68)

    # Créer et configurer le cadre supérieur de la partie gauche
    left_upper_frame = tk.Frame(left_frame, bg='whitesmoke', width=left_width, height=left_upper_height, bd=1, relief="solid")
    left_upper_frame.place(x=0, y=0)

    # Créer et configurer le cadre inférieur de la partie gauche
    left_lower_frame = tk.Frame(left_frame, bg='whitesmoke', width=left_width, height=left_lower_height, bd=1, relief="solid")
    left_lower_frame.place(x=0, y=left_upper_height+10,width=left_width, height=left_lower_height)


    def add_placeholder(entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(fg='grey')

    def remove_placeholder(event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg='black')

    def add_placeholder_back(event, placeholder):
        if event.widget.get() == "":
            event.widget.insert(0, placeholder)
            event.widget.config(fg='grey')

    # Barre de recherche
    search_entry = tk.Entry(left_lower_frame, width=left_width)
    search_entry.grid(row=0, column=0, padx=5, pady=5)
    placeholder_text = "Rechercher à partir de cette liste..."
    # Ajouter le placeholder initialement
    add_placeholder(search_entry, placeholder_text)

    # Lier les événements focus in et focus out pour gérer le placeholder
    search_entry.bind("<FocusIn>", lambda event: remove_placeholder(event, placeholder_text))
    search_entry.bind("<FocusOut>", lambda event: add_placeholder_back(event, placeholder_text))

    # Liste des diagrammes
    diagrams_listbox = tk.Listbox(left_lower_frame, selectmode=tk.SINGLE, bg='#FFFFFF', fg='#000000', width=left_width, height=left_lower_height)

    # Créer des barres de défilement horizontale et verticale
    scroll_y = tk.Scrollbar(left_lower_frame, orient="vertical", command=diagrams_listbox.yview)
    scroll_x = tk.Scrollbar(left_lower_frame, orient="horizontal", command=diagrams_listbox.xview)
    # Configurer la Listbox pour utiliser les barres de défilement
    diagrams_listbox.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    diagrams = ["Répartition Trafic par temps (Time vs Traffic)", 
                "Répartition Trafic par Protocole", 
                "Histogramme du Trafic", 
                "Distribution des protocoles utilisés",
                "Quantité total de données échangées par protocole",
                "Distribution de la quantité de données par protocole", 
                "Distribution de la durée des flux par protocole", 
                "Quantité de données au Fil du temps",
                "Durée du flux vs Quantité de données par protocole",
                "Heatmap de Corrélation",
                "Visualisation des Addresses IP Sources",
                "Visualisation des Addresses IP Destinations",
                "Visualisation des ports sources les plus fréquents",
                "Visualisation des ports destinations les plus fréquents",
                "Flux par interface",
                "Distribution des durées de flux",
                "Distribution des paquets entrants et sortants",
                "Analyse des Flags TCP",
                "Flux par direction",
                "Flux par durée et taille des paquets",
                "Flux par adresse IP source et destination (Heatmap)",
                "Visualisation des Modèles de trafic anormaux (Outliers)",
                "Densité de trafic",
                "Facet Grid (Trafic par protocole)"]
                
    for diagram in diagrams:
        diagrams_listbox.insert(tk.END, diagram)
    diagrams_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    scroll_y.grid(row=1, column=2, sticky='ns')
    scroll_x.grid(row=2, column=0, columnspan=2, sticky='ew')

    # Configurer les poids des colonnes et lignes pour un redimensionnement correct
    left_lower_frame.grid_columnconfigure(0, weight=1)
    left_lower_frame.grid_columnconfigure(1, weight=1)
    left_lower_frame.grid_rowconfigure(1, weight=1)


    # Configurer les poids des colonnes et lignes pour un redimensionnement correct
    left_lower_frame.grid_columnconfigure(1, weight=1)
    left_lower_frame.grid_rowconfigure(1, weight=1)

    # Fonction pour afficher les coordonnées de la souris
    def on_plot_hover(event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            coord_label.config(text=f"Coordonnées: x={int(x)}, y={y:.2f}")

    # Créer et configurer le cadre de droite
    right_frame = tk.Frame(root, bg='#1E90FF', width=right_width, height=screen_height, bd=1, relief="solid")
    right_frame.place(x=left_width, y=0)

    # Calculer les hauteurs pour les deux parties de la section droite
    right_upper_height = int(screen_height * 0.6)
    right_lower_height = screen_height - right_upper_height

    # Créer et configurer le cadre supérieur de la partie droite
    right_upper_frame = tk.Frame(right_frame, bg='whitesmoke', width=right_width, height=right_upper_height, bd=1, relief="solid")
    right_upper_frame.place(x=0, y=0)

    # Créer et configurer le cadre inférieur de la partie droite
    right_lower_frame = tk.Frame(right_frame, bg='whitesmoke', width=right_width, height=right_lower_height, bd=1, relief="solid")
    right_lower_frame.place(x=0, y=right_upper_height)

    # Calculer les largeurs pour les deux sous-parties de la section inférieure droite
    s4_width = int(right_width * 0.5)
    s5_width = right_width - s4_width

    # Créer et configurer le sous-cadre de gauche dans la partie inférieure droite
    s4_frame = tk.Frame(right_lower_frame, bg='whitesmoke', width=s4_width, height=right_lower_height, bd=1, relief="solid")
    s4_frame.place(x=0, y=0)

    # Créer et configurer le sous-cadre de droite dans la partie inférieure droite
    s5_frame = tk.Frame(right_lower_frame, bg='whitesmoke', width=s5_width, height=right_lower_height, bd=1, relief="solid")
    s5_frame.place(x=s4_width, y=0)

    # Ajouter une combobox pour sélectionner l'intervalle de temps
    interval_options = ["2min","10min", "1h", "6h", "24h","+ de 1 jour"]
    selected_interval = tk.StringVar()
    selected_interval.set([current_interval])  # Définir l'option par défaut
    interval_combobox = ttk.Combobox(root, textvariable=selected_interval, values=interval_options, state='readonly')
    interval_combobox.place(x=screen_width - 150, y=10)

    # Ajouter une étiquette pour afficher les coordonnées
    coord_label = tk.Label(root, text="Coordonnées: x=, y=")
    coord_label.place(x=left_width + 10, y=10)

    # Dictionnaire associant chaque diagramme à sa fonction
    diagram_functions = {
        "Répartition Trafic par temps (Time vs Traffic)": line_plot,
        "Répartition Trafic par Protocole": traffic_by_protocol,
        "Histogramme du Trafic": traffic_histogram, 
        "Distribution des protocoles utilisés": distribution_protocole,
        "Quantité total de données échangées par protocole": quantite_protocole,
        "Distribution de la quantité de données par protocole": donnees_protocole, 
        "Distribution de la durée des flux par protocole": duree_protocole, 
        "Quantité de données au Fil du temps": quantite_temps,
        "Durée du flux vs Quantité de données par protocole": dureevsquantite,
        "Heatmap de Corrélation": heatmap_correlation,
        "Visualisation des Addresses IP Sources": IPS_frequente,
        "Visualisation des Addresses IP Destinations": IPD_frequente,
        "Visualisation des ports sources les plus fréquents": prS_frequente,
        "Visualisation des ports destinations les plus fréquents": prD_frequente,
        "Flux par interface": flux_interface,
        "Distribution des durées de flux":duree_flux, 
        "Distribution des paquets entrants et sortants": entrant_sortie,   
        "Analyse des Flags TCP":flag_tcp,
        "Flux par direction": flux_direction,
        "Flux par durée et taille des paquets": duree_packet,
        "Flux par adresse IP source et destination (Heatmap)": sa_da,
        "Visualisation des Modèles de trafic anormaux (Outliers)": traffic_anormaux,
        "Densité de trafic":density_traffic,
        "Facet Grid (Trafic par protocole)":comparaison
    }

    #****************************************************************************************************
    #Confugurer la fenêtre pour acceullir le MAJ
    fig_upper = plt.Figure(figsize=((right_width/100), (right_upper_height/100)), dpi=100)
    fig_upper.subplots_adjust(right=0.95)
    fig_upper.subplots_adjust(left=0.18)
    fig_upper.subplots_adjust(top=0.9)
    fig_upper.subplots_adjust(bottom=0.18)  # Ajuster la marge gauche
    canvas_s3 = FigureCanvasTkAgg(fig_upper, master=right_upper_frame)
    canvas_s3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)   
    # Connecter l'événement de survol de la souris
    canvas_s3.mpl_connect("motion_notify_event", on_plot_hover)


    fig_s4 = plt.Figure(figsize=((s4_width/100), (right_lower_height/117)), dpi=100)
    canvas_s4 = FigureCanvasTkAgg(fig_s4, master=s4_frame)
    canvas_s4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    fig_s5= plt.Figure(figsize=((s4_width/100), (right_lower_height/117)), dpi=100)
    canvas_s5 = FigureCanvasTkAgg(fig_s5, master=s5_frame)
    canvas_s5.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    #*********************************************************************************************************
    # Afficher les graphiques dans les sections spécifiées
    root.update_idletasks()# Mettre à jour la géométrie des cadres avant de créer les plots

    make_current_plot(fig_upper,canvas_s3,current_df,current_plot)
    lower_seaborn_plot(fig_s4,canvas_s4,fig_upper,canvas_s3, current_df, sns.countplot,
            title="Distribution des protocoles utilisés", xlabel="Protocole", ylabel="Count",
            x='pr') 
    lower_seaborn_plot(fig_s5, canvas_s5 ,fig_upper,canvas_s3, current_df, sns.scatterplot,
                title="Durée du flux vs Quantité de données par protocole",
                xlabel="Durée du flux (s)", ylabel="Quantité de données",
                x='td', y='ibyt', hue='pr', palette='viridis')      
    pie_create_matplot(left_upper_frame, current_dfPred,current_pie_color)

    # Gestionnaire d'événements pour la liste des diagrammes
    def on_diagram_select(event):
        global current_df
        #global fig_upper
        #global canvas_s3
        global current_plot
        global selection
        # Obtenez la sélection courante
        selection = diagrams_listbox.curselection()
        if not selection:
            # Si aucune sélection n'est faite
            print("Erreur", "Aucun diagramme sélectionné")
            selection=0
            return
        else :
            selection = int(selection[0])
            # Récupérez l'élément sélectionné
            selected_diagram = diagrams_listbox.get(selection)    
            # Traitez l'élément sélectionné ici
            print(f"Diagramme sélectionné : {selection}")

        config.current_plot=diagram_functions[selected_diagram]
        current_plot=config.current_plot
        make_current_plot(fig_upper,canvas_s3,current_df,current_plot)

    diagrams_listbox.bind('<<ListboxSelect>>', on_diagram_select)

    # Fonction de recherche
    def search_diagrams(event):
        search_term = search_entry.get().lower()
        diagrams_listbox.delete(0, tk.END)
        for diagram in diagrams:
            if search_term in diagram.lower():
                diagrams_listbox.insert(tk.END, diagram)

    search_entry.bind('<KeyRelease>', search_diagrams)

    def select_item(index):
            # Désélectionner tous les éléments
            diagrams_listbox.selection_clear(0, tk.END)
            # Sélectionner l'élément à l'index donné
            diagrams_listbox.selection_set(index)
            # Assurer la visibilité de l'élément sélectionné
            print("mlay be")
            print(index)
            diagrams_listbox.see(index)
        

    def on_interval_change(event):
        global current_interval, selection
        global df_default,dfPred,current_df
        interval = selected_interval.get()
        current_interval=interval
        print("current_interval ao anaty on_interval_change :", current_interval)
        current_plot=config.current_plot
        current_df=load_data(current_interval, df_default)
        current_dfPred=load_data(current_interval,dfPred)
        
        if selection!=0:   
            select_item(selection)
        pie_create_matplot(left_upper_frame, current_dfPred,current_pie_color)
        update_diagrams(current_df,current_plot,fig_upper,canvas_s3,fig_s4,fig_s5,canvas_s4,canvas_s5)
            
        
    interval_combobox.bind("<<ComboboxSelected>>", on_interval_change)

    print("Current interval après boxage : ", current_interval)

    def periodic_update():
        print("Tentative de mis à jour")
        current_plot=config.current_plot
        #global fig_upper, fig_s4, fig_s5
        #global canvas_s3, canvas_s4, canvas_s5
        global data_general,data_last_two_min, last_modified_time
        global current_dfPred,df_last_five,current_df,df_default,dfPred
        global current_pie_color,current_interval
        df_last_five=pd.read_csv(data_last_two_min)
        if df_last_five.empty:
            print ("Fichier vide!!")
        elif df_last_five.empty and not df_last_five.columns.empty:
            print("Aucune nouvelle donnée")
        else :
            dfPred=predict(df_last_five)
            current_dfPred=load_data(current_interval,dfPred)
            config.new_anomalie_seen=False
            pie_create_matplot(left_upper_frame, current_dfPred,current_pie_color)

        try:
            modified_time = os.path.getmtime(data_general)
            if modified_time != last_modified_time:
                df_default=pd.read_csv(data_general)
                current_df=load_data(current_interval,df_default)
                print("Nouveaux flux à visulaiser détectés!!")
                last_modified_time = modified_time
                update_diagrams(current_df,current_plot,fig_upper,canvas_s3,fig_s4,fig_s5,canvas_s4,canvas_s5)
        except Exception as e:
            print(f"Error checking file updates: {e}")
        root.after(20000, periodic_update)


    root.after(30000, periodic_update)



    # Gestionnaire pour fermer correctement la fenêtre Tkinter (Tsy mampiram anle terminal)
    def on_closing():
        plt.close('all')
        # root.after_cancel() 
        root.quit()  
        root.destroy() 
        

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Lancer la boucle principale de l'application
    root.mainloop()

if __name__ == "__main__":
    main()