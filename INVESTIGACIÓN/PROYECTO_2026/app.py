import re
import unicodedata
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine
 
# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA TERRITORIAL (Mi toque personal, basado en Gabriel García Marquez y la Mariposa Amarilla de Bogotá)
# ==============================================================================
st.set_page_config(
    page_title="TerritorialGov | Bogotá D.C.",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Fondo azul medianoche con matriz de puntos dorados */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #060911 !important;
        background-image: radial-gradient(rgba(234, 179, 8, 0.42) 1.15px, transparent 1.15px) !important;
        background-size: 28px 28px !important;
        color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hacer transparente la barra superior nativa de Streamlit */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Barra lateral oscura con borde dorado sutil */
    [data-testid="stSidebar"] {
        background-color: #080C16 !important;
        border-right: 1px solid rgba(234, 179, 8, 0.28) !important;
    }
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }

    /* Contenedor principal con padding-top de 3.8rem */
    .block-container {
        padding-top: 3.8rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }

    /* Barra institucional superior */
    .top-brand-bar {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-top: 6px;
        padding-bottom: 14px;
        margin-bottom: 24px;
        border-bottom: 1px solid rgba(234, 179, 8, 0.38);
    }
    .brand-butterfly {
        font-size: 1.7rem;
        filter: drop-shadow(0 0 12px rgba(250, 204, 21, 0.85));
    }
    .brand-title {
        font-family: 'Playfair Display', serif;
        color: #FACC15;
        font-size: 1.3rem;
        font-weight: 700;
        line-height: 1.3;
    }
    .brand-subtitle {
        color: #94A3B8;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin-top: 3px;
    }

    /* Tarjeta Hero Principal */
    .hero-card {
        background: #0B101E;
        border: 1px solid rgba(234, 179, 8, 0.45);
        border-radius: 24px;
        padding: 2.8rem 2.6rem;
        text-align: center;
        box-shadow: 0 0 45px rgba(0, 0, 0, 0.9), 0 0 25px rgba(234, 179, 8, 0.08);
        margin-bottom: 2rem;
    }
    .hero-icons {
        font-size: 2.2rem;
        letter-spacing: 10px;
        margin-bottom: 0.8rem;
        filter: drop-shadow(0 0 16px rgba(250, 204, 21, 0.75));
    }
    .hero-serif-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.22;
        margin-bottom: 1rem;
        text-shadow: 0 0 24px rgba(250, 204, 21, 0.35);
    }
    .hero-description {
        font-size: 1.02rem;
        color: #CBD5E1;
        max-width: 860px;
        margin: 0 auto;
        line-height: 1.65;
    }

    /* Pestañas limpias y espaciadas */
    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 10px 18px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FACC15 !important;
        border-bottom-color: #FACC15 !important;
    }

    /* Expander oscuro con borde dorado */
    [data-testid="stExpander"] {
        background-color: #0B101E !important;
        border: 1px solid rgba(234, 179, 8, 0.32) !important;
        border-radius: 16px !important;
        margin-bottom: 1.5rem !important;
    }

    /* Tarjetas KPI */
    .kpi-card {
        background: #0B101E;
        border: 1px solid rgba(234, 179, 8, 0.32);
        border-top: 3px solid #FACC15;
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        margin-bottom: 1.2rem;
    }
    .kpi-title {
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #FACC15;
    }
    .kpi-number {
        font-family: 'Playfair Display', serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 6px 0;
        text-shadow: 0 0 15px rgba(250, 204, 21, 0.25);
    }
    .kpi-sub {
        font-size: 0.82rem;
        color: #94A3B8;
    }

    /* Encabezado explicativo para cada gráfica */
    .chart-header-box {
        background: #0B101E;
        border: 1px solid rgba(234, 179, 8, 0.32);
        border-left: 4px solid #FACC15;
        border-radius: 16px;
        padding: 1.3rem 1.6rem;
        margin-top: 1rem;
        margin-bottom: 0.6rem;
    }
    .chart-header-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #FEF08A;
        margin: 0 0 0.5rem 0;
    }
    .chart-header-guide {
        font-size: 0.9rem;
        color: #CBD5E1;
        line-height: 1.65;
        margin: 0;
    }
    .why-badge {
        display: inline-block;
        background: rgba(250, 204, 21, 0.14);
        border: 1px solid rgba(250, 204, 21, 0.4);
        color: #FEF08A;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 8px;
        margin-top: 8px;
    }

    /* Lienzo de Plotly */
    [data-testid="stPlotlyChart"] {
        background: #0B101E;
        border: 1px solid rgba(234, 179, 8, 0.28);
        border-radius: 18px;
        padding: 0.8rem 1rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.65);
        margin-bottom: 2rem;
    }

    /* Tarjetas de Storytelling (Pestaña 4) */
    .story-card {
        background: #0B101E;
        border: 1px solid rgba(234, 179, 8, 0.38);
        border-radius: 18px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65);
    }
    .story-heading {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #FACC15;
        margin-top: 0;
        margin-bottom: 0.6rem;
    }
    .math-pill {
        background: rgba(250, 204, 21, 0.15);
        border: 1px solid rgba(250, 204, 21, 0.35);
        color: #FEF08A;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.88rem;
    }
    .result-highlight {
        background: rgba(16, 185, 129, 0.12);
        border-left: 3px solid #10B981;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 10px 0;
        color: #E2E8F0;
        font-size: 0.92rem;
    }
    .alert-highlight {
        background: rgba(239, 68, 68, 0.12);
        border-left: 3px solid #EF4444;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 10px 0;
        color: #E2E8F0;
        font-size: 0.92rem;
    }

    /* Tarjeta pedagógica en la barra lateral */
    .sidebar-helper {
        background: rgba(250, 204, 21, 0.08);
        border: 1px solid rgba(250, 204, 21, 0.28);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 16px;
        font-size: 0.83rem;
        line-height: 1.5;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 2. CONEXIÓN A POSTGRESQL, MUESTREO ESTRATÉGICO (<= 100.000) Y LIMPIEZA
# ==============================================================================
@st.cache_resource
def init_connection():
    return create_engine(
        "postgresql://postgres:Angelica.1996@localhost:5432/posgressin10"
    )


engine = init_connection()


def normalizar_texto(texto):
    if pd.isna(texto):
        return ""
    t = str(texto).upper().strip()
    t = "".join(
        c
        for c in unicodedata.normalize("NFD", t)
        if unicodedata.category(c) != "Mn"
    )
    if t in ["NAN", "NONE", "NULL", "NO APLICA", "SIN ESPECIFICAR", "0", "-"]:
        return ""
    t = re.sub(r"\s*-\s*[A-Z0-9\s\.]{1,25}-\s*$", "", t)
    t = re.sub(r"^BOGOTA D\.?C\.?\s*-\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()


def clasificar_frente_bogota(nombre):
    if not nombre or len(nombre) < 3:
        return "OTROS"
    reglas = [
        (
            r"\b(IDU|DESARROLLO URBANO|MOVILIDAD|TRANSMILENIO|VIAS|TRANSPORTE)\b",
            "Movilidad y Vías (IDU)",
        ),
        (r"\b(SALUD|HOSPITAL|SUBRED|CLINICA)\b", "Red de Salud y Hospitales"),
        (r"\b(EDUCACION|COLEGIO|UNIVERSIDAD|SENA)\b", "Educación y Colegios"),
        (
            r"\b(ACUEDUCTO|ALCANTARILLADO|EAAB|AMBIENTE|JARDIN BOTANICO)\b",
            "Acueducto y Ambiente",
        ),
        (
            r"\b(INTEGRACION SOCIAL|BIENESTAR FAMILIAR|ICBF)\b",
            "Integración Social y Niñez",
        ),
        (
            r"\b(HABITAT|VIVIENDA|CAJA DE LA VIVIENDA)\b",
            "Hábitat y Vivienda Popular",
        ),
        (
            r"\b(CULTURA|RECREACION|DEPORTE|IDRD)\b",
            "Cultura, Recreación y Deporte",
        ),
        (
            r"\b(SEGURIDAD|POLICIA|BOMBEROS|JUSTICIA|DEFENSA|EJERCITO)\b",
            "Seguridad y Justicia",
        ),
        (
            r"\b(ALCALDIA|FONDO DE DESARROLLO LOCAL|GOBIERNO)\b",
            "Alcaldías Locales",
        ),
        (r"\b(HACIENDA|CATASTRO|PLANEACION)\b", "Hacienda y Planeación"),
        (r"\b(ENERGIA|MINAS|ELECTRIFICADORA)\b", "Energía y Servicios"),
        (
            r"\b(AGROPECUARIO|AGRICULTURA|BANCO AGRARIO|RURAL)\b",
            "Desarrollo Rural",
        ),
    ]
    for patron, etiqueta in reglas:
        if re.search(patron, nombre):
            return etiqueta
    return "OTROS"


@st.cache_data(ttl=600)
def cargar_datos_muestrales():
    """
    Muestreo Determinístico de Alto Impacto (Máximo 100.000 registros):
    Selecciona los contratos más representativos por monto adjudicado y días de demora
    para maximizar la riqueza analítica del cruce entre SECOP II y BHOEL.
    """
    q_secop_curva = """
        WITH muestra_priorizada AS (
            SELECT 
                entidad,
                duracion,
                valor_adjudicacion,
                GREATEST(0, (fecha_adjudicacion - fecha_publicacion)) AS dias_retraso
            FROM secop_analisis_limpio
            WHERE valor_adjudicacion BETWEEN 1000000 AND 100000000000
              AND duracion BETWEEN 1 AND 1825
              AND entidad IS NOT NULL
            ORDER BY 
                valor_adjudicacion DESC,
                GREATEST(0, (fecha_adjudicacion - fecha_publicacion)) DESC
            LIMIT 100000
        )
        SELECT 
            duracion,
            AVG(valor_adjudicacion) AS costo_promedio,
            COUNT(*) AS cantidad_contratos,
            AVG(dias_retraso) AS dias_retraso_adj
        FROM muestra_priorizada
        GROUP BY duracion
        ORDER BY duracion ASC;
    """
    df_curva = pd.read_sql(q_secop_curva, con=engine)

    q_secop_ent = """
        WITH muestra_priorizada AS (
            SELECT 
                entidad,
                duracion,
                valor_adjudicacion,
                GREATEST(0, (fecha_adjudicacion - fecha_publicacion)) AS dias_retraso
            FROM secop_analisis_limpio
            WHERE valor_adjudicacion BETWEEN 1000000 AND 500000000000
              AND duracion BETWEEN 1 AND 1825
              AND entidad IS NOT NULL
            ORDER BY 
                valor_adjudicacion DESC,
                GREATEST(0, (fecha_adjudicacion - fecha_publicacion)) DESC
            LIMIT 100000
        )
        SELECT 
            entidad,
            COUNT(*) AS total_contratos_secop,
            SUM(valor_adjudicacion) AS inversion_total_secop,
            AVG(valor_adjudicacion) AS costo_promedio_contrato,
            AVG(duracion) AS duracion_promedio_secop,
            AVG(dias_retraso) AS retraso_prom_dias
        FROM muestra_priorizada
        GROUP BY entidad;
    """
    df_sec_ent = pd.read_sql(q_secop_ent, con=engine)

    q_bhoel = """
        SELECT * 
        FROM bhoel_consolidado
        LIMIT 100000;
    """
    df_bh = pd.read_sql(q_bhoel, con=engine)

    return df_curva, df_sec_ent, df_bh


df_curva, df_secop_ent, df_bhoel_raw = cargar_datos_muestrales()

# Limpieza y estandarización de BHOEL
df_bhoel = df_bhoel_raw.copy()
df_bhoel["entidad_limpia"] = (
    df_bhoel["NOMBREENTIDAD"].apply(normalizar_texto)
    if "NOMBREENTIDAD" in df_bhoel.columns
    else ""
)
df_bhoel["sector_limpio"] = (
    df_bhoel["SECTOR"]
    .apply(normalizar_texto)
    .apply(lambda s: re.sub(r"^\d+\s*-\s*", "", s).strip())
    if "SECTOR" in df_bhoel.columns
    else ""
)
df_bhoel = df_bhoel[
    (df_bhoel["entidad_limpia"] != "") & (df_bhoel["sector_limpio"] != "")
].copy()
df_bhoel["frente_institucional"] = df_bhoel["entidad_limpia"].apply(
    clasificar_frente_bogota
)

# Limpieza y estandarización de SECOP II por entidad
df_secop_ent["entidad_limpia"] = df_secop_ent["entidad"].apply(normalizar_texto)
df_secop_ent = df_secop_ent[df_secop_ent["entidad_limpia"] != ""].copy()
df_secop_ent["frente_institucional"] = df_secop_ent["entidad_limpia"].apply(
    clasificar_frente_bogota
)

# ==============================================================================
# 3. ENCABEZADO SUPERIOR Y EXPLICACIÓN INTUITIVA DEL MODELO
# ==============================================================================
st.markdown(
    """
<div class="top-brand-bar">
    <div class="brand-butterfly">🦋</div>
    <div>
        <div class="brand-title">Proyecto Integrador: Cálculo Diferencial, Algoritmos e Introducción a la Analítica de Datos | 2026</div>
        <div class="brand-subtitle">BOGOTÁ D.C. • MUESTRA ESTRATÉGICA DE ALTO IMPACTO (TOP 100.000 REGISTROS)</div>
    </div>
</div>

<div class="hero-card">
    <div class="hero-icons">🦋 ✨ 🦋</div>
    <div class="hero-serif-title">
       Eficiencia del Gasto Público en Bogotá D.C. | Análisis de Riesgos y Sobrecostos en Obras Públicas
    </div>
    <div class="hero-description">
        Modelación matemática continua del presupuesto ejecutado <b><i>C(t)</i></b> y del tiempo de retraso <b><i>R(t)</i></b> sobre una muestra representativa de hasta <b>100.000 registros estratégicos</b> de <b>SECOP II</b> y <b>BHOEL</b>. Traducimos la primera derivada (<b>velocidad del gasto</b>) y la segunda derivada (<b>aceleración del sobrecosto</b>) en un semáforo ciudadano para prevenir obras inconclusas ("elefantes blancos").
    </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander(
    "📘 Guía Rápida para No Matemáticos y Ecuaciones del Modelo Diferencial (Unicafam)",
    expanded=False,
):
    col_eq1, col_eq2 = st.columns(2)
    with col_eq1:
        st.markdown("#### 🚗 Analogía del Automóvil (Sin Fórmulas Complejas)")
        st.markdown(
            "Imagina que un contrato público en Bogotá es como un viaje en carro:\n"
            "* **Posición $C(t)$:** Es el dinero que cuesta el contrato según los días de plazo ($t$).\n"
            "* **Velocidad $C'(t)$ (Primera Derivada):** Es el **velocímetro o taxímetro**. Nos dice cuántos millones de pesos sube el costo por cada día adicional.\n"
            "* **Aceleración $C''(t)$ (Segunda Derivada):** Es el **pedal del acelerador**. Si se pisa a fondo ($C''(t) > 0$), el costo se desborda como una bola de nieve y se enciende nuestra **Alerta Roja**."
        )
        st.latex(r"C'(t) = \frac{dC}{dt} \quad \text{(Velocidad Diaria del Gasto)}")
    with col_eq2:
        st.markdown("#### 📐 Formulación Académica y Criterio Muestral")
        st.markdown(
            "**1. Aceleración del Sobrecosto y Puntos de Inflexión:** Detecta el instante exacto donde cambia la curvatura del presupuesto."
        )
        st.latex(
            r"C''(t) = \frac{d^2C}{dt^2} = \frac{d}{dt}\left(\frac{dC}{dt}\right)"
        )
        st.markdown(
            "**2. Muestreo Estratégico ($N \le 100.000$):** Se seleccionan los registros de mayor materialidad presupuestal y mayor demora en adjudicación para maximizar la precisión del cruce relacional con BHOEL."
        )

# ==============================================================================
# 4. BARRA LATERAL CIUDADANA (SENCILLA Y PEDAGÓGICA)
# ==============================================================================
st.sidebar.markdown("## 🦋 Panel de Exploración")
st.sidebar.markdown(
    """
<div class="sidebar-helper">
    <b>👋 ¡Explora sin ser experto en matemáticas!</b><br>
    Usa estos 3 controles sencillos para elegir el tamaño de los contratos, su duración en el calendario y qué tan estricto quieres que sea el detector de sobrecostos.
</div>
""",
    unsafe_allow_html=True,
)

opcion_presupuesto = st.sidebar.selectbox(
    "💵 Paso 1: ¿Qué tamaño de contratos quieres ver?",
    options=[
        "Pequeños y Estándar (Hasta $500 Millones)",
        "Medianos (Hasta $2.000 Millones)",
        "Grandes Obras (Hasta $10.000 Millones)",
        "Ver Todos los Contratos (Sin límite)",
    ],
    index=1,
    help="Filtra el techo presupuestal en el eje vertical para observar con mayor claridad los contratos de menor o mayor cuantía.",
)
mapa_tope = {
    "Pequeños y Estándar (Hasta $500 Millones)": 500.0,
    "Medianos (Hasta $2.000 Millones)": 2000.0,
    "Grandes Obras (Hasta $10.000 Millones)": 10000.0,
    "Ver Todos los Contratos (Sin límite)": 999999.0,
}
tope_millones = mapa_tope[opcion_presupuesto]

opcion_plazo = st.sidebar.radio(
    "🗓️ Paso 2: ¿Hasta qué duración de obra deseas analizar?",
    options=[
        "Cortos (Hasta 6 meses / 180 días)",
        "De un año (Hasta 1 año / 365 días)",
        "Mediano plazo (Hasta 2 años / 730 días)",
        "Largo plazo (Hasta 5 años / 1.825 días)",
    ],
    index=2,
    help="Equivale a la variable tiempo (t) en el eje horizontal de nuestra función matemática.",
)
mapa_plazo = {
    "Cortos (Hasta 6 meses / 180 días)": 180,
    "De un año (Hasta 1 año / 365 días)": 365,
    "Mediano plazo (Hasta 2 años / 730 días)": 730,
    "Largo plazo (Hasta 5 años / 1.825 días)": 1825,
}
horizon_dias = mapa_plazo[opcion_plazo]

nivel_auditoria = st.sidebar.select_slider(
    "🚨 Paso 3: Rigurosidad del Detector de Alertas:",
    options=[
        "Alta Vigilancia",
        "Equilibrada (Recomendada)",
        "Solo Casos Extremos",
    ],
    value="Equilibrada (Recomendada)",
    help="Define a partir de qué nivel de aceleración del gasto (segunda derivada) un plazo se marca en color Rojo.",
)
mapa_sensibilidad = {
    "Alta Vigilancia": 0.78,
    "Equilibrada (Recomendada)": 0.85,
    "Solo Casos Extremos": 0.92,
}
cuantil_interno = mapa_sensibilidad[nivel_auditoria]

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
**📊 Ficha Técnica de la Muestra:**
* **Tope Muestral:** Máx. 100.000 registros
* **Criterio:** Mayor impacto fiscal y demora

**Investigadores Unicafam:**
* Yeison Steven Castañeda Sánchez
* Daniel Felipe García Guevara

**Asesor:** William Mauricio Hernández  
*Tecnología en Análisis y Gestión de Datos (2026)*
"""
)

# ==============================================================================
# 5. MOTOR DE CÁLCULO DIFERENCIAL Y CONSOLIDACIÓN DE RESULTADOS
# ==============================================================================
df_curva["t_dias"] = df_curva["duracion"].astype(float)
df_curva["C_t_millones"] = df_curva["costo_promedio"].astype(float) / 1e6

# Primera derivada C'(t): Velocidad instantánea del gasto respecto al plazo
df_curva["velocidad_diaria"] = np.gradient(
    df_curva["C_t_millones"], df_curva["t_dias"]
)

# Segunda derivada C''(t): Aceleración o concavidad de la curva de costo
df_curva["aceleracion_costo"] = np.gradient(
    df_curva["velocidad_diaria"], df_curva["t_dias"]
)

umbral_alerta_roja = df_curva["aceleracion_costo"].quantile(cuantil_interno)


def asignar_semaforo(row):
    acel = row["aceleracion_costo"]
    if acel > umbral_alerta_roja:
        return "🔴 Alerta Roja (Aceleración Crítica)"
    elif acel > 0:
        return "🟡 Alerta Naranja (En Aceleración)"
    else:
        return "🟢 Estado Verde (Ritmo Estable)"


df_curva["semaforo"] = df_curva.apply(asignar_semaforo, axis=1)

df_secop_plot = df_curva[
    (df_curva["t_dias"] <= horizon_dias)
    & (df_curva["C_t_millones"] <= tope_millones)
].copy()


def clasificar_etapa_plazo(dias):
    if dias <= 90:
        return "1. Corto Plazo (1 a 90 días)"
    elif dias <= 180:
        return "2. Semestral (91 a 180 días)"
    elif dias <= 365:
        return "3. Anual (181 a 365 días)"
    elif dias <= 730:
        return "4. Bianual (1 a 2 años)"
    else:
        return "5. Plurianual (> 2 años)"


df_curva["etapa_plazo"] = df_curva["t_dias"].apply(clasificar_etapa_plazo)

resumen_etapas = (
    df_curva.groupby("etapa_plazo")
    .agg(
        costo_medio_millones=("C_t_millones", "mean"),
        velocidad_media=("velocidad_diaria", lambda s: np.abs(s).mean()),
        aceleracion_max=("aceleracion_costo", "max"),
        total_plazos=("t_dias", "count"),
        plazos_alerta_roja=(
            "semaforo",
            lambda s: (s == "🔴 Alerta Roja (Aceleración Crítica)").sum(),
        ),
        contratos_totales=("cantidad_contratos", "sum"),
        retraso_medio_etapa=("dias_retraso_adj", "mean"),
    )
    .reset_index()
)
resumen_etapas["pct_alerta_roja"] = (
    resumen_etapas["plazos_alerta_roja"]
    / resumen_etapas["total_plazos"]
    * 100
).round(1)

# Preparación de BHOEL y Cruce Relacional para todas las pestañas
df_bhoel_bogota = df_bhoel[df_bhoel["frente_institucional"] != "OTROS"].copy()
if df_bhoel_bogota.empty:
    df_bhoel_bogota = df_bhoel.copy()

secop_frentes = (
    df_secop_ent[df_secop_ent["frente_institucional"] != "OTROS"]
    .groupby("frente_institucional")
    .agg(
        entidad_ejemplo_secop=("entidad_limpia", "first"),
        contratos_secop=("total_contratos_secop", "sum"),
        inversion_miles_millones=(
            "inversion_total_secop",
            lambda s: s.sum() / 1e9,
        ),
        costo_prom_millones=(
            "costo_promedio_contrato",
            lambda s: s.mean() / 1e6,
        ),
        retraso_medio_dias=("retraso_prom_dias", "mean"),
    )
    .reset_index()
)

bhoel_frentes = (
    df_bhoel_bogota.groupby("frente_institucional")
    .agg(
        entidad_ejemplo_bhoel=("entidad_limpia", "first"),
        obras_bhoel=("entidad_limpia", "count"),
    )
    .reset_index()
)

df_cruce_bogota = pd.merge(
    secop_frentes, bhoel_frentes, on="frente_institucional", how="inner"
)

if not df_cruce_bogota.empty:
    r_bhoel = (
        df_cruce_bogota["obras_bhoel"] / df_cruce_bogota["obras_bhoel"].max()
    )
    r_retraso = (
        df_cruce_bogota["retraso_medio_dias"]
        / df_cruce_bogota["retraso_medio_dias"].replace(0, 1).max()
    )
    df_cruce_bogota["indice_riesgo_100"] = (
        (0.55 * r_bhoel + 0.45 * r_retraso) * 100
    ).round(1)

BG_TRANSPARENT = "rgba(0,0,0,0)"
PLOT_AREA_BG = "rgba(15, 23, 42, 0.45)"
GRID_GOLD = "rgba(234, 179, 8, 0.12)"

# ==============================================================================
# 6. NAVEGACIÓN POR PESTAÑAS (1 GRÁFICA EN TABS 1-3 | 0 GRÁFICAS EN TAB 4)
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🚦 1. Modelo Diferencial SECOP II",
    "🏗️ 2. Memoria Histórica BHOEL",
    "🔗 3. Cruce Relacional (SECOP vs. BHOEL)",
    "🦋 4. Storytelling de Resultados (Sin Gráficas)",
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: 1 SOLA GRÁFICA — DISPERSIÓN DIFERENCIAL C(t), C'(t) Y C''(t)
# ------------------------------------------------------------------------------
with tab1:
    total_contratos_eval = int(df_curva["cantidad_contratos"].sum())
    total_rojas = len(
        df_curva[df_curva["semaforo"] == "🔴 Alerta Roja (Aceleración Crítica)"]
    )
    cambios_tendencia = int(
        np.sum(np.diff(np.sign(df_curva["aceleracion_costo"])) != 0)
    )

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">Muestra Depurada en'
            f' Bogotá D.C.</div><div class="kpi-number">{total_contratos_eval:,}'
            '</div><div class="kpi-sub">Top registros de mayor impacto (Máx.'
            " 100.000)</div></div>",
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#EF4444;"><div'
            ' class="kpi-title">Plazos en Alerta Roja (C\'\'(t) Crítica)</div><div'
            f' class="kpi-number">{total_rojas}</div><div class="kpi-sub">Duraciones'
            " donde el sobrecosto se acelera bruscamente</div></div>",
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#10B981;"><div'
            ' class="kpi-title">Puntos de Inflexión (C\'\'(t) = 0)</div><div'
            f' class="kpi-number">{cambios_tendencia}</div><div'
            ' class="kpi-sub">Cambios de concavidad en la curva de gasto'
            " público</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class="chart-header-box">
        <div class="chart-header-title">Gráfica Maestra 1 — Función de Costo C(t) y Semáforo de Segunda Derivada C''(t) en Bogotá D.C.</div>
        <p class="chart-header-guide">
        • <b>¿Cómo leerla fácilmente?:</b> Cada punto representa una duración de contrato en días (<b>Eje X</b>) y cuánto cuesta en promedio en millones de pesos (<b>Eje Y</b>).<br>
        • <b>Significado del color (Cálculo Diferencial):</b>
        <span style="color:#34D399; font-weight:700;">🟢 Verde (C''(t) ≤ 0):</span> El gasto crece a ritmo controlado |
        <span style="color:#FACC15; font-weight:700;">🟡 Naranja (C''(t) > 0):</span> El costo empieza a acelerarse |
        <span style="color:#F87171; font-weight:700;">🔴 Rojo (Umbral Crítico):</span> Aceleración desbordada del presupuesto.<br>
        <span class="why-badge">🎓 Enfoque de Cálculo Diferencial: Pasa el cursor sobre cualquier punto para ver simultáneamente el valor de la función C(t), su primera derivada C'(t) (velocidad diaria) y su segunda derivada C''(t) (aceleración).</span>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    fig1 = px.scatter(
        df_secop_plot,
        x="t_dias",
        y="C_t_millones",
        color="semaforo",
        color_discrete_map={
            "🔴 Alerta Roja (Aceleración Crítica)": "#EF4444",
            "🟡 Alerta Naranja (En Aceleración)": "#FACC15",
            "🟢 Estado Verde (Ritmo Estable)": "#10B981",
        },
        custom_data=[
            "t_dias",
            "C_t_millones",
            "cantidad_contratos",
            "velocidad_diaria",
            "aceleracion_costo",
            "semaforo",
        ],
    )
    fig1.update_traces(
        marker=dict(
            size=9, opacity=0.88, line=dict(width=0.6, color="#060911")
        ),
        hovertemplate=(
            "<b>📍 Análisis Diferencial del Plazo (Bogotá D.C.)</b><br>"
            "• <b>Tiempo t (Plazo):</b> %{customdata[0]:.0f} días<br>"
            "• <b>Función C(t) (Costo Promedio):</b> $%{customdata[1]:,.1f} Millones COP<br>"
            "• <b>Contratos en este punto:</b> %{customdata[2]:,}<br>"
            "• <b>1ra Derivada C'(t) (Velocidad):</b> $%{customdata[3]:,.2f} Millones/día<br>"
            "• <b>2da Derivada C''(t) (Aceleración):</b> $%{customdata[4]:,.2f} Millones/día²<br>"
            "• <b>Diagnóstico:</b> %{customdata[5]}<extra></extra>"
        ),
    )
    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=PLOT_AREA_BG,
        height=500,
        font=dict(family="Plus Jakarta Sans", size=13, color="#F8FAFC"),
        xaxis=dict(
            title="<b>Variable Independiente t: Duración Pactada del Contrato [Días]</b>",
            ticksuffix=" días",
            showgrid=True,
            gridcolor=GRID_GOLD,
            automargin=True,
        ),
        yaxis=dict(
            title="<b>Función Dependiente C(t): Costo Promedio [Millones COP]</b>",
            tickprefix="$",
            ticksuffix=" M",
            showgrid=True,
            gridcolor=GRID_GOLD,
            automargin=True,
        ),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=80, r=40, t=55, b=65),
    )
    st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 2: 1 SOLA GRÁFICA — CONCENTRACIÓN BHOEL CON PALETA MULTICROMÁTICA
