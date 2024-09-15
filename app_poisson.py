import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from scipy.stats import poisson


def calcular_probs():
    ataque_local = local_favor / locales_f
    defensa_visitante = visitante_contra / locales_f
    fuerza_local = ataque_local * defensa_visitante * locales_f
    
    ataque_visitante = visitante_favor / visitantes_f
    defensa_local = local_contra / visitantes_f
    fuerza_visitante = ataque_visitante * defensa_local * visitantes_f
    
    col1, _, col3 = st.columns(3)
    col1.metric("Fuerza LOCAL", round(fuerza_local, 3))
    col3.metric("Fuerza VISITANTE", round(fuerza_visitante, 3))

    st.subheader("", divider="orange")
    
    lambda_local = fuerza_local
    goles_local = [poisson.pmf(k, fuerza_local) for k in range(11)]
    
    lambda_visitante = fuerza_visitante
    goles_visitante = [poisson.pmf(k, fuerza_visitante) for k in range(11)]


    col1, _, col3 = st.columns(3)
    st.subheader("", divider="orange")

    col1.write("LOCAL MARCA...")
    for n, l in enumerate(goles_local[:6]):
        col1.write(f"{n} goles: {l:.1%}")
    
    col3.write("VISITANTE MARCA...")
    for n, v in enumerate(goles_visitante[:6]):
        col3.write(f"{n} goles: {v:.1%}")


    victoria_local, empate, victoria_visitante, probs = [], [], [], []
    
    for n1, gl in enumerate(goles_local):
        for n2, gv in enumerate(goles_visitante):
    
            prob_conjunta = gl * gv
            probs.append(prob_conjunta)
            
            if n1 > n2:
                victoria_local.append(prob_conjunta)
    
            elif n1 < n2:
                victoria_visitante.append(prob_conjunta)
    
            else:
                empate.append(prob_conjunta)
    
    victoria_local = sum(victoria_local)
    empate = sum(empate)
    victoria_visitante = sum(victoria_visitante)
    
    col1, col2, col3 = st.columns(3)
    
    vl_formateado = f"{victoria_local:.1%}"
    em_formateado = f"{empate:.1%}"
    vv_formateado = f"{victoria_visitante:.1%}"
    
    col1.metric("LOCAL", vl_formateado)
    col2.metric("EMPATE", em_formateado)
    col3.metric("VISITANTE", vv_formateado)

    st.subheader("", divider="orange")
    
    
    array = np.array(probs).reshape(11, 11)
    df = pd.DataFrame(array, index=[f"{goles}" for goles in range(0, 11)], columns=[f"{goles}" for goles in range(0, 11)])
    df_formateado = df.map(lambda x: f"{100*x:.1f}%")
    
    plt.figure(figsize=(10, 8))
    heatmap = sns.heatmap(df, annot=df.map(lambda x: f"{100*x:.1f}%"), fmt="", cmap="Reds", cbar=False)
    plt.title("Probabilidad de cada resultado en porcentaje", pad=15)
    plt.xlabel("Visitante", labelpad=10)
    plt.ylabel("Local")
    heatmap.xaxis.tick_top()
    heatmap.xaxis.set_label_position('top')
    st.pyplot(plt)
    
    st.subheader("", divider="orange")

    st.dataframe(df_formateado)

    return


st.set_page_config(page_title="Vencex - Poisson", page_icon="v negra - favicon.png", layout="wide")
st.title(":rainbow[_Calculadora de Probabilidades_]")
st.subheader("Estimación mediante la distribución de :red[Poisson]")
st.write("_-Introduce los datos._")
st.write("_-Haz click en_ :orange[_CALCULAR PROBABILIDADES_]")
st.subheader("", divider="orange")


with st.sidebar:

    st.image("logo vencex portada - 240x60.png", output_format="PNG")

    col1, col2 = st.columns(2)

    col1.write("LOCAL")
    col2.write("VISITANTE")


    local_favor = col1.slider("Media de goles como local, A FAVOR", 0.0, 7.0)
    local_contra = col1.slider("Media de goles como local, EN CONTRA", 0.0, 7.0)
    locales_f = col1.number_input("Media de goles marcados por los equipos LOCALES en la competición", min_value=0.0)

    visitante_favor = col2.slider("Media de goles como visitante, A FAVOR", 0.0, 7.0)
    visitante_contra = col2.slider("Media de goles como visitante, EN CONTRA", 0.0, 7.0)
    visitantes_f = col2.number_input("Media de goles marcados por los equipos VISITANTES en la competición", min_value=0.0)


if locales_f != 0 and visitantes_f != 0:
    pass
else:
    st.stop()


if st.sidebar.button("CALCULAR PROBABILIDADES"):
    calcular_probs()
else:
    pass
