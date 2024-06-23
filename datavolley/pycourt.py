"""module to plout a court"""
import matplotlib.pyplot as plt
import numpy as np

def pycourt(ax=None):
    """
    Draws a volleyball court on a given matplotlib Axes object.

    Parameters:
    ax (matplotlib.axes._axes.Axes, optional): 
        A matplotlib Axes object to draw the court on. 
        If None, a new figure and axes are created.

    The function performs the following steps:
    1. Plots the boundary lines of the volleyball court.
    2. Adds horizontal and vertical grid lines 
       to represent the zones and 3-meter lines.
    3. Sets the court limits and aspect ratio to ensure 
       the court is drawn to scale.
    4. Removes axis ticks for a cleaner presentation.

    Example:
    fig, ax = plt.subplots()
    pycourt(ax)
    plt.show()
    """
    if ax is None:
        _, ax = plt.subplots()

    # Plot the volleyball court
    plt.plot([0.25, 3.75], [3.5, 3.5], color="black", linewidth=2, zorder=1)

    # Horizontal grid lines
    hl = np.array([[0.5, 0.5], [3.5, 0.5], [3.5, 6.5], [0.5, 6.5]])
    plt.plot(hl[:, 0], hl[:, 1], color="black", linewidth=0.5, zorder=1)

    # Zone line along 3m line
    hlz = np.array([[3.5, 4.5], [0.5, 4.5], [0.5, 2.5], [3.5, 2.5]])
    plt.plot(hlz[:, 0], hlz[:, 1], color="black", linewidth=0.5, zorder=1)

    # Vertical grid lines
    vl = np.array([[0.5, 0.5], [0.5, 6.5], [3.5, 6.5], [3.5, 0.5]])
    plt.plot(vl[:, 0], vl[:, 1], color="black", linewidth=0.5, zorder=1)

    # Set court limits and aspect ratio
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])

def half_pycourt(ax=None):
    """
    Draws the upper half of a volleyball court on a given matplotlib Axes object.

    Parameters:
    ax (matplotlib.axes._axes.Axes, optional): 
        A matplotlib Axes object to draw the court on. 
        If None, a new figure and axes are created.

    The function performs the following steps:
    1. Plots the net line and the upper half of the volleyball court.
    2. Adds horizontal and vertical grid lines to represent 
       the zones and the 3-meter line.
    3. Sets the court limits and aspect ratio to ensure
       the upper half of the court is drawn to scale.
    4. Removes axis ticks for a cleaner presentation.

    Example:
    fig, ax = plt.subplots()
    half_pycourt(ax)
    plt.show()
    """
    if ax is None:
        _, ax = plt.subplots()      
    # Plot the upper half of the volleyball court
    plt.plot([0.25, 3.75], [3.5, 3.5], color="black", linewidth=2, zorder=1)  # Net line
    # Upper horizontal grid lines
    hl = np.array([[0.5, 3.5], [3.5, 3.5], [3.5, 6.5], [0.5, 6.5]])
    plt.plot(hl[:, 0], hl[:, 1], color="black", linewidth=0.5, zorder=1)

    # Zone line along 3m line
    hlz = np.array([[3.5, 4.5], [0.5, 4.5]])
    plt.plot(hlz[:, 0], hlz[:, 1], color="black", linewidth=0.5, zorder=1)

    # Upper vertical grid lines
    vl = np.array([[0.5, 3.5], [0.5, 6.5], [3.5, 6.5], [3.5, 3.5]])
    plt.plot(vl[:, 0], vl[:, 1], color="black", linewidth=0.5, zorder=1)

    # Set court limits and aspect ratio for the upper half
    ax.set_xlim(0, 4)
    ax.set_ylim(3.5, 7)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])
    
