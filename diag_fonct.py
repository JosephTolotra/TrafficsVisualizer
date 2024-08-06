import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import *
from collections import Counter
from process import (create_seaborn_plot)

# Fonctions pour chaque type de diagramme
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def line_plot(df):
    diagram = sns.lineplot
    title = "Répartition de trafic par temps (Time vs Traffic)"
    xlabel = "Time"
    ylabel = "Trafic"
    kwargs = {
        'x': 'ts',
        'y': 'tr'
    }
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs
        
def traffic_by_protocol(df):
    diagram = sns.countplot
    title = "Répartition Traffic par Protocole"
    xlabel = "Protocole"
    ylabel = "Count"
    kwargs = {
        'x': 'pr'
    }
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def traffic_histogram(df):
    diagram = sns.histplot
    title = "Histogramme du Traffic"
    xlabel = "Traffic"
    ylabel = "Frequency"
    kwargs = {
        'x': 'tr'
    }
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs
    
def distribution_protocole(df):
    diagram = sns.countplot
    title = "Distribution des protocoles utilisés"
    xlabel = "Protocole"
    ylabel = "Count"
    kwargs = {
        'x': 'tr'
    }
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def quantite_protocole(df):
    df = df.groupby('pr')['ibyt'].sum().reset_index()
    diagram = sns.barplot
    title = "Quantité total de données échangées par protocole"
    xlabel = "Protocole"
    ylabel = "Quantité totale de données échangées"
    kwargs = {'x': 'pr', 'y': 'ibyt', 'palette': 'muted'}
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def donnees_protocole(df):
    diagram = sns.boxplot
    title = "Distribution de la quantité de données par protocole"
    xlabel = "Protocole"
    ylabel = "Quantité de données"
    kwargs = {'x': 'pr', 'y': 'ibyt', 'palette': 'pastel'}
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def duree_protocole(df):
    diagram = sns.boxplot
    title = "Distribution de la durée des flux par protocole"
    xlabel = "Protocole"
    ylabel = "Durée des flux (s)"
    kwargs = {'x': 'pr', 'y': 'td', 'palette': 'pastel'}
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def quantite_temps(df):
    diagram = sns.lineplot
    title = "Quantité de données au Fil du temps"
    xlabel = "Time"
    ylabel = "Quantité de données"
    kwargs = {
        'x': 'ts', 'y': 'ibyt'
    }
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def dureevsquantite(df):
    def add_legend(ax, df):
        ax.legend(title='Protocole')

    diagram = sns.scatterplot
    title = "Durée du flux vs Quantité de données par protocole"
    xlabel = "Durée du flux (s)"
    ylabel = "Quantité de données"
    kwargs = {
        'x': 'td',
        'y': 'ibyt',
        'hue': 'pr',
        'palette': 'viridis'
    }
    accessories = [add_legend]
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def heatmap_correlation(df):
    # df[['ibyt', 'td', 'ipkt', 'opkt']] = df[['ibyt', 'td', 'ipkt', 'opkt']].apply(pd.to_numeric, errors='coerce')
    df.loc[:,['ibyt', 'td', 'ipkt', 'opkt']] = df[['ibyt', 'td', 'ipkt', 'opkt']].apply(pd.to_numeric, errors='coerce')
    df_clean = df[['ibyt', 'td', 'ipkt', 'opkt']].dropna()
    df_correlation = df_clean.corr()
    diagram = sns.heatmap
    title = "Heatmap de Corrélation"
    xlabel = "Features"
    ylabel = "Features"
    kwargs = {
        'annot': True, 'cmap': "coolwarm", 'fmt': ".2f", 'linewidths': .5
    }
    accessories = []
    return df_correlation, diagram, title, xlabel, ylabel, accessories, kwargs

def IPS_frequente(df):
    diagram = sns.countplot
    title = "Visualisation des Addresses IP Sources"
    xlabel = "Source Address"
    ylabel = "Count"
    kwargs = {
        'x': 'sa', 'palette': 'viridis'
    }
    accessories = []
    return df, diagram, title, xlabel, ylabel, accessories, kwargs

def IPD_frequente(df):
    plot_func = sns.countplot
    title = "Visualisation des Addresses IP Destinations"
    xlabel = "Destination Address"
    ylabel = "Count"
    kwargs = {'x': 'da'}
    accessories = []
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def prS_frequente(df):
    # Convertir les résultats en DataFrame
    df_most_common_ports = pd.DataFrame(Counter(df['sp']).items(), columns=['sp', 'Count'])
    top_10_ports = df_most_common_ports.head(10)
    plot_func = sns.countplot
    title = "Visualisation des ports sources les plus fréquents"
    xlabel = "Source Port"
    ylabel = "Count"
    kwargs = {'x': 'sp'}
    accessories = []
    return top_10_ports, plot_func, title, xlabel, ylabel, accessories, kwargs

