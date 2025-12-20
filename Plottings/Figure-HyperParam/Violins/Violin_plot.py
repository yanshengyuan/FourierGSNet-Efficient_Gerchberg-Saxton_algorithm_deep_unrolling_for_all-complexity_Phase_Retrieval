import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

sns.set(style='whitegrid', context='notebook', font_scale=2.25)
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['savefig.dpi'] = 300

metrics = ["MAE", "SSIM", "FRCM", "ReconsErr"]
metrics = ["MAE", "SSIM", "FRCM"]

beamshape="CDI/"

fig, axes = plt.subplots(1, len(metrics), figsize=(7*len(metrics), 7))
axes = axes.flatten()

for idx, metric in enumerate(metrics):
    metric=metrics[idx]+"/"
    ten = beamshape+metric+"10.npy"
    fifteen = beamshape+metric+"15.npy"
    five = beamshape+metric+"5.npy"

    ten = np.load(ten)
    fifteen = np.load(fifteen)
    five = np.load(five)

    values = np.concatenate([
        five,
        ten,
        fifteen
    ])

    groups = ['5', '10', '15']
    lengths = [len(five), len(ten), len(fifteen)]

    group_labels = np.concatenate([
        [g] * l for g, l in zip(groups, lengths)
    ])

    df = pd.DataFrame({
        'value': values,
        'group': group_labels
    })

    palette = sns.color_palette("Paired")
    ax = axes[idx]
    
    sns.violinplot(
        x='group',
        y='value',
        data=df,
        palette=palette,
        inner=None,
        linewidth=1,
        cut=0,
        scale="width",
        width=0.8,
        ax = ax
    )
    for violin in ax.collections:
        violin.set_alpha(0.5)

    group_means = [df[df['group'] == g]['value'].mean() for g in groups]
    if(metric=="MAE/"):
        mark=min(group_means)
    if(metric=="SSIM/"):
        mark=max(group_means)
    if(metric=="FRCM/"):
        mark=min(group_means)
    if(metric=="ReconsErr/"):
        mark=min(group_means)
        
    for i, mean in enumerate(group_means):
        ax.scatter(i, mean, color='red', s=80, zorder=10, edgecolor='white', linewidth=1.2, label='Mean' if i == 0 else "")

    group_maxes = [df[df['group'] == g]['value'].max() for g in groups]
    for i, maxx in enumerate(group_maxes):
        #ax.vlines(x=i, ymin=df['value'].min(), ymax=maxx, color='black', linewidth=2.5, alpha=0.8, linestyle=(0, (2, 2)))
        mean = group_means[i]
        if(mean==mark):
            ax.text(i, group_maxes[i], f'{mean:.3f}', ha='center', va='bottom', color="mediumseagreen")
        else:
            ax.text(i, group_maxes[i], f'{mean:.3f}', ha='center', va='bottom', color='black')

    ax.set_xlabel(r"Number of unrolled layers $M$", fontsize=30)

    if(metric=="MAE/"):
        ax.set_ylabel("MAE ↓ [rad]", fontsize=30)
    if(metric=="SSIM/"):
        ax.set_ylabel("SSIM ↑ [a.u.]", fontsize=30)
    if(metric=="FRCM/"):
        ax.set_ylabel("FRCM ↓ [a.u.]", fontsize=30)
    if(metric=="ReconsErr/"):
        ax.set_ylabel("ReconsErr ↓ [a.u.]", fontsize=30)

    sns.despine()
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['5', '10', '15'], fontsize=26)

    ax.legend_.remove() if ax.get_legend() else None
    plt.tight_layout()

plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.savefig("Violins/M_comparison_" + beamshape[:-1] + ".png", dpi=300, bbox_inches='tight')
plt.show()