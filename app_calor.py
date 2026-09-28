import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PALETA GRUVBOX
# ============================================================
GRUVBOX = {
    "bg0_hard": "#1d2021", "bg0": "#282828", "bg1": "#3c3836",
    "bg2": "#504945", "fg0": "#fbf1c7", "fg1": "#ebdbb2",
    "fg2": "#d5c4a1", "fg3": "#bdae93", "fg4": "#a89984",
    "red": "#fb4934", "green": "#b8bb26", "yellow": "#fabd2f",
    "blue": "#83a598", "purple": "#d3869b", "aqua": "#8ec07c",
    "orange": "#fe8019", "gray": "#928374",
}
CORES_PARAM = {
    "T_L": GRUVBOX["orange"], "T_R": GRUVBOX["yellow"],
    "T_init": GRUVBOX["aqua"], "alpha": GRUVBOX["purple"],
    "N": GRUVBOX["blue"],
}
GRUVBOX_THERMAL = [
    [0.00, "#458588"], [0.20, GRUVBOX["blue"]],
    [0.40, GRUVBOX["aqua"]], [0.60, GRUVBOX["yellow"]],
    [0.80, GRUVBOX["orange"]], [1.00, GRUVBOX["red"]],
]

# ============================================================
# VISTAS PREDEFINIDAS
# ============================================================
VISTAS_PDE = {
    "Isométrica": dict(x=1.6,  y=-1.7, z=1.3),
    "Frontal":    dict(x=0.05, y=-2.5, z=0.0),
    "Lateral":    dict(x=2.5,  y=0.0,  z=0.05),
    "Topo":       dict(x=0.05, y=0.0,  z=2.5),
    "Traseira":   dict(x=-1.6, y=1.7,  z=1.3),
    "Base":       dict(x=0.0,  y=0.0,  z=-2.5),
}
VISTAS_GEOM = {
    "Isométrica": dict(x=1.4,  y=1.6,  z=1.2),
    "Frontal":    dict(x=0.0,  y=2.5,  z=0.0),
    "Lateral":    dict(x=2.5,  y=0.0,  z=0.0),
    "Topo":       dict(x=0.0,  y=0.0,  z=2.5),
    "Traseira":   dict(x=-1.4, y=-1.6, z=1.2),
    "Base":       dict(x=0.0,  y=0.0,  z=-2.5),
}
DESC_PDE = {
    "Isométrica": "Perspectiva 3D completa da solução.",
    "Frontal":    "Plano x–u. Corte de temperatura ao longo da barra.",
    "Lateral":    "Plano t–u. Evolução temporal em posição fixa.",
    "Topo":       "Plano x–t. Diagrama espaço-tempo.",
    "Traseira":   "Perspectiva oposta — face final.",
    "Base":       "Face inicial (t = 0), vista por baixo.",
}
DESC_GEOM = {
    "Isométrica": "Perspectiva 3D do cilindro/barra.",
    "Frontal":    "Seção transversal.",
    "Lateral":    "Vista longitudinal.",
    "Topo":       "Vista superior — distribuição axial.",
    "Traseira":   "Perspectiva oposta.",
    "Base":       "Vista inferior.",
}

# ============================================================
# PERFIS DE QUALIDADE (payload × fidelidade)
# ============================================================
PERFIS_QUALIDADE = {
    "Econômico": {"res_x": 40,  "res_radial": 8,  "cap_frames": 24},
    "Padrão":    {"res_x": 60,  "res_radial": 12, "cap_frames": 30},
    "Alta":      {"res_x": 100, "res_radial": 24, "cap_frames": 60},
}

