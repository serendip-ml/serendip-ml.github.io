#!/usr/bin/env python3
"""Generate scaling curve chart for fine-tuning blog post (dark and light versions)."""

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# Font configuration - DejaVu Sans (bold works reliably)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# Bold font for bar labels
font_bold = FontProperties(family='DejaVu Sans', weight='bold', size=11)

# Data: model sizes and ratings
models = ['0.5B', '1.5B', '3B', '7B', '14B', '32B', '72B']
base = np.array([1.18, 1.49, 1.55, 1.70, 1.81, 1.90, 2.21])
sft = np.array([1.34, 2.24, 2.56, 2.76, 2.96, 3.00, 2.95])
dpo = np.array([1.48, 2.44, 2.70, 2.84, 3.07, 3.04, 3.10])

# Calculate lifts for stacking
sft_lift = np.where(np.isnan(sft), 0, sft - base)
dpo_lift = np.where(np.isnan(dpo), 0, dpo - sft)

# Haiku reference
haiku_avg = 2.62

# Theme colors
THEMES = {
    'dark': {
        'bg_color': '#1a1a1a',
        'text_color': '#e0e0e0',
        'grid_color': '#333333',
        'base_color': '#4a5568',
        'sft_color': '#3182ce',
        'dpo_color': '#48bb78',
        'haiku_color': '#ed8936',
    },
    'light': {
        'bg_color': '#ffffff',
        'text_color': '#222222',
        'grid_color': '#cccccc',
        'base_color': '#6b7280',
        'sft_color': '#2563eb',
        'dpo_color': '#16a34a',
        'haiku_color': '#ea580c',
    },
}


def generate_chart(theme_name: str, suffix: str = ''):
    """Generate chart for a given theme."""
    t = THEMES[theme_name]
    x = np.arange(len(models))
    width = 0.6

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=t['bg_color'])
    ax.set_facecolor(t['bg_color'])

    # Stacked bars
    bars_base = ax.bar(x, base, width, label='Base',
                       color=t['base_color'], edgecolor=t['bg_color'])
    bars_sft = ax.bar(x, sft_lift, width, bottom=base, label='+SFT',
                      color=t['sft_color'], edgecolor=t['bg_color'])
    bars_dpo = ax.bar(x, dpo_lift, width, bottom=base + sft_lift, label='+DPO',
                      color=t['dpo_color'], edgecolor=t['bg_color'])

    # Haiku reference line
    ax.axhline(y=haiku_avg, color=t['haiku_color'], linestyle='--', linewidth=2,
               label=f'Haiku ({haiku_avg})')

    # Add value labels on top of bars
    for i, (b, s, d) in enumerate(zip(base, sft, dpo)):
        val = d if not np.isnan(d) else b
        ax.text(i, val + 0.06, f'{val:.2f}', ha='center', va='bottom',
                color=t['text_color'], fontproperties=font_bold)

    # Styling
    ax.set_xlabel('Qwen 2.5 Model Size', color=t['text_color'], fontsize=12)
    ax.set_ylabel('Joke Quality (1-5 stars)', color=t['text_color'], fontsize=12)
    ax.set_title('Joke Telling Quality After Fine-tuning',
                 color=t['text_color'], fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, color=t['text_color'])
    ax.tick_params(colors=t['text_color'])
    ax.set_ylim(1, 3.5)
    ax.set_yticks([1, 1.5, 2, 2.5, 3, 3.5])

    # Grid
    ax.yaxis.grid(True, color=t['grid_color'], linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Legend - order to match visuals (top to bottom)
    handles, labels = ax.get_legend_handles_labels()
    order = [3, 2, 1, 0]  # +DPO, +SFT, Base, Haiku
    legend = ax.legend([handles[i] for i in order], [labels[i] for i in order],
                       loc='upper left', facecolor=t['bg_color'], edgecolor=t['grid_color'])
    for text in legend.get_texts():
        text.set_color(t['text_color'])

    # Spines
    for spine in ax.spines.values():
        spine.set_color(t['grid_color'])

    plt.tight_layout()

    # Save
    base_path = f'../assets/images/scaling-curve{suffix}'
    plt.savefig(f'{base_path}.svg', format='svg', facecolor=t['bg_color'], edgecolor='none')
    plt.savefig(f'{base_path}.png', format='png', dpi=150, facecolor=t['bg_color'], edgecolor='none')
    print(f'Saved {base_path}.svg and .png')

    plt.close(fig)


if __name__ == '__main__':
    generate_chart('dark', '')
    generate_chart('light', '-light')