# ------------------------------------------------------------------------------
with tab2:
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">Obras Históricas en'
            f' BHOEL</div><div class="kpi-number">{len(df_bhoel_bogota):,}</div>'
            '<div class="kpi-sub">Muestra depurada de la Contraloría</div></div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#10B981;"><div'
            ' class="kpi-title">Entidades Ejecutoras Únicas</div><div'
            f' class="kpi-number">{df_bhoel_bogota["entidad_limpia"].nunique():,}'
            '</div><div class="kpi-sub">Instituciones con antecedentes'
            " registrados</div></div>",
            unsafe_allow_html=True,
        )
    with b3:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#EF4444;"><div'
            ' class="kpi-title">Frentes Urbanos de Bogotá</div><div'
            f' class="kpi-number">{df_bhoel_bogota["frente_institucional"].nunique()}'
            '</div><div class="kpi-sub">Sectores estratégicos'
            " capitalinos</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class="chart-header-box">
        <div class="chart-header-title">Gráfica Maestra 2 — Distribución Multicromática de Obras Inconclusas (BHOEL) por Frente Urbano de Bogotá D.C.</div>
        <p class="chart-header-guide">
        • <b>¿Cómo leerla fácilmente?:</b> Cada barra tiene un color distintivo que identifica a un gran sector de inversión de Bogotá (Salud, Educación, Movilidad, Alcaldías Locales, etc.) y muestra cuántas obras con problemas históricos acumula en la Contraloría.<br>
        • <b>Preparación para el Cruce:</b> Estos sectores estandarizados son la "llave maestra" que une los antecedentes de la Contraloría (BHOEL) con la contratación actual (SECOP II).<br>
        <span class="why-badge">🎓 Enfoque Académico: Representa las condiciones iniciales de vulnerabilidad estructural de cada sector antes de cruzarlos con las tasas de retraso actuales.</span>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    frentes_bhoel = (
        df_bhoel_bogota.groupby("frente_institucional")
        .agg(
            Total_Obras=("entidad_limpia", "count"),
            Entidades_Involucradas=("entidad_limpia", "nunique"),
        )
        .reset_index()
        .nlargest(8, "Total_Obras")
        .sort_values(by="Total_Obras", ascending=True)
    )
    frentes_bhoel["Porcentaje"] = (
        frentes_bhoel["Total_Obras"] / frentes_bhoel["Total_Obras"].sum() * 100
    ).round(1)
    max_b2 = frentes_bhoel["Total_Obras"].max() * 1.32

    # Paleta de colores vibrantes y diferenciados para cada Frente Urbano
    paleta_frentes_bhoel = [
        "#6366F1",  # Índigo Profundo
        "#EC4899",  # Rosa Magenta
        "#A855F7",  # Púrpura Real
        "#F97316",  # Coral Naranja
        "#10B981",  # Verde Esmeralda
        "#38BDF8",  # Azul Cielo
        "#14B8A6",  # Turquesa Cian
        "#06B6D4",  # Cian Brillante (Top 1)
    ][: len(frentes_bhoel)]

    fig_b2 = go.Figure(
        go.Bar(
            x=frentes_bhoel["Total_Obras"],
            y=frentes_bhoel["frente_institucional"],
            orientation="h",
            text=frentes_bhoel.apply(
                lambda r: f"{r['Total_Obras']:,} obras ({r['Porcentaje']}%)",
                axis=1,
            ),
            textposition="outside",
            textfont=dict(color="#F8FAFC", size=13),
            marker=dict(
                color=paleta_frentes_bhoel,
                line=dict(color="#FFFFFF", width=1.2),
            ),
            customdata=np.stack(
                [
                    frentes_bhoel["frente_institucional"],
                    frentes_bhoel["Entidades_Involucradas"],
                    frentes_bhoel["Porcentaje"],
                ],
                axis=-1,
            ),
            hovertemplate=(
                "<b>🏗️ %{customdata[0]}</b><br>"
                "• <b>Obras reportadas en BHOEL:</b> %{x:,}<br>"
                "• <b>Peso porcentual en Bogotá:</b> %{customdata[2]}%<br>"
                "• <b>Entidades ejecutoras involucradas:</b> %{customdata[1]}<extra></extra>"
            ),
        )
    )
    fig_b2.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=PLOT_AREA_BG,
        height=490,
        bargap=0.36,
        font=dict(family="Plus Jakarta Sans", size=13, color="#F8FAFC"),
        yaxis=dict(
            title="<b>Frente Institucional en Bogotá D.C.</b>", automargin=True
        ),
        xaxis=dict(
            title="<b>Cantidad de Obras Registradas en BHOEL y Participación (%)</b>",
            range=[0, max_b2],
            showgrid=True,
            gridcolor=GRID_GOLD,
            automargin=True,
        ),
        margin=dict(l=240, r=90, t=35, b=60),
    )
    st.plotly_chart(fig_b2, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 3: 1 SOLA GRÁFICA — MATRIZ DE 4 CUADRANTES (CRUCE SECOP II + BHOEL)
# ------------------------------------------------------------------------------
with tab3:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">Sectores Cruzados'
            f' Exitosamente</div><div class="kpi-number">{len(df_cruce_bogota)}'
            '</div><div class="kpi-sub">Frentes presentes en SECOP II y'
            " BHOEL</div></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#10B981;"><div'
            ' class="kpi-title">Contratos SECOP II Cruzados</div><div'
            f' class="kpi-number">{int(df_cruce_bogota["contratos_secop"].sum()):,}'
            '</div><div class="kpi-sub">Muestra estratégica vinculada al'
            " cruce</div></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#EF4444;"><div'
            ' class="kpi-title">Obras BHOEL Cruzadas</div><div'
            f' class="kpi-number">{int(df_cruce_bogota["obras_bhoel"].sum()):,}'
            '</div><div class="kpi-sub">Antecedentes físicos en los mismos'
            " sectores</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class="chart-header-box">
        <div class="chart-header-title">Gráfica Maestra 3 — Plano Cartesiano de Vulnerabilidad: Antecedentes BHOEL (X) vs. Tasa de Demora SECOP II (Y)</div>
        <p class="chart-header-guide">
        • <b>¿Cómo leerla fácilmente?:</b> Hemos dividido el mapa en 4 zonas mediante líneas punteadas. Las burbujas que caen arriba a la derecha (<b>Cuadrante Crítico</b>) son los sectores que tienen al mismo tiempo más obras inconclusas en el pasado (<b>Eje X</b>) y mayores demoras de adjudicación hoy en día (<b>Eje Y</b>).<br>
        • <b>Tamaño de la burbuja:</b> Representa el volumen de contratos analizados en ese sector.<br>
        <span class="why-badge">🎓 Enfoque de Cálculo y Analítica: Integra la razón de cambio temporal del retraso R'(t) con el historial físico de la Contraloría para priorizar auditorías preventivas en Bogotá D.C.</span>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    med_x = df_cruce_bogota["obras_bhoel"].median()
    med_y = df_cruce_bogota["retraso_medio_dias"].median()
    max_cx = df_cruce_bogota["obras_bhoel"].max() * 1.18
    max_cy = df_cruce_bogota["retraso_medio_dias"].max() * 1.22
    min_cy = max(0, df_cruce_bogota["retraso_medio_dias"].min() * 0.8)

    fig_c1 = px.scatter(
        df_cruce_bogota,
        x="obras_bhoel",
        y="retraso_medio_dias",
        size="contratos_secop",
        color="frente_institucional",
        color_discrete_sequence=[
            "#FACC15",
            "#38BDF8",
            "#EF4444",
            "#10B981",
            "#F97316",
            "#A855F7",
            "#EC4899",
            "#14B8A6",
            "#EAB308",
            "#6366F1",
        ],
        size_max=48,
        custom_data=[
            "frente_institucional",
            "obras_bhoel",
            "retraso_medio_dias",
            "contratos_secop",
            "costo_prom_millones",
            "indice_riesgo_100",
        ],
    )
    fig_c1.update_traces(
        marker=dict(opacity=0.9, line=dict(width=2, color="#FFFFFF")),
        hovertemplate=(
            "<b>🔗 %{customdata[0]}</b><br>"
            "• <b>Obras Históricas (BHOEL):</b> %{customdata[1]:,} obras<br>"
            "• <b>Demora Media Precontractual (SECOP II):</b> %{customdata[2]:.1f} días<br>"
            "• <b>Contratos en la Muestra:</b> %{customdata[3]:,}<br>"
            "• <b>Costo Promedio por Contrato:</b> $%{customdata[4]:,.1f} Millones COP<br>"
            "• <b>Índice Combinado de Vulnerabilidad:</b> %{customdata[5]:.1f} / 100 pts<extra></extra>"
        ),
    )
    fig_c1.add_vline(
        x=med_x,
        line_dash="dash",
        line_color="rgba(250, 204, 21, 0.55)",
        annotation_text="Mediana Histórica BHOEL",
        annotation_position="top",
    )
    fig_c1.add_hline(
        y=med_y,
        line_dash="dash",
        line_color="rgba(250, 204, 21, 0.55)",
        annotation_text="Mediana de Demora (Días)",
        annotation_position="right",
    )
    fig_c1.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=PLOT_AREA_BG,
        height=510,
        font=dict(family="Plus Jakarta Sans", size=13, color="#F8FAFC"),
        xaxis=dict(
            title="<b>Eje X: Antecedentes de Obras en BHOEL (Contraloría General)</b>",
            range=[-max_cx * 0.05, max_cx],
            showgrid=True,
            gridcolor=GRID_GOLD,
            automargin=True,
        ),
        yaxis=dict(
            title="<b>Eje Y: Demora Promedio de Adjudicación en SECOP II [Días]</b>",
            ticksuffix=" días",
            range=[min_cy, max_cy],
            showgrid=True,
            gridcolor=GRID_GOLD,
            automargin=True,
        ),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=80, r=60, t=70, b=65),
    )
    st.plotly_chart(fig_c1, use_container_width=True)