def prD_frequente(df):
    plot_func = sns.countplot
    title = "Visualisation des ports destinations les plus fréquents"
    xlabel = "Destination Port"
    ylabel = "Count"
    kwargs = {'x': 'dp'}
    accessories = []
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def flux_interface(df):
    # Quantité de données par interface d'entrée
    df = df.groupby('in')['ibyt'].sum().reset_index()
    plot_func = sns.barplot
    title = "Quantité de données par interface d'entrée"
    xlabel = "Interface d'entrée"
    ylabel = "Quantité de données"
    kwargs = {'x': 'in', 'y': 'ibyt', 'palette': 'coolwarm'}
    accessories = []
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def duree_flux(df):
    plot_func = sns.histplot
    title = "Distribution des Durées de Flux"
    xlabel = "Durée du flux (s)"
    ylabel = "Nombre de flux"
    kwargs = {'bins': 50, 'kde': True, 'color': 'green'}
    accessories = []
    return df['td'], plot_func, title, xlabel, ylabel, accessories, kwargs

def entrant_sortie(df):
    def plot_histograms(ax, df):
        sns.histplot(df['ipkt'], ax=ax, bins=50, kde=True, color='blue', label='Paquets entrants')
        sns.histplot(df['opkt'], ax=ax, bins=50, kde=True, color='orange', label='Paquets sortants')
        ax.legend()

    plot_func = None
    title = "Distribution des paquets Entrants et sortants"
    xlabel = "nombre de paquets"
    ylabel = "nombre de flux"
    kwargs = {'bins':50, 'kde':True, 'color':'blue', 'label':'Paquets entrants'}
    accessories = [plot_histograms]
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def flag_tcp(df):
    plot_func = sns.countplot
    title = "Distribution des Flags TCP"
    xlabel = "Flags TCP"
    ylabel = "Nombre de flux"
    kwargs = {'x': 'flg', 'palette': 'coolwarm'}
    accessories = []
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def flux_direction(df):
    plot_func = sns.countplot
    title = "Distribution des Flux par direction"
    xlabel = "Direction"
    ylabel = "Nombre de flux"
    kwargs = {'x': 'dir', 'palette': 'viridis'}
    accessories = []
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def duree_packet(df):
    def add_legend(ax, df):
        ax.legend(title='Protocole')

    plot_func = sns.scatterplot
    title = "Relation entre Durée du flux et taille des paquets"
    xlabel = "Direction"
    ylabel = "Nombre de flux"
    kwargs = {'x': 'td', 'y': 'ibyt', 'hue': 'pr', 'palette': 'viridis', 'alpha': 0.7}
    accessories = [add_legend]
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def sa_da(df):
    ip_matrix = pd.crosstab(df['sa'], df['da'])
    plot_func = sns.heatmap
    title = "Heatmap des Relations entre Adresses IP Source et Destination"
    xlabel = "Adresse IP Destination"
    ylabel = "Adresse IP Source"
    kwargs = {'cmap': 'coolwarm', 'cbar': True}
    accessories = []
    return ip_matrix, plot_func, title, xlabel, ylabel, accessories, kwargs

def traffic_anormaux(df):
    plot_func = sns.boxplot
    title = "Détection des Flux Anormaux par Protocole"
    xlabel = "Protocole"
    ylabel = "Quantité de données (bytes)"
    kwargs = {'x': 'pr', 'y': 'ibyt', 'palette': 'coolwarm'}
    accessories = []
    return df, plot_func, title, xlabel, ylabel, accessories, kwargs

def density_traffic(df):
    # df['td'] = df['td'].apply(pd.to_numeric, errors='coerce')
    df.loc[:,'td'] = df['td'].apply(pd.to_numeric, errors='coerce')
    df_clean = df['td'].dropna() # Supprimer les NaN
    plot_func = sns.kdeplot
    title = "Densité"
    xlabel = "Total duration"
    ylabel = "density"
    kwargs = {'fill': True}
    accessories = []
    return df_clean, plot_func, title, xlabel, ylabel, accessories, kwargs

    
# def comparaison(df):
#     def add_legend(ax):
#         ax.add_legend()

#     accessories = [add_legend]

#     title = "Facet Grid (Traffic by Protocol)"
#     fig = plt.figure()
#     canvas = fig.canvas
#     ax = fig.add_subplot(111)
#     g = sns.FacetGrid(df, ax=ax, col='pr', col_wrap=4)
#     g.map(plt.plot, 'ts', 'td')
#     g.add_legend()
#     fig.subplots_adjust(top=0.9)
#     ax.set_title("Densité")

#     return df, None, title, None, None, accessories, None

def comparaison(df):
    def add_legend(ax,df):
        ax.add_legend()
        g = sns.FacetGrid(df, ax=ax, col='pr', col_wrap=4)
        g.map(plt.plot, 'ts', 'td')
        g.add_legend()
        ax.set_title("Densité")
    accessories = [add_legend]
    title = "Facet Grid (Traffic by Protocol)"
    return df, None, title, None, None, accessories, None

  