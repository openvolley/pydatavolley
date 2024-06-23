"""module to plot the zones of a court"""
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

def draw_court_grid(ax):
    """Draw the basic volleyball court grid."""
    # Horizontal grid lines
    hl = np.array([[0.5, 0.5], [3.5, 0.5], [3.5, 6.5], [0.5, 6.5]])
    ax.plot(hl[:, 0], hl[:, 1], color="black", linewidth=0.5, zorder=1)

    # Zone line along 3m line
    hlz = np.array([[3.5, 4.5], [0.5, 4.5], [0.5, 2.5], [3.5, 2.5]])
    ax.plot(hlz[:, 0], hlz[:, 1], color="black", linewidth=0.5, zorder=1)

    # Vertical grid lines
    vl = np.array([[0.5, 0.5], [0.5, 6.5], [3.5, 6.5], [3.5, 0.5]])
    ax.plot(vl[:, 0], vl[:, 1], color="black", linewidth=0.5, zorder=1)

    # Additional vertical lines for dividing each side into 3 zones
    for i in range(1, 3):
        ax.plot([i + 0.5, i + 0.5], [0.5, 6.5], color="black", linewidth=0.5, zorder=1)

    # Additional horizontal lines for dividing each side into 6 zones
    for i in range(1, 6):
        ax.plot([0.5, 3.5], [i + 0.5, i + 0.5], color="black", linewidth=0.5, zorder=1)

def define_zones():
    """Define the coordinates of the 18 zones on the court."""
    return [
        np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]]),
        np.array([[1.5, 0.5], [2.5, 0.5], [2.5, 1.5], [1.5, 1.5], [1.5, 0.5]]),
        np.array([[2.5, 0.5], [3.5, 0.5], [3.5, 1.5], [2.5, 1.5], [2.5, 0.5]]),
        np.array([[0.5, 1.5], [1.5, 1.5], [1.5, 2.5], [0.5, 2.5], [0.5, 1.5]]),
        np.array([[1.5, 1.5], [2.5, 1.5], [2.5, 2.5], [1.5, 2.5], [1.5, 1.5]]),
        np.array([[2.5, 1.5], [3.5, 1.5], [3.5, 2.5], [2.5, 2.5], [2.5, 1.5]]),
        np.array([[0.5, 2.5], [1.5, 2.5], [1.5, 3.5], [0.5, 3.5], [0.5, 2.5]]),
        np.array([[1.5, 2.5], [2.5, 2.5], [2.5, 3.5], [1.5, 3.5], [1.5, 2.5]]),
        np.array([[2.5, 2.5], [3.5, 2.5], [3.5, 3.5], [2.5, 3.5], [2.5, 2.5]]),
        np.array([[0.5, 3.5], [1.5, 3.5], [1.5, 4.5], [0.5, 4.5], [0.5, 3.5]]),
        np.array([[1.5, 3.5], [2.5, 3.5], [2.5, 4.5], [1.5, 4.5], [1.5, 3.5]]),
        np.array([[2.5, 3.5], [3.5, 3.5], [3.5, 4.5], [2.5, 4.5], [2.5, 3.5]]),
        np.array([[0.5, 4.5], [1.5, 4.5], [1.5, 5.5], [0.5, 5.5], [0.5, 4.5]]),
        np.array([[1.5, 4.5], [2.5, 4.5], [2.5, 5.5], [1.5, 5.5], [1.5, 4.5]]),
        np.array([[2.5, 4.5], [3.5, 4.5], [3.5, 5.5], [2.5, 5.5], [2.5, 4.5]]),
        np.array([[0.5, 5.5], [1.5, 5.5], [1.5, 6.5], [0.5, 6.5], [0.5, 5.5]]),
        np.array([[1.5, 5.5], [2.5, 5.5], [2.5, 6.5], [1.5, 6.5], [1.5, 5.5]]),
        np.array([[2.5, 5.5], [3.5, 5.5], [3.5, 6.5], [2.5, 6.5], [2.5, 5.5]])
    ]

def count_points_in_zones(coordinates_pairs, quadrati):
    """Count the number of points in each zone based on provided coordinates."""
    conteggio_punti = [0] * len(quadrati)
    for pair in coordinates_pairs:
        punto = Point(pair)
        for i, quadrato in enumerate(quadrati):
            if punto.within(Polygon(quadrato)):
                conteggio_punti[i] += 1
    return conteggio_punti