# ============================================================
# PÁGINA
# ============================================================
st.set_page_config(
    page_title="Oficina de Fourier: Calor 3D",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(f"""
    <style>
        .stApp {{ background-color: {GRUVBOX["bg0_hard"]}; color: {GRUVBOX["fg1"]}; }}
        section[data-testid="stSidebar"] {{
            background-color: {GRUVBOX["bg0"]};
            border-right: 1px solid {GRUVBOX["bg2"]};
        }}
        section[data-testid="stSidebar"] * {{ color: {GRUVBOX["fg1"]}; }}
        h1, h2, h3, h4 {{
            color: {GRUVBOX["orange"]} !important;
            font-family: "JetBrains Mono", "Fira Code", monospace;
            letter-spacing: 0.5px;
        }}
        p, span, label, div {{ color: {GRUVBOX["fg1"]}; }}
        .katex-html {{ color: {GRUVBOX["fg0"]} !important; font-size: 1.1em; }}
        hr {{ border-color: {GRUVBOX["bg2"]}; }}
        div[data-baseweb="slider"] div[role="slider"] {{
            background-color: {GRUVBOX["orange"]} !important;
        }}
        div[data-testid="stAlert"] {{
            background-color: {GRUVBOX["bg1"]};
            border: 1px solid {GRUVBOX["bg2"]};
            color: {GRUVBOX["fg0"]};
        }}
        div[data-baseweb="select"] > div {{
            background-color: {GRUVBOX["bg1"]};
            color: {GRUVBOX["fg0"]};
            border-color: {GRUVBOX["bg2"]};
        }}
        details {{
            background-color: {GRUVBOX["bg0"]} !important;
            border: 1px solid {GRUVBOX["bg2"]} !important;
            border-radius: 6px !important;
        }}
        details > summary {{
            color: {GRUVBOX["fg0"]} !important;
            font-family: "JetBrains Mono", monospace !important;
            font-weight: 600 !important;
        }}
        details[open] > summary {{ border-bottom: 1px solid {GRUVBOX["bg2"]}; }}
        .view-panel {{
            background-color: {GRUVBOX["bg0"]};
            border: 1px solid {GRUVBOX["bg2"]};
            border-radius: 8px;
            padding: 12px 14px 4px 14px;
            margin-top: 8px; margin-bottom: 12px;
        }}
        .view-panel-title {{
            color: {GRUVBOX["yellow"]};
            font-family: "JetBrains Mono", monospace;
            font-size: 0.85rem; font-weight: 600;
            letter-spacing: 1px; text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .view-panel-desc {{
            color: {GRUVBOX["fg3"]};
            font-family: "JetBrains Mono", monospace;
            font-size: 0.78rem;
            margin-top: 8px; padding-top: 8px;
            border-top: 1px dashed {GRUVBOX["bg2"]};
        }}
        div[data-testid="stButton"] > button[kind="primary"] {{
            background-color: {GRUVBOX["orange"]} !important;
            color: {GRUVBOX["bg0_hard"]} !important;
            border: 1px solid {GRUVBOX["orange"]} !important;
            font-family: "JetBrains Mono", monospace !important;
            font-weight: 700 !important;
            border-radius: 5px !important;
        }}
        div[data-testid="stButton"] > button[kind="secondary"] {{
            background-color: {GRUVBOX["bg1"]} !important;
            color: {GRUVBOX["fg1"]} !important;
            border: 1px solid {GRUVBOX["bg2"]} !important;
            font-family: "JetBrains Mono", monospace !important;
            font-weight: 500 !important;
            border-radius: 5px !important;
        }}
        div[data-testid="stButton"] > button[kind="secondary"]:hover {{
            background-color: {GRUVBOX["bg2"]} !important;
            color: {GRUVBOX["orange"]} !important;
            border-color: {GRUVBOX["orange"]} !important;
        }}
    </style>
""", unsafe_allow_html=True)


# ============================================================
# ESTADO
# ============================================================
DEFAULTS = {"T_L": 100, "T_R": 0, "T_init": 20, "alpha": 0.50, "N": 40}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(f"ws_{k}", v)
    st.session_state.setdefault(f"wi_{k}", v)
st.session_state.setdefault("view_atual", "Isométrica")


def sync_from_sidebar(p):
    def cb(): st.session_state[f"wi_{p}"] = st.session_state[f"ws_{p}"]
    return cb


def sync_from_inline(p):
    def cb(): st.session_state[f"ws_{p}"] = st.session_state[f"wi_{p}"]
    return cb


def val(p): return st.session_state[f"ws_{p}"]


# ============================================================
# CABEÇALHO
# ============================================================
st.title("Simulador Computacional: Equação do Calor")
st.markdown(
    "Ajuste os parâmetros nos cartões ou na barra lateral. Escolha entre "
    "**vista única** (girando com o mouse) ou **mosaico 3×2** com as 6 "
    "perspectivas animadas em sincronia."
)

# ============================================================
# EQUAÇÃO INTERATIVA
# ============================================================
st.markdown("## Equação Governante")
st.latex(r'''
\frac{\partial u}{\partial t} = \textcolor{#d3869b}{\alpha}\,\frac{\partial^2 u}{\partial x^2}
\quad\Longrightarrow\quad
u(x,t) = \textcolor{#fe8019}{T_L}
+ \frac{x}{L}\!\left(\textcolor{#fabd2f}{T_R} - \textcolor{#fe8019}{T_L}\right)
+ \sum_{n=1}^{\textcolor{#83a598}{N}}
\textcolor{#8ec07c}{b_n}\!\left(\textcolor{#8ec07c}{T_{\text{init}}}\right)
\sin\!\left(\frac{n\pi x}{L}\right)
\, e^{-\textcolor{#d3869b}{\alpha}\left(\frac{n\pi}{L}\right)^2 t}
''')

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    with st.expander("T_L", expanded=False):
        st.markdown(f"<span style='color:{CORES_PARAM['T_L']}'>●</span> "
                    "**Temperatura na borda esquerda**", unsafe_allow_html=True)
        st.number_input("Valor (°C)", 0, 100, key="wi_T_L",
                        on_change=sync_from_inline("T_L"))
with c2:
    with st.expander("T_R", expanded=False):
        st.markdown(f"<span style='color:{CORES_PARAM['T_R']}'>●</span> "
                    "**Temperatura na borda direita**", unsafe_allow_html=True)
        st.number_input("Valor (°C)", 0, 100, key="wi_T_R",
                        on_change=sync_from_inline("T_R"))
with c3:
    with st.expander("T_init", expanded=False):
        st.markdown(f"<span style='color:{CORES_PARAM['T_init']}'>●</span> "
                    "**Temperatura inicial**", unsafe_allow_html=True)
        st.number_input("Valor (°C)", 0, 100, key="wi_T_init",
                        on_change=sync_from_inline("T_init"))
with c4:
    with st.expander("α", expanded=False):
        st.markdown(f"<span style='color:{CORES_PARAM['alpha']}'>●</span> "
                    "**Difusividade térmica**", unsafe_allow_html=True)
        st.number_input("Valor", 0.01, 2.00, step=0.01, format="%.2f",
                        key="wi_alpha", on_change=sync_from_inline("alpha"))
with c5:
    with st.expander("N", expanded=False):
        st.markdown(f"<span style='color:{CORES_PARAM['N']}'>●</span> "
                    "**Número de harmônicos**", unsafe_allow_html=True)
        st.number_input("Valor", 1, 150, step=1, key="wi_N",
                        on_change=sync_from_inline("N"))

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("Parâmetros Termodinâmicos")
    st.subheader("Condições de Contorno")
    st.slider("Temp. Esquerda (T_L)", 0, 100, key="ws_T_L",
              on_change=sync_from_sidebar("T_L"))
    st.slider("Temp. Direita (T_R)", 0, 100, key="ws_T_R",
              on_change=sync_from_sidebar("T_R"))
    st.slider("Temp. Inicial (T_init)", 0, 100, key="ws_T_init",
              on_change=sync_from_sidebar("T_init"))

    st.subheader("Física e Matemática")
    st.slider("Difusividade Térmica (α)", 0.01, 2.00, step=0.01, format="%.2f",
              key="ws_alpha", on_change=sync_from_sidebar("alpha"))
    st.slider("Harmônicos de Fourier (N)", 1, 150, key="ws_N",
              on_change=sync_from_sidebar("N"))

    st.subheader("Visualização")
    tipo_viz = st.radio(
        "Tipo de gráfico 3D",
        ["Superfície u(x,t) — solução da EDP",
         "Geometria física colorida"],
        index=0
    )
    modo_layout = st.radio(
        "Layout",
        ["Única vista", "Mosaico 3×2 (6 vistas)"],
        index=0
    )

    if tipo_viz.startswith("Geometria"):
        geometria = st.selectbox(
            "Formato da Geometria",
            ["Cilindro Metálico", "Barra Retangular", "Fio Fino"]
        )
    else:
        geometria = None

    modo_mosaico = modo_layout.startswith("Mosaico")

    if modo_mosaico:
        qualidade = st.select_slider(
            "Qualidade do mosaico",
            options=list(PERFIS_QUALIDADE.keys()),
            value="Econômico",
            help="Controla resolução e número de frames. Econômico evita "
                 "travamentos em máquinas modestas."
        )
        perfil = PERFIS_QUALIDADE[qualidade]
    else:
        qualidade = "Alta"
        perfil = PERFIS_QUALIDADE["Alta"]

    if not modo_mosaico:
        st.subheader("Animação")
        modo_animacao = st.radio(
            "Comportamento da câmera",
            ["Câmera fixa (você controla)", "Rotação automática"],
            index=0
        )
        voltas_camera = (st.slider("Voltas da câmera", 0.5, 3.0, 1.0, 0.25)
                         if modo_animacao == "Rotação automática" else 0.0)
    else:
        modo_animacao = "Câmera fixa (você controla)"
        voltas_camera = 0.0
        st.info("No mosaico, as 6 câmeras ficam fixas. Um único Play anima "
                "todas em sincronia.")

    t_final = st.slider("Duração total (s)", 1.0, 30.0, 12.0, 0.5)

    # Slider de frames com faixa FIXA. O corte é interno.
    n_frames_asked = st.slider("Nº de frames", 20, 120, 40, 5)

cap_frames = perfil["cap_frames"]
n_frames = min(n_frames_asked, cap_frames)
if n_frames_asked != n_frames:
    st.caption(
        f"Usando **{n_frames}** frames (limite do perfil **{qualidade}**). "
        f"Aumente a qualidade do mosaico para usar mais."
    )

res_x = perfil["res_x"] if modo_mosaico else 100
res_radial = perfil["res_radial"] if modo_mosaico else 24

T_L, T_R = val("T_L"), val("T_R")
T_init, alpha, N = val("T_init"), val("alpha"), int(val("N"))


# ============================================================
# MOTOR MATEMÁTICO
# ============================================================
@st.cache_data(show_spinner=False)
def calcular_perfil(T_L, T_R, T_init, alpha, N, t, L=10.0, resolucao=100):
    x_vals = np.linspace(0, L, resolucao)
    steady = T_L + (x_vals / L) * (T_R - T_L)
    transient = np.zeros_like(x_vals)
    for n in range(1, N + 1):
        term1 = (T_init - T_L) * (1 - (-1) ** n)
        term2 = (T_R - T_L) * ((-1) ** n)
        bn = (2.0 / (n * np.pi)) * (term1 + term2)
        decay = np.exp(-alpha * ((n * np.pi) / L) ** 2 * t)
        transient += bn * np.sin(n * np.pi * x_vals / L) * decay
    return x_vals, steady + transient


@st.cache_data(show_spinner=False)
def gerar_geometria(geometria, x_vals, resolucao_radial=24):
    if geometria == "Cilindro Metálico":
        r, theta = 1.0, np.linspace(0, 2 * np.pi, resolucao_radial)
    elif geometria == "Barra Retangular":
        r = 1.2
        theta = np.array([np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4, 9*np.pi/4])
    else:  # Fio Fino
        r, theta = 0.2, np.linspace(0, 2 * np.pi, resolucao_radial)
    X, Theta = np.meshgrid(x_vals, theta)
    Y = r * np.cos(Theta)
    Z = r * np.sin(Theta)
    return X, Y, Z, len(theta)


@st.cache_data(show_spinner="Calculando solução u(x,t)...")
def calcular_solucao_2d(T_L, T_R, T_init, alpha, N, t_final, n_frames,
                        L=10.0, resolucao=100):
    tempos = np.linspace(0.0, t_final, n_frames)
    x_vals = np.linspace(0, L, resolucao)
    U = np.zeros((n_frames, resolucao), dtype=np.float32)
    for i, t in enumerate(tempos):
        # CORRIGIDO: passa resolucao para calcular_perfil
        _, u = calcular_perfil(T_L, T_R, T_init, alpha, N, float(t),
                                L=L, resolucao=resolucao)
        U[i] = u
    return x_vals, tempos, U


@st.cache_data(show_spinner="Calculando difusão térmica...")
def calcular_frames_geom(T_L, T_R, T_init, alpha, N, geometria,
                         t_final, n_frames, resolucao_x, resolucao_radial):
    tempos = np.linspace(0.0, t_final, n_frames)
    x_vals, _ = calcular_perfil(T_L, T_R, T_init, alpha, N, 0.0,
                                 resolucao=resolucao_x)
    X, Y, Z, n_theta = gerar_geometria(geometria, tuple(x_vals),
                                        resolucao_radial=resolucao_radial)
    perfis = np.zeros((n_frames, resolucao_x), dtype=np.float32)
    for i, t in enumerate(tempos):
        _, u = calcular_perfil(T_L, T_R, T_init, alpha, N, float(t),
                                resolucao=resolucao_x)
        perfis[i] = u
    return {"tempos": tempos, "x_vals": x_vals, "X": X, "Y": Y, "Z": Z,
            "n_theta": n_theta, "perfis": perfis}


# ============================================================
# HELPERS
# ============================================================
def posicao_camera_auto_pde(p, nv):
    a = 2 * np.pi * nv * p - np.pi / 3
    return 2.2 * np.cos(a), 2.2 * np.sin(a), 1.5


def posicao_camera_auto_geom(p, nv):
    a = 2 * np.pi * nv * p + np.pi / 4
    return 1.4, 2.0 * np.cos(a), 2.0 * np.sin(a)


def botoes_play_pause(duracao, y_pos=1.12):
    return [dict(
        type="buttons", direction="left",
        x=0.02, y=y_pos, xanchor="left", yanchor="top",
        showactive=False, bgcolor=GRUVBOX["bg1"],
        bordercolor=GRUVBOX["orange"],
        font=dict(color=GRUVBOX["fg0"], size=13,
                  family="JetBrains Mono, monospace"),
        pad=dict(r=8, t=8),
        buttons=[
            dict(label="Play", method="animate",
                 args=[None, dict(frame=dict(duration=duracao, redraw=True),
                                  fromcurrent=True,
                                  transition=dict(duration=0),
                                  mode="immediate")]),
            dict(label="Pause", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=True),
                                    mode="immediate",
                                    transition=dict(duration=0))])
        ]
    )]


