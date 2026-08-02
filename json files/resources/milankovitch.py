import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator

# === CONFIGURAÇÃO PARA METADE DE UM A4 RETRATO (A5 / HALF-PAGE) ===
# 5.83 x 8.27 polegadas @ 300 DPI
FIG_WIDTH_INCHES = 5.8
FIG_HEIGHT_INCHES = 8.0

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7.0,             # Fonte base ajustada para layout A5
    'axes.titlesize': 8.0,        # Título dos subgráficos
    'axes.labelsize': 7.5,        # Nomes dos eixos
    'xtick.labelsize': 6.5,       # Números dos eixos X
    'ytick.labelsize': 6.5,       # Números dos eixos Y
    'legend.fontsize': 6.5,       # Legendas
    'lines.linewidth': 0.7,       # Espessura das linhas otimizada
    'figure.dpi': 300,            # Resolução gráfica para impressão
    'axes.labelpad': 3.0          # Distância entre título e linha do eixo
})

# === SÉRIES TEMPORAIS (SINTÉTICAS PARA DEMONSTRAÇÃO) ===
t = np.linspace(-800, 0, 2000)

obliquity = 23.44 + 0.8 * np.sin(2 * np.pi * t / 41) + 0.2 * np.cos(2 * np.pi * t / 29)
eccentricity = 0.03 + 0.015 * np.sin(2 * np.pi * t / 100) + 0.008 * np.cos(2 * np.pi * t / 405)
precession_sin = np.sin(2 * np.pi * t / 23 + 0.5 * np.sin(2 * np.pi * t / 100))
precession_index = eccentricity * precession_sin
insolation = 480 + 35 * precession_index + 15 * (obliquity - 23.44)

d18O = 4.0 - 0.6 * precession_index - 0.4 * (obliquity - 23.44) + 0.1 * np.random.normal(0, 1, len(t))
temp_vostok = -4.0 + 5.0 * (4.5 - d18O) + 0.2 * np.random.normal(0, 1, len(t))

mask_vostok = t >= -420
t_vostok = t[mask_vostok]
temp_vostok = temp_vostok[mask_vostok]

# === MONTAGEM DO GRID NA PROPORÇÃO METADE A4 ===
fig = plt.figure(figsize=(FIG_WIDTH_INCHES, FIG_HEIGHT_INCHES))
gs = gridspec.GridSpec(6, 1, hspace=0.25, left=0.14, right=0.96, top=0.93, bottom=0.07)

colors = {
    'obliquity': '#1f77b4',
    'eccentricity': '#2ca02c',
    'prec_index': '#d62728',
    'insolation': '#333333',
    'd18O': '#8c564b',
    'temp': '#17becf'
}

fig.suptitle('Milankovitch Orbital Forcing & Paleoclimate', fontsize=9.5, fontweight='bold', y=0.97)

# 1. Obliquity
ax0 = fig.add_subplot(gs[0])
ax0.plot(t, obliquity, color=colors['obliquity'])
ax0.set_ylabel(r'$\epsilon$ [deg]')
ax0.set_title('Obliquity (≈41 kyr)', pad=3)
ax0.grid(True, linestyle='--', alpha=0.3)

# 2. Eccentricity
ax1 = fig.add_subplot(gs[1], sharex=ax0)
ax1.plot(t, eccentricity, color=colors['eccentricity'])
ax1.set_ylabel(r'$e$')
ax1.set_title('Eccentricity (100 & 405 kyr)', pad=3)
ax1.grid(True, linestyle='--', alpha=0.3)

# 3. Precession Index
ax2 = fig.add_subplot(gs[2], sharex=ax0)
ax2.plot(t, precession_index, color=colors['prec_index'])
ax2.set_ylabel(r'$e \sin(\varpi)$')
ax2.set_title('Precessional Index (≈23 kyr)', pad=3)
ax2.grid(True, linestyle='--', alpha=0.3)

# 4. Insolation 65N
ax3 = fig.add_subplot(gs[3], sharex=ax0)
ax3.plot(t, insolation, color=colors['insolation'], linewidth=0.6)
ax3.set_ylabel(r'$\overline{Q}^{\text{day}}_{\text{65N}}$ [W m$^{-2}$]')
ax3.set_title('TOA Insolation (Summer 65°N)', pad=3)
ax3.grid(True, linestyle='--', alpha=0.3)

# 5. Benthic d18O
ax4 = fig.add_subplot(gs[4], sharex=ax0)
ax4.plot(t, d18O, color=colors['d18O'], linewidth=0.6, label='LR04 Benthic')
ax4.set_ylabel(r'$\delta^{18}\text{O}$ [‰]')
ax4.set_title(r'Benthic $\delta^{18}\text{O}$ Stack', pad=3)
ax4.invert_yaxis()
ax4.grid(True, linestyle='--', alpha=0.3)
ax4.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.8)

# 6. Temperature Anomaly (Vostok)
ax5 = fig.add_subplot(gs[5], sharex=ax0)
ax5.plot(t_vostok, temp_vostok, color=colors['temp'], linewidth=0.6, label='Vostok Temp.')
ax5.set_ylabel(r'$\Delta T_{\text{surface}}$ [K]')
ax5.set_xlabel('Time [thousands of years BP (ka BP)]')
ax5.set_title('Antarctic Surface Temperature Anomaly', pad=3)
ax5.set_xlim([-800, 0])
ax5.grid(True, linestyle='--', alpha=0.3)
ax5.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.8)

# Ocultar rótulos do eixo X nos painéis superiores
for ax in [ax0, ax1, ax2, ax3, ax4]:
    plt.setp(ax.get_xticklabels(), visible=False)

# === EXPORTAÇÃO ===
output_filename = 'milankovitch_a5_portrait.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Figura gerada no formato Metade A4 (A5) com sucesso: {output_filename}")
plt.show()