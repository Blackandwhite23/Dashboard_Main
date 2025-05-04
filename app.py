import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard-Prototyp – Supermarktkette")

# Verkauf laden
df = pd.read_csv("verkauf.csv", parse_dates=["Datum"])
df_kpi = df.groupby("Datum").sum(numeric_only=True).reset_index()

# KPI-Chart Forecast vs Ist
st.subheader("🧮 Verkauf Ist vs. Forecast")
fig1 = px.line(df_kpi, x="Datum", y=["Verkauf_Ist", "Forecast"], markers=True,
               labels={"value": "Verkauf", "variable": "Typ"},
               title="Täglicher Verkaufsvergleich")
st.plotly_chart(fig1, use_container_width=True)

# Verspätete Lieferungen
df_liefer = pd.read_csv("lieferung.csv")
df_filialen = pd.read_csv("filialen.csv")
df_liefer = df_liefer.merge(df_filialen, left_on="Ziel_Filiale", right_on="Filial_ID")

# Dummy-Koordinaten (vereinfacht)
import numpy as np
import random
df_liefer['Lat'] = df_liefer['Land'].apply(lambda x: 50 + random.uniform(-4, 4))
df_liefer['Lon'] = df_liefer['Land'].apply(lambda x: 10 + random.uniform(-4, 4))

st.subheader("🚚 Verspätete Lieferungen")
fig2 = px.scatter_geo(df_liefer,
                      lat='Lat', lon='Lon',
                      size='Menge',
                      color='Verspätung_Tage',
                      hover_name='Ziel_Filiale',
                      color_continuous_scale='OrRd',
                      title='Lieferverzögerungen nach Filiale',
                      projection='natural earth')
st.plotly_chart(fig2, use_container_width=True)