def config_eixos_3d(geom_tipo):
    aspect = (dict(x=1.9, y=1.5, z=1.2) if geom_tipo == "pde"
              else dict(x=2.5, y=0.5, z=0.5))
    return dict(
        xaxis=dict(showbackground=False, showgrid=False,
                   zeroline=False, showticklabels=False, title=''),
        yaxis=dict(showbackground=False, showgrid=False,
                   zeroline=False, showticklabels=False, title=''),
        zaxis=dict(showbackground=False, showgrid=False,
                   zeroline=False, showticklabels=False, title=''),
        aspectratio=aspect
    )


def layout_eixos_2d():
    return dict(
        xaxis=dict(range=[0, 10], title="Posição (x)",
                   color=GRUVBOX["fg1"],
                   title_font=dict(color=GRUVBOX["fg1"]),
                   gridcolor="rgba(168,153,132,0.15)",
                   zerolinecolor="rgba(168,153,132,0.35)",
                   linecolor=GRUVBOX["bg2"]),
        yaxis=dict(range=[-5, 105], title="Temperatura (°C)",
                   color=GRUVBOX["fg1"],
                   title_font=dict(color=GRUVBOX["fg1"]),
                   gridcolor="rgba(168,153,132,0.15)",
                   zerolinecolor="rgba(168,153,132,0.35)",
                   linecolor=GRUVBOX["bg2"])
    )


