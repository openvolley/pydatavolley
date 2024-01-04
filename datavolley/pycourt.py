import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def pycourt(ax=None):
    if ax == None:
        fig, ax = plt.subplots()

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
    if ax == None:
        fig, ax = plt.subplots()
        
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