# ------------------------------------------------------------------------------
# PESTAÑA 4: STORYTELLING PROFUNDO Y EXPLÍCITO (CERO GRÁFICAS, 100% RESULTADOS)
# ------------------------------------------------------------------------------
with tab4:
    # Extracción explícita de todos los números obtenidos para contar la historia
    etapa_corto = resumen_etapas.iloc[0]
    etapa_largo = resumen_etapas.iloc[-1]
    etapa_mas_riesgosa = resumen_etapas.sort_values(
        by="pct_alerta_roja", ascending=False
    ).iloc[0]

    multiplicador_costo = round(
        etapa_largo["costo_medio_millones"]
        / max(etapa_corto["costo_medio_millones"], 1),
        1,
    )
    velocidad_media_global = round(
        np.abs(df_curva["velocidad_diaria"]).mean(), 2
    )
    velocidad_max_global = round(df_curva["velocidad_diaria"].max(), 2)
    retraso_global_dias = round(df_curva["dias_retraso_adj"].mean(), 1)

    total_plazos_evaluados = len(df_curva)
    total_verdes = int(
        (df_curva["semaforo"] == "🟢 Estado Verde (Ritmo Estable)").sum()
    )
    total_naranjas = int(
        (df_curva["semaforo"] == "🟡 Alerta Naranja (En Aceleración)").sum()
    )
    pct_rojas_global = round(
        (total_rojas / max(total_plazos_evaluados, 1)) * 100, 1
    )

    # Ranking completo del cruce SECOP II + BHOEL
    cruce_ranking = df_cruce_bogota.sort_values(
        by="indice_riesgo_100", ascending=False
    ).reset_index(drop=True)
    top1_frente = cruce_ranking.iloc[0]
    top2_frente = (
        cruce_ranking.iloc[1] if len(cruce_ranking) > 1 else top1_frente
    )
    top3_frente = (
        cruce_ranking.iloc[2] if len(cruce_ranking) > 2 else top2_frente
    )
    frente_mas_estable = cruce_ranking.iloc[-1]

    inversion_total_cruzada_billones = round(
        df_cruce_bogota["inversion_miles_millones"].sum() / 1000, 2
    )
    inversion_total_miles_mill = round(
        df_cruce_bogota["inversion_miles_millones"].sum(), 1
    )

    # Encabezado Literario y Ciudadano
    st.markdown(
        f"""
    <div class="story-card">
        <div class="story-heading">🦋 Crónica de un Sobrecosto Anunciado: Lo que Dicen las Cifras Reales de Bogotá D.C.</div>
        <p style="font-size:0.97rem; line-height:1.78; color:#CBD5E1; margin-bottom:0;">
        En <i>Cien años de soledad</i>, las mariposas amarillas anunciaban la llegada de Mauricio Babilonia antes de que nadie pudiera verlo. En las obras públicas de <b>Bogotá D.C.</b> ocurre exactamente lo mismo: un hospital, un colegio o una avenida nunca se convierte en un "elefante blanco" de la noche a la mañana. Tras analizar una muestra de alto impacto de <b>{total_contratos_eval:,} contratos de SECOP II</b> (que representan <b>${inversion_total_miles_mill:,.1f} miles de millones de pesos</b> en inversión) y cruzarlos con <b>{len(df_bhoel_bogota):,} obras históricas de la Contraloría (BHOEL)</b>, tradujimos las ecuaciones del cálculo diferencial a lenguaje ciudadano para mostrar con cifras exactas dónde y cuándo se desborda el dinero público.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # 4 KPIs Resumen de Hallazgos Numéricos
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">Aumento por Plazo'
            f' Largo</div><div class="kpi-number">{multiplicador_costo}x'
            '</div><div class="kpi-sub">Veces más caro un proyecto plurianual'
            " vs. uno corto</div></div>",
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#38BDF8;"><div'
            ' class="kpi-title">El "Taxímetro" Diario</div><div'
            f' class="kpi-number">${velocidad_media_global:,.1f} M</div><div'
            ' class="kpi-sub">Velocidad media de cambio por día de plazo'
            " (1ra Derivada)</div></div>",
            unsafe_allow_html=True,
        )
    with r3:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#EF4444;"><div'
            ' class="kpi-title">Etapa de Mayor Riesgo</div><div'
            f' class="kpi-number">{etapa_mas_riesgosa["pct_alerta_roja"]}%'
            '</div><div class="kpi-sub">De plazos en Alerta Roja en'
            f' {etapa_mas_riesgosa["etapa_plazo"]}</div></div>',
            unsafe_allow_html=True,
        )
    with r4:
        st.markdown(
            '<div class="kpi-card" style="border-top-color:#10B981;"><div'
            ' class="kpi-title">Sector #1 más Crítico</div><div'
            f' class="kpi-number">{top1_frente["indice_riesgo_100"]} pts</div>'
            f'<div class="kpi-sub">{top1_frente["frente_institucional"]}'
            " (Escala 0 a 100)</div></div>",
            unsafe_allow_html=True,
        )

    # Bloque de los 4 Actos con Resultados Explícitos
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown(
            f"""
        <div class="story-card">
            <div class="story-heading" style="font-size:1.25rem;">Acto I — El Efecto del Tiempo en el Bolsillo Público (La Función del Costo)</div>
            <p style="font-size:0.93rem; line-height:1.72; color:#CBD5E1;">
            Para una persona que no usa matemáticas, una <b>función</b> es simplemente una relación: <i>"dime cuántos días dura una obra y te diré cuánto nos cuesta"</i>. Al medir nuestros <b>{total_contratos_eval:,} contratos</b>, descubrimos que el tiempo multiplica el gasto de forma dramática:
            </p>
            <div class="result-highlight">
                • <b>En contratos cortos ({etapa_corto['etapa_plazo']}):</b> El costo promedio es de <b>${etapa_corto['costo_medio_millones']:,.1f} Millones COP</b> (sobre {int(etapa_corto['contratos_totales']):,} contratos) y tardan en promedio <b>{etapa_corto['retraso_medio_etapa']:.1f} días</b> en adjudicarse.<br>
                • <b>En megaproyectos largos ({etapa_largo['etapa_plazo']}):</b> El costo promedio salta a <b>${etapa_largo['costo_medio_millones']:,.1f} Millones COP</b> (sobre {int(etapa_largo['contratos_totales']):,} contratos), es decir, son <b>{multiplicador_costo} veces más costosos</b> y su demora previa sube a <b>{etapa_largo['retraso_medio_etapa']:.1f} días</b>.
            </div>
            <div class="story-heading" style="font-size:1.25rem; margin-top:1.4rem;">Acto II — El "Taxímetro" y la "Bola de Nieve" (1ra y 2da Derivada sin Fórmulas)</div>
            <p style="font-size:0.93rem; line-height:1.72; color:#CBD5E1;">
            En Cálculo Diferencial hablamos de <b>Primera y Segunda Derivada</b>, pero en la vida real funcionan como un taxi:<br>
            • <b>El Taxímetro (<span class="math-pill">1ra Derivada = Velocidad</span>):</b> Nos indica que, en promedio, cada día adicional de plazo mueve el presupuesto a una velocidad de <b>${velocidad_media_global:,.2f} Millones de pesos por día</b>, llegando a picos máximos de <b>${velocidad_max_global:,.1f} Millones/día</b> en plazos de alta volatilidad.<br>
            • <b>El Efecto Bola de Nieve (<span class="math-pill">2da Derivada = Aceleración</span>):</b> Nos avisa cuándo el taxímetro se descontrola. De los <b>{total_plazos_evaluados} plazos distintos</b> evaluados en el calendario, <b>{total_verdes} plazos</b> mantienen un ritmo estable (🟢 Verde), <b>{total_naranjas} plazos</b> están empezando a encarecerse (🟡 Naranja) y <b>{total_rojas} plazos ({pct_rojas_global}%)</b> están en <b>🔴 Alerta Roja</b> porque el costo se acelera peligrosamente. Además, el presupuesto cambia bruscamente de dirección <b>{cambios_tendencia} veces</b> (puntos de inflexión).
            </p>
            <div class="alert-highlight">
                🚨 <b>Dato clave para auditores:</b> La etapa más peligrosa de toda la contratación en Bogotá es <b>{etapa_mas_riesgosa['etapa_plazo']}</b>, donde el <b>{etapa_mas_riesgosa['pct_alerta_roja']}%</b> de los plazos enciende la Alerta Roja con un valor promedio de <b>${etapa_mas_riesgosa['costo_medio_millones']:,.1f} Millones COP</b> por contrato.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with s_col2:
        st.markdown(
            f"""
        <div class="story-card">
            <div class="story-heading" style="font-size:1.25rem;">Acto III — Los Nombres Propios del Riesgo (Resultados del Cruce SECOP II + BHOEL)</div>
            <p style="font-size:0.93rem; line-height:1.72; color:#CBD5E1;">
            ¿Las demoras actuales ocurren por mala suerte o se repiten en los mismos sectores que ya dejaron obras inconclusas en el pasado? Al cruzar los <b>{int(df_cruce_bogota['contratos_secop'].sum()):,} contratos activos de SECOP II</b> con las <b>{int(df_cruce_bogota['obras_bhoel'].sum()):,} obras reportadas en la Contraloría (BHOEL)</b> dentro de los <b>{len(df_cruce_bogota)} frentes urbanos de Bogotá</b>, obtuvimos el <b>Top 3 de Sectores Más Vulnerables</b>:
            </p>
            <div class="alert-highlight">
                🥇 <b>1. {top1_frente['frente_institucional']} ({top1_frente['indice_riesgo_100']} / 100 pts):</b> Acumula <b>{int(top1_frente['obras_bhoel']):,} obras históricas en BHOEL</b>, registra una demora media actual de <b>{top1_frente['retraso_medio_dias']:.1f} días</b> en sus <b>{int(top1_frente['contratos_secop']):,} contratos de SECOP II</b> y maneja un costo promedio de <b>${top1_frente['costo_prom_millones']:,.1f} Millones COP</b>.<br><br>
                🥈 <b>2. {top2_frente['frente_institucional']} ({top2_frente['indice_riesgo_100']} / 100 pts):</b> Registra <b>{int(top2_frente['obras_bhoel']):,} antecedentes en BHOEL</b>, <b>{top2_frente['retraso_medio_dias']:.1f} días</b> de retraso promedio y <b>{int(top2_frente['contratos_secop']):,} contratos analizados</b> (costo medio de <b>${top2_frente['costo_prom_millones']:,.1f} Millones COP</b>).<br><br>
                🥉 <b>3. {top3_frente['frente_institucional']} ({top3_frente['indice_riesgo_100']} / 100 pts):</b> Presenta <b>{int(top3_frente['obras_bhoel']):,} reportes en Contraloría</b>, una demora promedio de <b>{top3_frente['retraso_medio_dias']:.1f} días</b> sobre <b>{int(top3_frente['contratos_secop']):,} contratos</b> y un valor medio de <b>${top3_frente['costo_prom_millones']:,.1f} Millones COP</b>.
            </div>
            <div class="result-highlight">
                ✅ <b>El Contraste Positivo (Sector Más Estable):</b> En el otro extremo, el frente de <b>{frente_mas_estable['frente_institucional']}</b> presenta el menor índice de vulnerabilidad con <b>{frente_mas_estable['indice_riesgo_100']} / 100 puntos</b>, con solo <b>{int(frente_mas_estable['obras_bhoel']):,} registros en BHOEL</b> y una demora promedio de <b>{frente_mas_estable['retraso_medio_dias']:.1f} días</b>.
            </div>
            <div class="story-heading" style="font-size:1.25rem; margin-top:1.3rem;">Acto IV — Conclusión Práctica para Bogotá D.C.</div>
            <p style="font-size:0.93rem; line-height:1.72; color:#CBD5E1; margin-bottom:0;">
            La enseñanza de este proyecto integrador es contundente: <b>la matemática sirve para cuidar los impuestos de la gente</b>. Si un contrato supera el umbral de <b>{etapa_mas_riesgosa['etapa_plazo']}</b> y pertenece a sectores como <b>{top1_frente['frente_institucional']}</b> o <b>{top2_frente['frente_institucional']}</b>, no hay que esperar años para saber que está en peligro; basta con mirar nuestro semáforo de aceleración y activar una auditoría preventiva desde el primer mes.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Ficha Metodológica y de Fuentes en la parte inferior
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            f"""
        <div class="story-card">
            <div class="story-heading" style="font-size:1.1rem;">1. Muestra SECOP II ({total_contratos_eval:,} registros)</div>
            <p style="font-size:0.86rem; color:#CBD5E1; line-height:1.6; margin-bottom:0;">
            • <b>Entidad Oficial:</b> Agencia Nacional de Contratación Pública — Colombia Compra Eficiente.<br>
            • <b>Estrategia Muestral:</b> Selección de hasta 100.000 contratos priorizados por impacto presupuestal y días de demora en Bogotá D.C. (DANE 11001).<br>
            • <b>Demora Global Media:</b> {retraso_global_dias} días entre publicación y adjudicación.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            f"""
        <div class="story-card">
            <div class="story-heading" style="font-size:1.1rem;">2. Fuente BHOEL ({len(df_bhoel_bogota):,} obras)</div>
            <p style="font-size:0.86rem; color:#CBD5E1; line-height:1.6; margin-bottom:0;">
            • <b>Entidad Oficial:</b> Contraloría General de la República (Sistema SIRECI).<br>
            • <b>Consolidación:</b> Banco de Herramientas de Obras Inconclusas depurado para los {len(df_cruce_bogota)} frentes estratégicos de Bogotá D.C.<br>
            • <b>Entidades Auditadas:</b> {df_bhoel_bogota['entidad_limpia'].nunique():,} instituciones públicas.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            """
        <div class="story-card">
            <div class="story-heading" style="font-size:1.1rem;">3. Arquitectura Académica (Unicafam)</div>
            <p style="font-size:0.86rem; color:#CBD5E1; line-height:1.6; margin-bottom:0;">
            • <b>Base de Datos:</b> PostgreSQL (<code>posgressin10</code>) con muestreo determinístico por CTE.<br>
            • <b>Motor de Cálculo:</b> Diferenciación numérica de 1er y 2do orden (<code>np.gradient</code>) en Python.<br>
            • <b>Visualización:</b> 3 gráficas maestras interactivas (Tabs 1 a 3) y 1 informe ejecutivo de storytelling cuantitativo (Tab 4).
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )