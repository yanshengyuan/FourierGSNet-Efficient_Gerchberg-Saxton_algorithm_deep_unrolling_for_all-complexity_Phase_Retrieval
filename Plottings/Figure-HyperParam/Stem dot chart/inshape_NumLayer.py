import pandas as pd
import matplotlib.pyplot as plt

# ================= Global style =================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({'font.size': 20})

# ================= Load data =================
df = pd.read_excel('inshape.xlsx')  # 只包含前6个 dataset

layers = [5, 10, 15]
datasets = df['Datasets'].unique()  # 前6个 dataset

markers = ['o', 'D', '^', 'x', '*', 'v']

# ================= Figure =================
fig = plt.figure(figsize=(12, 10), dpi=400)

# ================= MAE =================
ax1 = plt.subplot(2, 2, 1)
for i, name in enumerate(datasets):
    y = df[df['Datasets'] == name].set_index('Number of unrolled layers M').loc[layers, 'MAE'].values
    ax1.stem(layers, y, markerfmt=markers[i], linefmt='--', label=name)

ax1.set_xlabel('Number of unrolled layers $M$')
ax1.set_ylabel('MAE', labelpad=2)
ax1.set_title('MAE')
ax1.set_yscale('log')
ax1.set_xlim(4, 16)
ax1.margins(x=0.1)

# ================= SSIM =================
ax2 = plt.subplot(2, 2, 2)
for i, name in enumerate(datasets):
    y = df[df['Datasets'] == name].set_index('Number of unrolled layers M').loc[layers, 'SSIM'].values
    ax2.stem(layers, y, markerfmt=markers[i], linefmt='--')

ax2.set_xlabel('Number of unrolled layers $M$')
ax2.set_ylabel('SSIM', labelpad=2)
ax2.set_title('SSIM')
ax2.set_yscale('log')
ax2.set_xlim(4, 16)
ax2.margins(x=0.1)

# ================= FRCM =================
ax3 = plt.subplot(2, 2, 3)
for i, name in enumerate(datasets):
    y = df[df['Datasets'] == name].set_index('Number of unrolled layers M').loc[layers, 'FRCM'].values
    ax3.stem(layers, y, markerfmt=markers[i], linefmt='--')

ax3.set_xlabel('Number of unrolled layers $M$')
ax3.set_ylabel('FRCM', labelpad=2)
ax3.set_title('FRCM')
ax3.set_yscale('log')
ax3.set_xlim(4, 16)
ax3.margins(x=0.1)

# ================= Recons =================
ax4 = plt.subplot(2, 2, 4)
for i, name in enumerate(datasets):
    y = df[df['Datasets'] == name].set_index('Number of unrolled layers M').loc[layers, 'Recons'].values
    ax4.stem(layers, y, markerfmt=markers[i], linefmt='--', label=name)

ax4.set_xlabel('Number of unrolled layers $M$')
ax4.set_ylabel('ReconsErr', labelpad=2)
ax4.set_title('Reconstruction error')
ax4.set_yscale('log')
ax4.set_xlim(4, 16)
ax4.margins(x=0.1)

ax1.set_xticks([5, 10, 15])
ax2.set_xticks([5, 10, 15])
ax3.set_xticks([5, 10, 15])
ax4.set_xticks([5, 10, 15])

# ================= Shared legend =================
# ================= Shared legend =================
handles, labels = ax1.get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc='upper center',
    ncol=3,
    frameon=True,           # 显示边框
    edgecolor='black',      # 边框颜色
    framealpha=1.0,         # 透明度
    bbox_to_anchor=(0.4, 1.08)
)


# ================= Finalize =================
plt.tight_layout()
plt.show()
plt.savefig('NumLayer_inshape.png')