def duracao_frame_ms(tempos):
    n = len(tempos)
    if n < 2:
        return 200
    dt = float(tempos[-1] - tempos[0]) / (n - 1)
    return max(40, int(1000 * dt))


# ============================================================
# FIGURA PDE — VISTA ÚNICA
# ============================================================
def figura_pde_unica(x_vals, tempos, U, modo_animacao, n_voltas,
                     camera_eye, uirevision_str):
    n = len(tempos)
    mov_auto = modo_animacao.startswith("Rotação")
    Xg, Tg = np.meshgrid(x_vals, tempos)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'surface'}, {'type': 'xy'}]],
        column_widths=[0.62, 0.38],
        horizontal_spacing=0.12,
        subplot_titles=("Solução u(x,t) — Superfície espaço-tempo",
                        "Corte transversal em t atual")
    )
    fig.add_trace(go.Surface(
        x=Xg, y=Tg, z=U, surfacecolor=U,
        colorscale=GRUVBOX_THERMAL, cmin=0, cmax=100, showscale=True,
        colorbar=dict(title=dict(text="u (°C)",
                                 font=dict(color=GRUVBOX["fg1"])),
                      x=0.42, len=0.7, thickness=14,
                      tickfont=dict(color=GRUVBOX["fg1"]),
                      outlinecolor=GRUVBOX["bg2"], bgcolor=GRUVBOX["bg0"]),
        contours=dict(z=dict(show=True, usecolormap=False,
                             color="rgba(251,241,199,0.20)", width=1))
    ), row=1, col=1)
    fig.add_trace(go.Scatter3d(
        x=x_vals, y=np.full_like(x_vals, float(tempos[0])), z=U[0],
        mode='lines', line=dict(color=GRUVBOX["red"], width=10)
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x_vals, y=U[0], mode='lines',
        line=dict(color=GRUVBOX["orange"], width=4),
        fill='tozeroy', fillcolor='rgba(254,128,25,0.12)'
    ), row=1, col=2)

    frames = []
    for i, (t, u) in enumerate(zip(tempos, U)):
        p = i / (n - 1) if n > 1 else 0.0
        lf = go.Layout(title=dict(
            text=f"Tempo: {t:.2f} s",
            font=dict(color=GRUVBOX["yellow"], size=18)))
        if mov_auto:
            xe, ye, ze = posicao_camera_auto_pde(p, n_voltas)
            lf.scene = dict(camera=dict(eye=dict(x=xe, y=ye, z=ze)))
        marker = go.Scatter3d(
            x=x_vals, y=np.full_like(x_vals, float(t)), z=u,
            mode='lines', line=dict(color=GRUVBOX["red"], width=10))
        profile = go.Scatter(
            x=x_vals, y=u, mode='lines',
            line=dict(color=GRUVBOX["orange"], width=4),
            fill='tozeroy', fillcolor='rgba(254,128,25,0.12)')
        frames.append(go.Frame(
            name=f"{t:.2f}", data=[marker, profile],
            traces=[1, 2], layout=lf))
    fig.frames = frames

    fig.update_layout(
        height=620, margin=dict(l=20, r=20, b=60, t=100),
        paper_bgcolor=GRUVBOX["bg0_hard"],
        plot_bgcolor=GRUVBOX["bg0_hard"],
        font=dict(color=GRUVBOX["fg1"],
                  family="JetBrains Mono, Fira Code, monospace"),
        title=dict(text=f"Tempo: {tempos[0]:.2f} s",
                   font=dict(color=GRUVBOX["yellow"], size=18)),
        showlegend=False,
        updatemenus=botoes_play_pause(duracao_frame_ms(tempos)),
        scene={**config_eixos_3d("pde"),
               "camera": dict(eye=camera_eye),
               "uirevision": uirevision_str},
        **layout_eixos_2d()
    )
    return fig


