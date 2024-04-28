import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon


def pycourtZones(coordinates_pairs, ax=None, invert_y=False):
    if ax is None:
        fig, ax = plt.subplots()

    

    # Horizontal grid lines
    hl = np.array([[0.5, 0.5], [3.5, 0.5], [3.5, 6.5], [0.5, 6.5]])
    plt.plot(hl[:, 0], hl[:, 1], color="black", linewidth=0.5, zorder=1)


    # Zone line along 3m line
    hlz = np.array([[3.5, 4.5], [0.5, 4.5], [0.5, 2.5], [3.5, 2.5]])
    plt.plot(hlz[:, 0], hlz[:, 1], color="black", linewidth=0.5, zorder=1)

    # Vertical grid lines
    vl = np.array([[0.5, 0.5], [0.5, 6.5], [3.5, 6.5], [3.5, 0.5]])
    plt.plot(vl[:, 0], vl[:, 1], color="black", linewidth=0.5, zorder=1)

    # Additional vertical lines for dividing each side into 3 zones
    for i in range(1, 3):
        plt.plot([i + 0.5, i + 0.5], [0.5, 6.5], color="black", linewidth=0.5, zorder=1)

    # Additional horizontal lines for dividing each side into 6 zones
    for i in range(1, 6):
        plt.plot([0.5, 3.5], [i + 0.5, i + 0.5], color="black", linewidth=0.5, zorder=1)


    # Quadrato 1 (prima riga, prima colonna)
    quadrato1 = np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]])

    # Quadrato 2 (prima riga, seconda colonna)
    quadrato2 = np.array([[1.5, 0.5], [2.5, 0.5], [2.5, 1.5], [1.5, 1.5], [1.5, 0.5]])

    # Quadrato 3 (prima riga, terza colonna)
    quadrato3 = np.array([[2.5, 0.5], [3.5, 0.5], [3.5, 1.5], [2.5, 1.5], [2.5, 0.5]])

    # Quadrato 4 (seconda riga, prima colonna)
    quadrato4 = np.array([[0.5, 1.5], [1.5, 1.5], [1.5, 2.5], [0.5, 2.5], [0.5, 1.5]])

    # Quadrato 5 (seconda riga, seconda colonna)
    quadrato5 = np.array([[1.5, 1.5], [2.5, 1.5], [2.5, 2.5], [1.5, 2.5], [1.5, 1.5]])

    # Quadrato 6 (seconda riga, terza colonna)
    quadrato6 = np.array([[2.5, 1.5], [3.5, 1.5], [3.5, 2.5], [2.5, 2.5], [2.5, 1.5]])

    # Quadrato 7 (terza riga, prima colonna)
    quadrato7 = np.array([[0.5, 2.5], [1.5, 2.5], [1.5, 3.5], [0.5, 3.5], [0.5, 2.5]])

    # Quadrato 8 (terza riga, seconda colonna)
    quadrato8 = np.array([[1.5, 2.5], [2.5, 2.5], [2.5, 3.5], [1.5, 3.5], [1.5, 2.5]])

    # Quadrato 9 (terza riga, terza colonna)
    quadrato9 = np.array([[2.5, 2.5], [3.5, 2.5], [3.5, 3.5], [2.5, 3.5], [2.5, 2.5]])

    # Quadrato 10 (quarta riga, prima colonna)
    quadrato10 = np.array([[0.5, 3.5], [1.5, 3.5], [1.5, 4.5], [0.5, 4.5], [0.5, 3.5]])

    # Quadrato 11 (quarta riga, seconda colonna)
    quadrato11 = np.array([[1.5, 3.5], [2.5, 3.5], [2.5, 4.5], [1.5, 4.5], [1.5, 3.5]])

    # Quadrato 12 (quarta riga, terza colonna)
    quadrato12 = np.array([[2.5, 3.5], [3.5, 3.5], [3.5, 4.5], [2.5, 4.5], [2.5, 3.5]])

    # Quadrato 13 (quinta riga, prima colonna)
    quadrato13 = np.array([[0.5, 4.5], [1.5, 4.5], [1.5, 5.5], [0.5, 5.5], [0.5, 4.5]])

    # Quadrato 14 (quinta riga, seconda colonna)
    quadrato14 = np.array([[1.5, 4.5], [2.5, 4.5], [2.5, 5.5], [1.5, 5.5], [1.5, 4.5]])

    # Quadrato 15 (quinta riga, terza colonna)
    quadrato15 = np.array([[2.5, 4.5], [3.5, 4.5], [3.5, 5.5], [2.5, 5.5], [2.5, 4.5]])

    # Quadrato 16 (sesta riga, prima colonna)
    quadrato16 = np.array([[0.5, 5.5], [1.5, 5.5], [1.5, 6.5], [0.5, 6.5], [0.5, 5.5]])

    # Quadrato 17 (sesta riga, seconda colonna)
    quadrato17 = np.array([[1.5, 5.5], [2.5, 5.5], [2.5, 6.5], [1.5, 6.5], [1.5, 5.5]])

    # Quadrato 18 (sesta riga, terza colonna)
    quadrato18 = np.array([[2.5, 5.5], [3.5, 5.5], [3.5, 6.5], [2.5, 6.5], [2.5, 5.5]])

    # Lista contenente tutti i quadrati
    quadrati = [quadrato1, quadrato2, quadrato3, quadrato4, quadrato5, quadrato6, quadrato7, quadrato8, quadrato9,
                quadrato10, quadrato11, quadrato12, quadrato13, quadrato14, quadrato15, quadrato16, quadrato17, quadrato18]


    #Conteggio e colorazione zone
    conteggio_punti = [0] * len(quadrati)

    # Conteggio dei punti in ciascun quadrato
    for pair in coordinates_pairs:
        punto = Point(pair)
        for i, quadrato in enumerate(quadrati):
            if punto.within(Polygon(quadrato)):
                conteggio_punti[i] += 1

  
    for i, quadrato in enumerate(quadrati):
        print(f"Quadrato {i+1}: {conteggio_punti[i]} punti")

    
    colors = ['white' if count == 0 else 'lightblue' if count < 35 else 'blue' for count in conteggio_punti]


    for quadrato, color in zip(quadrati, colors):
        ax.fill(quadrato[:, 0], quadrato[:, 1], color=color)
        ax.plot(quadrato[:, 0], quadrato[:, 1], color='black', linewidth=0.5)



    # Plot the volleyball court
    ax.plot([0.25, 3.75], [3.5, 3.5], color="black", linewidth=5, zorder=1)



    ax.set_xlim(0, 4)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])

    # Inverti l'asse y se necessario
    if invert_y:
        plt.gca().invert_yaxis()



def pycourtSubZones(coordinates_pairs, ax=None, invert_y=False):
    if ax is None:
        fig, ax = plt.subplots()

    # Horizontal grid lines
    hl = np.array([[0.5, 0.5], [3.5, 0.5], [3.5, 6.5], [0.5, 6.5]])
    plt.plot(hl[:, 0], hl[:, 1], color="black", linewidth=1, zorder=1)  # Increased linewidth

    # Zone line along 3m line
    hlz = np.array([[3.5, 4.5], [0.5, 4.5], [0.5, 2.5], [3.5, 2.5]])
    plt.plot(hlz[:, 0], hlz[:, 1], color="black", linewidth=1, zorder=1)  # Increased linewidth

    # Vertical grid lines
    vl = np.array([[0.5, 0.5], [0.5, 6.5], [3.5, 6.5], [3.5, 0.5]])
    plt.plot(vl[:, 0], vl[:, 1], color="black", linewidth=1, zorder=1)  # Increased linewidth

    # Additional vertical lines for dividing each side into 3 zones
    for i in range(1, 3):
        plt.plot([i + 0.5, i + 0.5], [0.5, 6.5], color="black", linewidth=1, zorder=1)  # Increased linewidth

    # Additional horizontal lines for dividing each side into 6 zones
    for i in range(1, 6):
        plt.plot([0.5, 3.5], [i + 0.5, i + 0.5], color="black", linewidth=1, zorder=1)  # Increased linewidth

    # Define quadrati
    quadrati = []
    names = ['5V', '6V', '1V', '7V', '8V', '9V', '4V', '3V', '2V', '2U', '3U', '4U', '9U', '8U', '7U', '1U', '6U', '5U']
    for row in range(6):
        for col in range(3):
            x_min = 0.5 + col
            x_max = x_min + 1
            y_min = 0.5 + row
            y_max = y_min + 1
            quadrato = np.array([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max], [x_min, y_min]])
            quadrati.append((quadrato, names[row*3 + col]))  # Associa il nome del quadrato in base all'ordine
            

    names_sub = ['D','A','C','B']
    # Subdivide each quadrato into 4 sottorettangoli
    sottorettangoli = []
    for quadrato in quadrati:
        x_min, y_min = quadrato[0][0]
        x_max, y_max = quadrato[0][2]
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2
        for i, name_sub in enumerate(names_sub):
            nome_completo = names_sub[i] + quadrato[1]
            if i == 0:
                sottorettangoli.append((np.array([[x_min, y_min], [x_mid, y_min], [x_mid, y_mid], [x_min, y_mid], [x_min, y_min]]), nome_completo)) # top left
            elif i == 1:
                sottorettangoli.append((np.array([[x_mid, y_min], [x_max, y_min], [x_max, y_mid], [x_mid, y_mid], [x_mid, y_min]]), nome_completo)) # top right
            elif i == 2:
                sottorettangoli.append((np.array([[x_min, y_mid], [x_mid, y_mid], [x_mid, y_max], [x_min, y_max], [x_min, y_mid]]), nome_completo)) # bottom left
            elif i == 3:
                sottorettangoli.append((np.array([[x_mid, y_mid], [x_max, y_mid], [x_max, y_max], [x_mid, y_max], [x_mid, y_mid]]), nome_completo)) # bottom right



    # Count and color zones
    conteggio_punti = [0] * len(sottorettangoli)

    # Count points in each quadrato
    for pair in coordinates_pairs:
        punto = Point(pair)
        for i, (sottorettangolo, name) in enumerate(sottorettangoli):
            if punto.within(Polygon(sottorettangolo)):
                conteggio_punti[i] += 1


    colors = ['white' if count == 0 else 'lightblue' if count < 10 else 'blue' for count in conteggio_punti]

    for (sottorettangolo, name), color in zip(sottorettangoli, colors):
        ax.fill(sottorettangolo[:, 0], sottorettangolo[:, 1], color=color)
        ax.plot(sottorettangolo[:, 0], sottorettangolo[:, 1], color='black', linewidth=0.5)  # Increased linewidth
    
    
    for quadrato, name in quadrati:
        ax.plot(quadrato[:, 0], quadrato[:, 1], color='black', linewidth=1)

    # Plot points
    for x, y in coordinates_pairs:
        ax.plot(x, y, marker='o', markersize=5, color='red')  # Imposta il marker 'o' (cerchio) rosso con dimensione 5





    # Plot the volleyball court
    ax.plot([0.25, 3.75], [3.5, 3.5], color="black", linewidth=5, zorder=1)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])

    # Invert y-axis if needed
    if invert_y:
        plt.gca().invert_yaxis()

