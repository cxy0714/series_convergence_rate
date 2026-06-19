"""Shared plotting style and small helpers for the convergence-rate experiments.

All experiments save vector PDF figures into ../figures and print the key
numbers they produce so the LaTeX paper can quote validated values.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIGDIR, exist_ok=True)

plt.rcParams.update({
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 120,
    "savefig.bbox": "tight",
    "lines.linewidth": 1.8,
    "lines.markersize": 5,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "mathtext.fontset": "cm",
})

# A small consistent colour cycle.
C = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b"]


def savefig(fig, name):
    path = os.path.join(FIGDIR, name)
    fig.savefig(path)
    plt.close(fig)
    print(f"  [saved] {os.path.relpath(path)}")


def banner(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)