# ============================================================
# FIGURA GEOM — VISTA ÚNICA
# ============================================================
def figura_geom_unica(dados, modo_animacao, n_voltas,
                      camera_eye, uirevision_str):
    tempos, x_vals = dados["tempos"], dados["x_vals"]
    X, Y, Z = dados["X"], dados["Y"], dados["Z"]
    nt = dados["n_theta"]
    perfis = dados["perfis"]
    n = len(tempos)
    mov_auto = modo_animacao.startswith("Rotação")

    U0 = np.round(np.tile(perfis[0], (nt, 1)), 1).astype(np.float32)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'surface'}, {'type': 'xy'}]],
        column_widths=[0.62, 0.38],
        horizontal_spacing=0.12,
        subplot_titles=("Simulação 3D Interativa", "Perfil Dinâmico T(x)")
    )
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z, surfacecolor=U0,
        colorscale=GRUVBOX_THERMAL, cmin=0, cmax=100, showscale=True,
        colorbar=dict(title=dict(text="°C",
                                 font=dict(color=GRUVBOX["fg1"])),
                      x=0.42, len=0.7, thickness=14,
                      tickfont=dict(color=GRUVBOX["fg1"]),
                      outlinecolor=GRUVBOX["bg2"], bgcolor=GRUVBOX["bg0"])
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=x_vals, y=perfis[0], mode='lines',
        line=dict(color=GRUVBOX["orange"], width=4),
        fill='tozeroy', fillcolor='rgba(254,128,25,0.12)'
    ), row=1, col=2)

    frames = []
    for i, (t, u) in enumerate(zip(tempos, perfis)):
        p = i / (n - 1) if n > 1 else 0.0
        Uc = np.round(np.tile(u, (nt, 1)), 1).astype(np.float32)
        lf = go.Layout(title=dict(
            text=f"Tempo: {t:.2f} s",
            font=dict(color=GRUVBOX["yellow"], size=18)))
        if mov_auto:
            xe, ye, ze = posicao_camera_auto_geom(p, n_voltas)
            lf.scene = dict(camera=dict(eye=dict(x=xe, y=ye, z=ze)))
        surface = go.Surface(
            x=X, y=Y, z=Z, surfacecolor=Uc,
            colorscale=GRUVBOX_THERMAL, cmin=0, cmax=100, showscale=True,
            colorbar=dict(title=dict(text="°C",
                                     font=dict(color=GRUVBOX["fg1"])),
                          x=0.42, len=0.7, thickness=14,
                          tickfont=dict(color=GRUVBOX["fg1"]),
                          outlinecolor=GRUVBOX["bg2"],
                          bgcolor=GRUVBOX["bg0"]))
        profile = go.Scatter(
            x=x_vals, y=u, mode='lines',
            line=dict(color=GRUVBOX["orange"], width=4),
            fill='tozeroy', fillcolor='rgba(254,128,25,0.12)')
        frames.append(go.Frame(
            name=f"{t:.2f}", data=[surface, profile],
            traces=[0, 1], layout=lf))
    fig.frames = frames

    fig.update_layout(
        height=620, margin=dict(l=20, r=20, b=60, t=100),
        paper_bgcolor=GRUVBOX["bg0_hard"],
        plot_bgcolor=GRUVBOX["bg0_hard"],
        font=dict(color=GRUVBOX["fg1"],
                  family="JetBrains Mono, Fira Code, monospace"),
        title=dict(text=f"Tempo: {tempos[0]:.2f} s",
                   font=dict(color=GRUVBOX["yellow"], size=18)),
        showlegend=False,
        updatemenus=botoes_play_pause(duracao_frame_ms(tempos)),
        scene={**config_eixos_3d("geom"),
               "camera": dict(eye=camera_eye),
               "uirevision": uirevision_str},
        **layout_eixos_2d()
    )
    return fig