def color_zones(ax, quadrati, conteggio_punti):
    """Color the zones based on the number of points."""
    colors = ['white' if count == 0\
              else 'lightblue' if count < 35\
            else 'blue' for count in conteggio_punti]
    for quadrato, color in zip(quadrati, colors):
        ax.fill(quadrato[:, 0], quadrato[:, 1], color=color)
        ax.plot(quadrato[:, 0], quadrato[:, 1], color='black', linewidth=0.5)

def pycourt_zones(coordinates_pairs, ax=None, invert_y=False):
    """
    Draws a volleyball court with zones and colors them based on the provided coordinate pairs.

    Parameters:
    coordinates_pairs (list of tuple): 
        A list of (x, y) tuples representing coordinates on the court.
    ax (matplotlib.axes._axes.Axes, optional): 
            A matplotlib Axes object to draw the court on. 
            If None, a new figure and axes are created.
    invert_y (bool, optional): If True, inverts the y-axis. Default is False.

    The function performs the following steps:
    1. Draws the volleyball court with horizontal and vertical grid lines.
    2. Defines and draws 18 zones on the court.
    3. Counts the number of points in each zone based on the provided coordinates.
    4. Colors each zone based on the count of points 
        (white if no points, light blue for fewer than 35 points, 
        blue for 35 or more points).
    5. Optionally inverts the y-axis if specified.

    Example:
    coordinates_pairs = [(1, 1), (2, 2), (3, 3), (4, 4)]
    fig, ax = plt.subplots()
    pycourt_zones(coordinates_pairs, ax)
    plt.show()
    """
    if ax is None:
        _, ax = plt.subplots()

    draw_court_grid(ax)
    quadrati = define_zones()
    conteggio_punti = count_points_in_zones(coordinates_pairs, quadrati)
    for i, count in enumerate(conteggio_punti):
        print(f"Square {i + 1}: {count} points")
    color_zones(ax, quadrati, conteggio_punti)
    # Plot the volleyball court
    ax.plot([0.25, 3.75], [3.5, 3.5], color="black", linewidth=5, zorder=1)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])
    # Invert y-axis if needed
    if invert_y:
        ax.invert_yaxis()

def draw_main_grid(ax):
    """Draw the main grid lines of the volleyball court."""
    hl = np.array([[0.5, 0.5], [3.5, 0.5], [3.5, 6.5], [0.5, 6.5]])
    ax.plot(hl[:, 0], hl[:, 1], color="black", linewidth=1, zorder=1)

    hlz = np.array([[3.5, 4.5], [0.5, 4.5], [0.5, 2.5], [3.5, 2.5]])
    ax.plot(hlz[:, 0], hlz[:, 1], color="black", linewidth=1, zorder=1)

    vl = np.array([[0.5, 0.5], [0.5, 6.5], [3.5, 6.5], [3.5, 0.5]])
    ax.plot(vl[:, 0], vl[:, 1], color="black", linewidth=1, zorder=1)

    for i in range(1, 3):
        ax.plot([i + 0.5, i + 0.5], [0.5, 6.5], color="black", linewidth=1, zorder=1)

    for i in range(1, 6):
        ax.plot([0.5, 3.5], [i + 0.5, i + 0.5], color="black", linewidth=1, zorder=1)

def define_zones_pycourtsubzones():
    """Define the main zones of the volleyball court."""
    names = ['5V', '6V', '1V', '7V',
             '8V', '9V', '4V', '3V', 
             '2V', '2U', '3U', '4U', 
             '9U', '8U', '7U', '1U', 
             '6U', '5U']
    quadrati = []
    for row in range(6):
        for col in range(3):
            x_min = 0.5 + col
            x_max = x_min + 1
            y_min = 0.5 + row
            y_max = y_min + 1
            quadrato = np.array([[x_min, y_min], [x_max, y_min],\
                     [x_max, y_max], [x_min, y_max], [x_min, y_min]])
            quadrati.append((quadrato, names[row * 3 + col]))
    return quadrati

