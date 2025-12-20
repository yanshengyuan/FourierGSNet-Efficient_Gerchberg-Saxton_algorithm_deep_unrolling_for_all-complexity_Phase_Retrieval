import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.ndimage import gaussian_filter

plt.rcParams['font.family'] = 'Times New Roman'
FontSize = 23

# -----------------------------
# Read Excel data
# -----------------------------
df = pd.read_excel("MAE_grid.xlsx", index_col=0)

batch_sizes = df.index.values.astype(float)
learning_rates = df.columns.values.astype(float)
mae_values = df.values

# -----------------------------
# Original coarse grid
# -----------------------------
BS, LR = np.meshgrid(batch_sizes, learning_rates, indexing="ij")

# Flatten for interpolation
points = np.column_stack((BS.flatten(), LR.flatten()))
values = mae_values.flatten()

# -----------------------------
# Create dense grid (smooth surface)
# -----------------------------
bs_dense = np.linspace(batch_sizes.min(), batch_sizes.max(), 2000)
lr_dense = np.linspace(learning_rates.min(), learning_rates.max(), 2000)

BS_dense, LR_dense = np.meshgrid(bs_dense, lr_dense)

# -----------------------------
# 2D interpolation (more stable)
# -----------------------------
MAE_dense = griddata(
    points,
    values,
    (BS_dense, LR_dense),
    method="linear"
)

# -----------------------------
# Smooth the surface (post-processing)
# -----------------------------
MAE_dense_smooth = gaussian_filter(MAE_dense, sigma=1.2)

# -----------------------------
# Plot
# -----------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

surface = ax.plot_surface(
    BS_dense,
    LR_dense,
    MAE_dense_smooth,
    cmap="viridis",
    edgecolor="none",
    linewidth=0,
    antialiased=False,
    alpha=1.0
)

# -----------------------------
# Plot original experiment points
# (use colormap, NOT black)
# -----------------------------
mae_min, mae_max = mae_values.min(), mae_values.max()
sizes = 50 + 200 * (mae_values.flatten() - mae_min) / (mae_max - mae_min)

scatter = ax.scatter(
    BS.flatten(),
    LR.flatten(),
    mae_values.flatten(),
    c=mae_values.flatten(),
    cmap=plt.cm.Greys_r,
    s=sizes,
    linewidth=1.2,
    edgecolor="k",
    depthshade=False
)

# -----------------------------
# Labels
# -----------------------------
ax.set_xlabel("Batch size", fontsize=FontSize, labelpad=15)
ax.set_ylabel("Initial learning rate", fontsize=FontSize, labelpad=15)
ax.set_zlabel("MAE ↓ [rad]", fontsize=FontSize, labelpad=15)
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=18)
ax.tick_params(axis='z', labelsize=18)

ax.view_init(elev=25, azim=135)

plt.tight_layout()

plt.savefig(
    "MAE_surface.png",
    dpi=600,
    bbox_inches="tight"
)
plt.show()