# ============================================================
# FIGURA PDE — MOSAICO (leve por natureza)
# ============================================================
def figura_pde_mosaico(x_vals, tempos, U, uirevision_str):
    nomes = list(VISTAS_PDE.keys())
    Xg, Tg = np.meshgrid(x_vals, tempos)

    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{'type': 'scene'}]*3, [{'type': 'scene'}]*3],
        subplot_titles=nomes,
        horizontal_spacing=0.02,
        vertical_spacing=0.06
    )

    # 6 superfícies estáticas (traces 0..5)
    surface_base = go.Surface(
        x=Xg, y=Tg, z=U, surfacecolor=U,
        colorscale=GRUVBOX_THERMAL, cmin=0, cmax=100, showscale=False
    )
    for i in range(6):
        r, c = divmod(i, 3)
        fig.add_trace(surface_base, row=r+1, col=c+1)

    # 6 marcadores (traces 6..11)
    marker_base = go.Scatter3d(
        x=x_vals, y=np.full_like(x_vals, float(tempos[0])), z=U[0],
        mode='lines', line=dict(color=GRUVBOX["red"], width=7),
        showlegend=False
    )
    for i in range(6):
        r, c = divmod(i, 3)
        fig.add_trace(marker_base, row=r+1, col=c+1)

    # Frames: só os marcadores mudam
    frames = []
    for t, u in zip(tempos, U):
        marker = go.Scatter3d(
            x=x_vals, y=np.full_like(x_vals, float(t)), z=u,
            mode='lines', line=dict(color=GRUVBOX["red"], width=7),
            showlegend=False)
        frames.append(go.Frame(
            name=f"{t:.2f}",
            data=[marker] * 6,
            traces=list(range(6, 12)),
            layout=go.Layout(title=dict(
                text=f"Tempo: {t:.2f} s",
                font=dict(color=GRUVBOX["yellow"], size=16)))))
    fig.frames = frames

    scene_cfgs = {}
    for i, nome in enumerate(nomes):
        key = "scene" if i == 0 else f"scene{i+1}"
        scene_cfgs[key] = {**config_eixos_3d("pde"),
                           "camera": dict(eye=VISTAS_PDE[nome])}

    fig.update_layout(
        height=820, margin=dict(l=10, r=10, b=20, t=90),
        paper_bgcolor=GRUVBOX["bg0_hard"],
        plot_bgcolor=GRUVBOX["bg0_hard"],
        font=dict(color=GRUVBOX["fg1"],
                  family="JetBrains Mono, Fira Code, monospace"),
        title=dict(text=f"Mosaico — u(x,t)   |   Tempo: {tempos[0]:.2f} s",
                   font=dict(color=GRUVBOX["orange"], size=17)),
        showlegend=False,
        updatemenus=botoes_play_pause(duracao_frame_ms(tempos), y_pos=1.06),
        uirevision=uirevision_str,
        **scene_cfgs
    )
    return fig


