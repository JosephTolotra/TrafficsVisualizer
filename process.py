import tkinter as tk
from tkinter import ttk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import timedelta
from tkinter import *
from data_window import display_data_window

import config


#Charger les données en fonction de current_interval
def load_data(current_interval, df):
    print("Chargement des données...")
    #La date du système d'exploitation
    # now = datetime.now()
    interval=current_interval
    if df.empty:
        return df
    else:
        # Convertir la colonne 'ts' en datetime de manière sécurisée
        df.loc[:,'ts'] = pd.to_datetime(df['ts'], errors='coerce')
        #Date du dernier enregistrement
        now =df.loc[:,'ts'].max()
        if interval == "2min":
            time_threshold = now - timedelta(minutes=2)
            # Filtrer les données
            filtered_df = df[df.loc[:,'ts'] >= time_threshold]
            df=filtered_df
        elif interval == "10min":
            time_threshold = now - timedelta(minutes=10)
            filtered_df = df[df.loc[:,'ts'] >= time_threshold]
            df=filtered_df
        elif interval == "1h":
            time_threshold = now - timedelta(hours=1)
            filtered_df = df[df.loc[:,'ts'] >= time_threshold]
            df=filtered_df
        elif interval == "6h":
            time_threshold = now - timedelta(hours=6)
            filtered_df = df[df.loc[:,'ts'] >= time_threshold]
            df=filtered_df
        elif interval == "24h":
            time_threshold = now - timedelta(hours=24)
            filtered_df = df[df.loc[:,'ts'] >= time_threshold]
            df=filtered_df
        else :
            df=df
        # Renvoie toutes les données si l'intervalle n'est pas reconnu
    return df

#Fonction pour calculer le taux des trafics anomalies
def rate_prediction(dfPred):
    #Convertir les valeurs de colonne "Label" en numérique
    if dfPred.empty:
        rate=0
    else:
        dfPred.loc[:,'Label']=dfPred['Label'].apply(pd.to_numeric, errors='coerce')
        # Compter le nombre total de lignes dans la colonne 'label'
        total_count = len(dfPred.loc[:,'Label'])
        # Compter le nombre de valeurs dans la colonne 'label' qui sont égales à 1 (Anomalies)
        count_lab_eg_1 = (dfPred.loc[:,'Label'] == 1).sum()
        # Calculer le taux
        print("Nombre total de ligne dans df :", total_count)
        print("Nombre total de ligne où Label =1 :", count_lab_eg_1)
        if total_count !=0 :
            rate = int((count_lab_eg_1 / total_count)*100)
        else :
            rate = 0
    return rate    


def create_seaborn_plot(fig, canvas, df, plot_func, title, xlabel, ylabel, accessories, **kwargs):
    fig.clear()
    ax = fig.add_subplot(111)

    if 'palette' in kwargs and 'hue' not in kwargs:
        kwargs['hue'] = kwargs['x']
        kwargs['legend'] = False

    if plot_func!=None:
        plot_func(ax=ax, data=df, **kwargs)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Récupérer les étiquettes actuelles
    labels = [item.get_text() for item in ax.get_xticklabels()]
    # Définir les étiquettes avec rotation et alignement
    ax.set_xticks(ax.get_xticks())  # Pour assurer que les positions des ticks sont fixées

    # Si les valeurs de x sont ts, tr, sa, da (ce sont les plus longues), on va configurer l'emplacement du plot
    if 'x' in kwargs:
        if kwargs['x']=='ts' or kwargs['x']=='tr' or kwargs['x']=='sa' or kwargs['x']=='da':
            ax.tick_params(axis='x', labelsize=7)
            ax.tick_params(axis='y', labelsize=8)
            fig.subplots_adjust(bottom=0.32)
            ax.set_xticklabels(labels, rotation=90, ha='center')

    else :
        fig.subplots_adjust(bottom=0.15)
    # Appliquer les accessoires s'ils sont fournis
    if accessories:
        for accessory in accessories:
            accessory(ax, df)  # Passer ax et df aux accessoires

    canvas.draw()

def make_current_plot(fig,canvas,data,diag_fonc):
    # Obtenir les arguments de la fonction plot_func
    df, plot_func, title, xlabel, ylabel, accessories, kwargs = diag_fonc(data)

    # Appeler create_seaborn_plot avec les arguments obtenus
    create_seaborn_plot(fig, canvas, df, plot_func, title, xlabel, ylabel, accessories, **kwargs)

 
