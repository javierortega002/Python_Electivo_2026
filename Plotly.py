import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ── Parámetros del talud ──────────────────────────────────
beta  = 50   # ángulo del talud (°)
phi   = 28   # ángulo de fricción interna (°)
c     = 20   # cohesión (kPa)
gamma = 18   # peso unitario (kN/m³)
H     = 15   # altura real del talud (m)

# ── Fórmula de Culmann ────────────────────────────────────
beta_r = np.radians(beta)
phi_r  = np.radians(phi)

Hc = (4 * c / gamma) * (
    np.sin(beta_r) * np.cos(phi_r) /
    (1 - np.cos(beta_r - phi_r))
)

ratio  = Hc / H
estado = "ESTABLE" if H < Hc else "INESTABLE"
print(f"Hc = {Hc:.2f} m  |  H = {H} m  |  {estado}")

# ── Curva Hc vs ángulo β ──────────────────────────────────
betas = np.linspace(31, 85, 100)
Hc_curva = (4*c/gamma) * (
    np.sin(np.radians(betas)) * np.cos(phi_r) /
    (1 - np.cos(np.radians(betas) - phi_r))
)

df = pd.DataFrame({'beta': betas, 'Hc': Hc_curva})

# ── Visualización con Plotly ──────────────────────────────
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['beta'], y=df['Hc'],
    mode='lines', name='Altura crítica Hc',
    line=dict(color='#378ADD', width=2)
))
fig.add_hline(y=H, line_dash='dash', line_color='#E24B4A',
             annotation_text=f'H real = {H} m')
fig.add_vline(x=beta, line_dash='dot', line_color='#888780')

fig.update_layout(
    title=f"Culmann — {estado}  (Hc={Hc:.1f} m)",
    xaxis_title="Ángulo del talud β (°)",
    yaxis_title="Altura crítica Hc (m)"
)
fig.show()