# ============================================================
# FIGURA GEOM — MOSAICO (otimizada)
# ============================================================
def figura_geom_mosaico(dados, uirevision_str):
    tempos, x_vals = dados["tempos"], dados["x_vals"]
    X, Y, Z = dados["X"], dados["Y"], dados["Z"]
    nt = dados["n_theta"]
    perfis = dados["perfis"]
    nomes = list(VISTAS_GEOM.keys())

    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{'type': 'scene'}]*3, [{'type': 'scene'}]*3],
        subplot_titles=nomes,
        horizontal_spacing=0.02,
        vertical_spacing=0.06
    )

    # Cor inicial já arredondada e em float32
    U0 = np.round(np.tile(perfis[0], (nt, 1)), 1).astype(np.float32)

    surface_base = go.Surface(
        x=X, y=Y, z=Z, surfacecolor=U0,
        colorscale=GRUVBOX_THERMAL, cmin=0, cmax=100, showscale=False
    )
    for i in range(6):
        r, c = divmod(i, 3)
        fig.add_trace(surface_base, row=r+1, col=c+1)

    # Frames: 6 superfícies (mesma referência, payload otimizado)
    frames = []
    for t, u in zip(tempos, perfis):
        Uc = np.round(np.tile(u, (nt, 1)), 1).astype(np.float32)
        surface = go.Surface(
            x=X, y=Y, z=Z, surfacecolor=Uc,
            colorscale=GRUVBOX_THERMAL, cmin=0, cmax=100, showscale=False)
        frames.append(go.Frame(
            name=f"{t:.2f}",
            data=[surface] * 6,
            traces=list(range(6)),
            layout=go.Layout(title=dict(
                text=f"Tempo: {t:.2f} s",
                font=dict(color=GRUVBOX["yellow"], size=16)))))
    fig.frames = frames

    scene_cfgs = {}
    for i, nome in enumerate(nomes):
        key = "scene" if i == 0 else f"scene{i+1}"
        scene_cfgs[key] = {**config_eixos_3d("geom"),
                           "camera": dict(eye=VISTAS_GEOM[nome])}

    fig.update_layout(
        height=820, margin=dict(l=10, r=10, b=20, t=90),
        paper_bgcolor=GRUVBOX["bg0_hard"],
        plot_bgcolor=GRUVBOX["bg0_hard"],
        font=dict(color=GRUVBOX["fg1"],
                  family="JetBrains Mono, Fira Code, monospace"),
        title=dict(text=f"Mosaico — geometria física   |   "
                        f"Tempo: {tempos[0]:.2f} s",
                   font=dict(color=GRUVBOX["orange"], size=17)),
        showlegend=False,
        updatemenus=botoes_play_pause(duracao_frame_ms(tempos), y_pos=1.06),
        uirevision=uirevision_str,
        **scene_cfgs
    )
    return fig


# ============================================================
# QUADRO DE VISTAS (vista única)
# ============================================================
auto_rotation = (not modo_mosaico) and modo_animacao.startswith("Rotação")
vistas_disp = VISTAS_PDE if tipo_viz.startswith("Superfície") else VISTAS_GEOM
descs_disp = DESC_PDE if tipo_viz.startswith("Superfície") else DESC_GEOM

# Garante que a view salva é válida para o tipo atual
if st.session_state.view_atual not in vistas_disp:
    st.session_state.view_atual = "Isométrica"

