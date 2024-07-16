import os
import ast
import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Datei öffnen und Zeilen lesen
def read_raw():
    with open('raw/rndgraph0.1-20_3-1-3_001.txt', 'r') as file:
        lines = file.readlines()

    # Initialisierung der Variablen
    V = []
    A = []

    # Durch die Zeilen iterieren und Werte extrahieren
    for line in lines:
        line = line.strip()
        if line.startswith("V ="):
            V = ast.literal_eval(line.split('=', 1)[1].strip())
        elif line.startswith("A ="):
            A = ast.literal_eval(line.split('=', 1)[1].strip())
    
    return A,V

def read_solution():
    # XML-Datei einlesen
    x_variablen = []
    y_variablen = []
    z_variablen = []
    a_variablen = []
    tree = ET.parse('solutions/rndgraph0.1-20_3-1-3_001.qlp.sol')
    root = tree.getroot()

    for variable in root.findall('.//variable'):
        name = variable.get('name')
        value = float(variable.get('value'))
        
        if value == 1:
            if name.startswith('x_'):
                x_variablen.append(int(name.split("_")[1]))
            elif name.startswith('y_'):
                y_variablen.append(int(name.split("_")[1]))
            elif name.startswith('z_'):
                z_variablen.append(int(name.split("_")[1]))
            elif name.startswith('alpha_'):
                a_variablen.append(int(name.split("_")[1]))

    return x_variablen, y_variablen, z_variablen, a_variablen 
    
    

def plott_solution(A,V,x_variablen, y_variablen, z_variablen, a_variablen):
    G = nx.DiGraph()

    # Knoten und Kanten hinzufügen
    G.add_nodes_from(V)
    G.add_edges_from(A)
    node_colors = []

    for node in V:
        if node in x_variablen:
            node_colors.append('blue')
        elif node in y_variablen:
            node_colors.append('purple')
        elif node in z_variablen:
            node_colors.append('green')
        elif node in a_variablen:
            node_colors.append('red')
        else:
            node_colors.append('lightblue')

    # Netzwerk visualisieren
    plt.figure(figsize=(14, 8))

    # Verwende shell_layout für eine schöne horizontale Anordnung
    pos = nx.shell_layout(G)

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500, font_size=10, arrows=True)
    plt.title("Visualisierung des gerichteten Netzwerks (horizontal)")
    plt.show()


if __name__ == "__main__":
    x, y, z, a = read_solution()
    A,V = read_raw()
    plott_solution(A,V,x,y,z,a)