def define_subzones_pycoutsubzone(quadrati):
    """Define the subzones within each main zone."""
    names_sub = ['D', 'A', 'C', 'B']
    sottorettangoli = []
    for quadrato in quadrati:
        x_min, y_min = quadrato[0][0]
        x_max, y_max = quadrato[0][2]
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2
        for i, _ in enumerate(names_sub):
            nome_completo = names_sub[i] + quadrato[1]
            if i == 0:
                sottorettangoli.append((np.array([[x_min, y_min],\
                        [x_mid, y_min], [x_mid, y_mid],\
                        [x_min, y_mid], [x_min, y_min]]),\
                        nome_completo)) # top left
            elif i == 1:
                sottorettangoli.append((np.array([[x_mid, y_min],\
                        [x_max, y_min], [x_max, y_mid],\
                        [x_mid, y_mid], [x_mid, y_min]]),\
                        nome_completo)) # top right
            elif i == 2:
                sottorettangoli.append((np.array([[x_min, y_mid],\
                        [x_mid, y_mid], [x_mid, y_max],\
                        [x_min, y_max], [x_min, y_mid]]),\
                        nome_completo)) # bottom left
            elif i == 3:
                sottorettangoli.append((np.array([[x_mid, y_mid],\
                        [x_max, y_mid], [x_max, y_max],\
                        [x_mid, y_max], [x_mid, y_mid]]),\
                        nome_completo)) # bottom right
    return sottorettangoli

def count_points_in_subzones(coordinates_pairs, sottorettangoli):
    """Count the number of points in each subzone based on the provided coordinates."""
    conteggio_punti = [0] * len(sottorettangoli)
    for pair in coordinates_pairs:
        punto = Point(pair)
        for i, (sottorettangolo, _) in enumerate(sottorettangoli):
            if punto.within(Polygon(sottorettangolo)):
                conteggio_punti[i] += 1
    return conteggio_punti

def color_subzones(ax, sottorettangoli, conteggio_punti):
    """Color the subzones based on the number of points."""
    colors = ['white' if count == 0 else 'lightblue'\
        if count < 10 else 'blue' for count in conteggio_punti]
    for (sottorettangolo, _), color in zip(sottorettangoli, colors):
        ax.fill(sottorettangolo[:, 0], sottorettangolo[:, 1], color=color)
        ax.plot(sottorettangolo[:, 0], sottorettangolo[:, 1], color='black', linewidth=0.5)

def plot_points(ax, coordinates_pairs):
    """Plot points on the court."""
    for x, y in coordinates_pairs:
        ax.plot(x, y, marker='o', markersize=5, color='red')

def pycourtsubzones(coordinates_pairs, ax=None, invert_y=False):
    """
    Draws a volleyball court with subzones and colors them based on the provided coordinate pairs.

    Parameters:
    coordinates_pairs (list of tuple): 
        A list of (x, y) tuples representing coordinates on the court.
    ax (matplotlib.axes._axes.Axes, optional):
        A matplotlib Axes object to draw the court on. 
        If None, a new figure and axes are created.
    
    invert_y (bool, optional): 
        If True, inverts the y-axis. Default is False.

    The function performs the following steps:
    1. Draws the volleyball court with horizontal and vertical grid lines.
    2. Defines and draws 18 zones on the court.
    3. Subdivides each zone into 4 subzones.
    4. Counts the number of points in each subzone
       based on the provided coordinates.
    5. Colors each subzone based on the count of points
       (white if no points, light blue for fewer than 
       10 points, blue for 10 or more points).
    6. Optionally inverts the y-axis if specified.

    Example:
    coordinates_pairs = [(1, 1), (2, 2), (3, 3), (4, 4)]
    fig, ax = plt.subplots()
    pycourtSubZones(coordinates_pairs, ax)
    plt.show()
    """
    if ax is None:
        _, ax = plt.subplots()

    draw_main_grid(ax)
    quadrati = define_zones_pycourtsubzones()
    sottorettangoli = define_subzones_pycoutsubzone(quadrati)
    conteggio_punti = count_points_in_subzones(coordinates_pairs, sottorettangoli)
    color_subzones(ax, sottorettangoli, conteggio_punti)
    plot_points(ax, coordinates_pairs)
    for quadrato, _ in quadrati:
        ax.plot(quadrato[:, 0], quadrato[:, 1], color='black', linewidth=1)
    # Plot the volleyball court
    ax.plot([0.25, 3.75], [3.5, 3.5], color="black", linewidth=5, zorder=1)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])
    # Invert y-axis if needed
    if invert_y:
        ax.invert_yaxis()