if not modo_mosaico:
    st.markdown(
        '<div class="view-panel"><div class="view-panel-title">'
        'Câmera — Escolha um ponto de vista</div></div>',
        unsafe_allow_html=True)
    cols_vista = st.columns(len(vistas_disp))
    for i, nome in enumerate(vistas_disp.keys()):
        with cols_vista[i]:
            ativo = (st.session_state.view_atual == nome)
            clicado = st.button(
                nome, key=f"btn_view_{nome}", use_container_width=True,
                type="primary" if ativo else "secondary",
                disabled=auto_rotation, help=descs_disp[nome])
            if clicado and not auto_rotation:
                st.session_state.view_atual = nome

    if auto_rotation:
        st.markdown(
            '<div class="view-panel-desc"><b>Aviso:</b> modo '
            '<i>Rotação automática</i> ativo — vistas predefinidas '
            'desabilitadas.</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="view-panel-desc"><b>{st.session_state.view_atual}:</b> '
            f'{descs_disp[st.session_state.view_atual]} '
            '&nbsp;·&nbsp; Você também pode girar com o mouse.</div>',
            unsafe_allow_html=True)

# Câmera efetiva
if auto_rotation:
    if tipo_viz.startswith("Superfície"):
        xe, ye, ze = posicao_camera_auto_pde(0.0, voltas_camera)
    else:
        xe, ye, ze = posicao_camera_auto_geom(0.0, voltas_camera)
    camera_eye = dict(x=xe, y=ye, z=ze)
    uirevision_str = "auto-rotation"
else:
    camera_eye = vistas_disp[st.session_state.view_atual]
    uirevision_str = f"view-{st.session_state.view_atual}"


# ============================================================
# AVISO DE DOWNSCALE
# ============================================================
if modo_mosaico and tipo_viz.startswith("Geometria"):
    st.info(
        f"Modo mosaico da geometria física: resolução reduzida "
        f"(**{res_x} × {res_radial} × {n_frames} frames** — perfil "
        f"**{qualidade}**). Isso evita travamento do navegador. "
        f"Aumente a qualidade na sidebar se sua máquina suportar."
    )


# ============================================================
# RENDER
# ============================================================
if tipo_viz.startswith("Superfície"):
    x_vals, tempos, U = calcular_solucao_2d(
        T_L, T_R, T_init, alpha, N, t_final, n_frames, resolucao=res_x)
    if modo_mosaico:
        fig = figura_pde_mosaico(x_vals, tempos, U,
                                  uirevision_str="mosaico-pde")
        st.caption(
            "**Mosaico 6 vistas — u(x,t).** Isométrica, Frontal (x–u), "
            "Lateral (t–u), Topo (x–t), Traseira e Base. A linha vermelha "
            "é o instante atual. Um único Play anima as 6 cenas.")
    else:
        fig = figura_pde_unica(x_vals, tempos, U, modo_animacao,
                                voltas_camera, camera_eye, uirevision_str)
        st.caption(
            "Posição x (horizontal), tempo t (profundidade), temperatura "
            "u(x,t) (vertical) — a solução completa da EDP parabólica.")
else:
    dados = calcular_frames_geom(T_L, T_R, T_init, alpha, N,
                                  geometria, t_final, n_frames,
                                  res_x, res_radial)
    if modo_mosaico:
        fig = figura_geom_mosaico(dados, uirevision_str="mosaico-geom")
        st.caption(
            f"**Mosaico 6 vistas — {geometria}.** Azul = 0 °C, "
            f"vermelho = 100 °C.")
    else:
        fig = figura_geom_unica(dados, modo_animacao, voltas_camera,
                                 camera_eye, uirevision_str)

st.plotly_chart(fig, use_container_width=True,
                config={"scrollZoom": True, "displaylogo": False},
                key=f"chart_{tipo_viz}_{modo_layout}")

if modo_mosaico:
    st.success(
        "Mosaico ativo. Um único **Play** anima as 6 perspectivas. "
        "Se ainda travar, reduza a **qualidade** na sidebar.")
elif modo_animacao.startswith("Câmera"):
    st.success("Câmera sob seu controle. Pause e arraste sobre o gráfico 3D.")
else:
    st.info("A câmera está sendo movida automaticamente durante o Play.")


# ============================================================
# RODAPÉ
# ============================================================
st.markdown("---")
st.markdown("### Interpretação física dos termos")
st.markdown(
    f"- **<span style='color:{CORES_PARAM['T_L']}'>T_L</span>** e "
    f"**<span style='color:{CORES_PARAM['T_R']}'>T_R</span>** definem o "
    "perfil linear de equilíbrio (estado estacionário).",
    unsafe_allow_html=True)
st.markdown(
    f"- **<span style='color:{CORES_PARAM['T_init']}'>T_init</span>** "
    "determina a amplitude dos modos transientes.",
    unsafe_allow_html=True)
st.markdown(
    f"- **<span style='color:{CORES_PARAM['alpha']}'>α</span>** controla a "
    "taxa de decaimento exponencial de cada harmônico.",
    unsafe_allow_html=True)
st.markdown(
    f"- **<span style='color:{CORES_PARAM['N']}'>N</span>** trunca a série "
    "de Fourier.",
    unsafe_allow_html=True)