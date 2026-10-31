#!/usr/bin/env python3
"""Draw the exact phase boundaries (theorems, not simulations). Writes phase_diagram.pdf/.png next to the manuscript."""
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False,
                     'svg.hashsalt': 'inhib', 'pdf.fonttype': 42})
b, c, d = 1.0, 1.0, 2.0
p = np.linspace(.001, .985, 600)
lam = np.linspace(.03, 7, 500)
P, L = np.meshgrid(p, lam)
fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.4), sharey=True, layout='constrained')
regions = [d + L*np.log(P) < b, b*L*(1-P) > d*c]
boundaries = [(d-b)/(-np.log(p)), d*c/(b*(1-p))]
titles = ['Conversion inhibition (S + I → 2I)', 'Catalytic inhibition (I + 2S → I + S)']
for ax, region, boundary, title in zip(axs, regions, boundaries, titles):
    ax.pcolormesh(P, L, region.astype(int), cmap=ListedColormap(['#EDE4D8', '#683F69']), shading='auto', rasterized=True)
    ax.plot(p, boundary, color='#D49B36', lw=2.3, label='exact threshold (non-explosive)')
    ax.set(xlim=(0, .98), ylim=(0, 7), xlabel='Inhibitor retention probability p', title=title)
    ax.text(.035, 6.55, 'Explosion possible', color='white', fontsize=9)
    ax.text(.70, .10, 'Non-explosive', color='#403044', fontsize=9, transform=ax.transAxes)
    ax.grid(alpha=.16, color='white')
ma = (d-b)/(1-p)
axs[0].plot(p, ma, color='white', lw=1.6, ls='--', label='same mean removal by a well-mixed reaction')
axs[0].legend(loc='upper left', bbox_to_anchor=(0.02, 0.87), fontsize=7.5, frameon=False, labelcolor='white')
axs[1].text(.035, 5.4, 'well-mixed removal gives\nthe same threshold', color='white', fontsize=8)
axs[0].set_ylabel('Division coefficient λ')
axs[0].plot([0], [3], marker='o', color='#D49B36', markersize=7, clip_on=False)
axs[0].annotate('Example: P(explosion) ≈ 0.7975\nfrom (S, I) = (3, 0)', xy=(0, 3), xytext=(.06, 2.15), fontsize=8.5, color='white',
                arrowprops={'arrowstyle': '->', 'color': 'white'})
fig.suptitle('Inhibitor segregation thresholds for b = c = 1 and d = 2', fontsize=13, fontweight='bold')
fig.supxlabel('Initial S ≥ 2, any finite I. Left: the band between the dashed and gold curves is the purely compartmental effect.', fontsize=9)
fig.savefig(OUT/'phase_diagram.pdf', bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
fig.savefig(OUT/'phase_diagram.png', dpi=190, bbox_inches='tight', metadata={'Software': None})