def lower_seaborn_plot(fig,canvas,fig_up,canvas3, df, plot_func, title, xlabel, ylabel, **kwargs): 
    fig.clear()
    fig.subplots_adjust(right=0.95)
    fig.subplots_adjust(left=0.2)
    fig.subplots_adjust(top=0.9)
    fig.subplots_adjust(bottom=0.18)  # Ajuster la marge gauche

    ax = fig.add_subplot(111)
    if 'palette' in kwargs and 'hue' not in kwargs:
        kwargs['hue'] = kwargs['x']
        kwargs['legend'] = False

    plot_func(ax=ax, data=df, **kwargs)
    ax.set_title(title,fontsize=10, fontname="Arial")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=5.5)
    accessories=[]

    def on_click (event):
        def low_diag(df):
            return df,plot_func,title,xlabel,ylabel,accessories,kwargs
        
        config.current_plot=low_diag   # Fonction appelée lors du clic sur le bouton "OK"
        make_current_plot(fig_up,canvas3,df,low_diag)

    canvas.mpl_connect('button_press_event', on_click)
    canvas.draw()

    
def pie_create_matplot(frame, df_pred, current_pie_color): #ito le pourcentage kely à gauche    
    taux=rate_prediction(df_pred)
    tauxS=str(taux) + "%"
    sizes = [(100-taux), taux]  # Les tailles doivent sommer à 100 pour représenter des pourcentages
    labels = [str(100-taux)+"%", '']  
    if not config.new_anomalie_seen:
    #Charger seulement les données prédit dans la 2 dernière minutes
        df_pred_last_2_min=load_data("2min", df_pred)
        # Compter le nombre de ligne ,dont la colonne 'Label' est égale à 1, dans les données collecté dans la 2 dernières minutes 
        count_lab_eg_1 = (df_pred_last_2_min.loc[:,'Label'] == 1).sum()
        print(count_lab_eg_1)
        if count_lab_eg_1>0:
            current_pie_color='red'
        print(current_pie_color)
    # Personnalisation des couleurs et des bordures
    colors = ['green', 'red']  # intérieur et extérieur
    outer_colors = ['black', 'white']  #bordure extérieure et intérieure
    
    for widget in frame.winfo_children():
            widget.destroy()  # Supprimer les anciens widgets (anciens graphiques)
    

    # Création du pie chart
    fig = plt.figure(figsize=(frame.winfo_width()/100, frame.winfo_height()/100))
    patches, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90, pctdistance=0.7, wedgeprops=dict(width=0.3, edgecolor='black'))
    # Ajout du texte au-dessus du cercle blanc
    plt.text(0, 0.1, tauxS, fontsize=18, weight="bold", ha='center')
    plt.title("Taux des flux anomalies dans le traffic",fontsize=9, fontname="Arial")

    # Ajout d'un cercle blanc au centre
    fog=plt.gca().add_artist(plt.Circle((0,0), 0.5, fc=current_pie_color))
    plt.axis('equal')  # Assure que le pie chart est dessiné comme un cercle

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_click(event):
        # Vérifier si le clic est à l'intérieur du cercle blanc
        if event.inaxes is not None:
            # Calculer la distance du point de clic au centre du cercle
            distance = (event.xdata**2 + event.ydata**2)**0.5
            if distance <= 0.8:
                # Changer la couleur du cercle central en blanc
                current_pie_color='white'
                fog.set_facecolor(current_pie_color)
                canvas.draw()
                display_data_window(df_pred[df_pred['Label']==1],"Trafics anomalies")
                config.new_anomalie_seen=True

        else :
                display_data_window(df_pred[df_pred['Label']==0],"Trafics normales")

    # Lier l'événement de clic à la fonction on_click
    canvas.mpl_connect('button_press_event', on_click)


#Fonction pour mettre à jour les diagrammes
def update_diagrams(df, current_plot,fig_up,canvas3,fig_s4,fig_s5,canvas1,canvas2):
    print("Mis à jour des diagrammes réussis!!")
    make_current_plot(fig_up,canvas3,df,current_plot)
    lower_seaborn_plot(fig_s4,canvas1,fig_up,canvas3, 
            df, sns.countplot,
            title="Distribution des protocoles utilisés", 
            xlabel="Protocole", ylabel="Count",
            x='pr')
    lower_seaborn_plot(fig_s5, canvas2 ,fig_up,canvas3, 
            df, sns.scatterplot,
            title="Durée du flux vs Quantité de données par protocole",
            xlabel="Durée du flux (s)", ylabel="Quantité de données",
            x='td', y='ibyt', hue='pr', palette='viridis')   

