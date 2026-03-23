"""Generate 4 editorial images for Capital on Tap review."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

OUT = Path('assets/images/capital-on-tap-review')
OUT.mkdir(parents=True, exist_ok=True)

# --- Shared style ---
BG = '#FFFFFF'
DARK = '#1a1a2e'
ACCENT_RED = '#c0392b'
ACCENT_AMBER = '#e67e22'
ACCENT_GREEN = '#27ae60'
ACCENT_BLUE = '#2c3e50'
GREY = '#7f8c8d'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
    'font.size': 13,
    'axes.facecolor': BG,
    'figure.facecolor': BG,
    'axes.edgecolor': '#ddd',
    'axes.grid': False,
    'text.color': DARK,
})

# ============================================================
# IMAGE 1: Rate Reality
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

labels = ['Floor rate\n(best case)', 'Representative APR\n(51% offered this)', 'Average rate paid\n(Q4 2025)']
values = [13.86, 34.9, 46.05]
colors = [ACCENT_GREEN, ACCENT_AMBER, ACCENT_RED]

bars = ax.barh(labels, values, color=colors, height=0.55, edgecolor='white', linewidth=1.5)

for bar, val in zip(bars, values):
    ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
            f'{val}%', va='center', ha='left', fontsize=15, fontweight='bold', color=DARK)

ax.set_xlim(0, 56)
ax.set_xlabel('Annual Percentage Rate (APR)', fontsize=11, color=GREY)
ax.set_title('Capital on Tap: What Rate Will You Actually Pay?',
             fontsize=16, fontweight='bold', pad=15, color=DARK)
ax.xaxis.set_major_formatter(mticker.PercentFormatter())
ax.tick_params(axis='y', length=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

fig.text(0.98, 0.02, 'Source: capitalontap.com, verified March 2026', ha='right', fontsize=8, color=GREY)

plt.tight_layout()
fig.savefig(OUT / 'capital-on-tap-rate-reality-floor-vs-average.png', dpi=150, bbox_inches='tight')
plt.close()
print('Image 1: Rate reality - done')

# ============================================================
# IMAGE 2: Monthly cost on 10k balance
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

rate_labels = ['Floor rate\n13.86%', 'Rep APR\n34.9%', 'Average rate\n46.05%']
monthly_costs = [115, 291, 383]
colors2 = [ACCENT_GREEN, ACCENT_AMBER, ACCENT_RED]

bars = ax.bar(rate_labels, monthly_costs, color=colors2, width=0.5, edgecolor='white', linewidth=1.5)

for bar, cost in zip(bars, monthly_costs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
            f'\u00a3{cost}', ha='center', fontsize=18, fontweight='bold', color=DARK)

ax.set_ylim(0, 480)
ax.set_ylabel('Monthly interest charge', fontsize=11, color=GREY)
ax.set_title('Monthly Interest on a \u00a310,000 Balance',
             fontsize=16, fontweight='bold', pad=15, color=DARK)
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('\u00a3{x:,.0f}'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', length=0)

# Gap annotation
mid_y = (383 + 115) / 2
ax.annotate('', xy=(2.35, 383), xytext=(2.35, 115),
            arrowprops=dict(arrowstyle='<->', color=GREY, lw=1.5))
ax.text(2.55, mid_y, '\u00a3268/mo\ndifference', ha='left', va='center', fontsize=10,
        color=ACCENT_RED, fontweight='bold')

fig.text(0.98, 0.02, 'Approximate figures based on simple interest calculation', ha='right', fontsize=8, color=GREY)

plt.tight_layout()
fig.savefig(OUT / 'capital-on-tap-monthly-interest-cost-10k-balance.png', dpi=150, bbox_inches='tight')
plt.close()
print('Image 2: Monthly cost - done')

# ============================================================
# IMAGE 3: Credit limit comparison
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))

cards = ['Capital on Tap', 'Funding Circle', 'Lloyds', 'Barclaycard', 'NatWest']
limits = [250000, 30000, 25000, 15000, 15000]
card_colors = [ACCENT_BLUE, '#8e44ad', '#2980b9', '#16a085', '#2980b9']

bars = ax.barh(cards, limits, color=card_colors, height=0.55, edgecolor='white', linewidth=1.5)

for bar, val in zip(bars, limits):
    label = f'\u00a3{val:,}'
    ax.text(bar.get_width() + 3000, bar.get_y() + bar.get_height()/2,
            label, va='center', ha='left', fontsize=13, fontweight='bold', color=DARK)

ax.set_xlim(0, 310000)
ax.set_xlabel('Maximum credit limit', fontsize=11, color=GREY)
ax.set_title('Business Credit Card Limits Compared',
             fontsize=16, fontweight='bold', pad=15, color=DARK)
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('\u00a3{x:,.0f}'))
ax.tick_params(axis='y', length=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

fig.text(0.98, 0.02, 'Maximum advertised limits, March 2026. Individual limits vary by applicant.', ha='right', fontsize=8, color=GREY)

plt.tight_layout()
fig.savefig(OUT / 'business-credit-card-limit-comparison-chart.png', dpi=150, bbox_inches='tight')
plt.close()
print('Image 3: Limit comparison - done')

# ============================================================
# IMAGE 4: Decision flowchart
# ============================================================
fig, ax = plt.subplots(figsize=(9, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

def draw_box(x, y, w, h, text, color, text_color='white', fontsize=11, bold=False):
    from matplotlib.patches import FancyBboxPatch
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle='round,pad=0.1',
                          facecolor=color, edgecolor='white', linewidth=2, zorder=2)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight=weight, zorder=3, linespacing=1.4)

def draw_diamond(x, y, w, h, text, color='#34495e'):
    verts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y), (x, y+h/2)]
    poly = plt.Polygon(verts, facecolor=color, edgecolor='white', linewidth=2, zorder=2)
    ax.add_patch(poly)
    ax.text(x, y, text, ha='center', va='center', fontsize=10,
            color='white', fontweight='bold', zorder=3, linespacing=1.3)

# Title
ax.text(5, 9.5, 'Should You Apply for Capital on Tap?',
        ha='center', fontsize=16, fontweight='bold', color=DARK)

# Q1: Ltd company?
draw_box(5, 8.6, 3.8, 0.6, 'Are you a UK limited company or LLP?', ACCENT_BLUE, fontsize=11, bold=True)

# Q1 No -> stop
ax.annotate('', xy=(1.8, 8.6), xytext=(3.1, 8.6),
            arrowprops=dict(arrowstyle='->', color=ACCENT_RED, lw=1.5), zorder=1)
ax.text(2.5, 8.85, 'No', fontsize=9, color=ACCENT_RED, fontweight='bold')
draw_box(1.2, 7.9, 2.2, 0.65, 'Cannot apply.\nSee sole trader cards.', ACCENT_RED, fontsize=9)

# Q1 Yes -> Q2
ax.annotate('', xy=(5, 7.9), xytext=(5, 8.3),
            arrowprops=dict(arrowstyle='->', color=ACCENT_GREEN, lw=1.5), zorder=1)
ax.text(5.2, 8.1, 'Yes', fontsize=9, color=ACCENT_GREEN, fontweight='bold')

# Q2: Clear monthly?
draw_diamond(5, 7.4, 3.8, 0.9, 'Will you clear the\nbalance monthly?')

# Q2 Yes -> Q3
ax.annotate('', xy=(5, 6.5), xytext=(5, 6.95),
            arrowprops=dict(arrowstyle='->', color=ACCENT_GREEN, lw=1.5), zorder=1)
ax.text(5.2, 6.7, 'Yes', fontsize=9, color=ACCENT_GREEN, fontweight='bold')

# Q2 No -> caution
ax.annotate('', xy=(8.2, 7.4), xytext=(6.9, 7.4),
            arrowprops=dict(arrowstyle='->', color=ACCENT_AMBER, lw=1.5), zorder=1)
ax.text(7.4, 7.65, 'No', fontsize=9, color=ACCENT_AMBER, fontweight='bold')
draw_box(8.5, 6.6, 2.6, 0.95, 'Check your offered rate.\nIf above 25%, consider\nBarclaycard at 25.5%.', ACCENT_AMBER, fontsize=9)

# Q3: Need limit above 25k?
draw_box(5, 6.1, 3.8, 0.6, 'Do you need a limit above \u00a325k?', ACCENT_BLUE, fontsize=11, bold=True)

# Q3 Yes -> strong fit
ax.annotate('', xy=(5, 5.3), xytext=(5, 5.8),
            arrowprops=dict(arrowstyle='->', color=ACCENT_GREEN, lw=1.5), zorder=1)
ax.text(5.2, 5.55, 'Yes', fontsize=9, color=ACCENT_GREEN, fontweight='bold')
draw_box(5, 4.8, 3.8, 0.7, 'Capital on Tap is a strong fit.\n\u00a3250k limit, 1% cashback,\nno bank switch needed.', ACCENT_GREEN, fontsize=10, bold=True)

# Q3 No -> compare
ax.annotate('', xy=(1.8, 6.1), xytext=(3.1, 6.1),
            arrowprops=dict(arrowstyle='->', color=GREY, lw=1.5), zorder=1)
ax.text(2.5, 6.35, 'No', fontsize=9, color=GREY, fontweight='bold')
draw_box(1.2, 5.4, 2.2, 0.65, 'Compare bank cards.\nLloyds or Barclaycard\nmay offer better rates.', GREY, fontsize=9)

# Footer
ax.text(5, 3.8, 'Application is a soft search \u2014 checking your rate does not affect your credit file.',
        ha='center', fontsize=9, color=GREY, fontstyle='italic')

fig.savefig(OUT / 'capital-on-tap-should-you-apply-decision-flowchart.png', dpi=150, bbox_inches='tight')
plt.close()
print('Image 4: Decision flowchart - done')

print('\nAll 4 images generated in:', OUT)
for f in sorted(OUT.glob('*.png')):
    print(f'  {f.name} ({f.stat().st_size // 1024}KB)')
