import pandas as pd
import streamlit as st
import pydeck as pdk

# Leer el archivo CSV
data = pd.read_csv("Lenguas_COL_denger_2_updated.csv")

# Convertir la columna "Hablantes" a números
data["Hablantes"] = data["Hablantes"].str.replace(",", "").astype(float)

# Dividir la columna "coordenadas" en "Latitud" y "Longitud"
data[["Latitud", "Longitud"]] = data["coordenadas"].str.replace(", ", ",").str.split(",", expand=True).astype(float)

# Obtener los datos filtrados por cantidad de hablantes
verde_data = data[data["Hablantes"] > 10000]
naranja_data = data[(data["Hablantes"] >= 1000) & (data["Hablantes"] <= 5000)]
rojo_data = data[data["Hablantes"] < 1000]

st.title("Lenguas Indígenas de Colombia por Número de Hablantes")
st.text("Datos extraídos de endangeredlanguages.com y endangeredlanguages.com (2023)")
st.text("Visualización de datos por @jp@col.social")
st.test("Pasa el cursor sobre los círculos o barras para ver más información")

# Configurar el tooltip
tooltip = {
    "html": "<b>Lengua:</b> {lengua}",
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=data["Latitud"].mean(),
        longitude=data["Longitud"].mean(),
        zoom=5,
        pitch=60,
        bearing=-30,
    ),
    layers=[
        pdk.Layer(
            "ColumnLayer",
            data=verde_data,
            get_position=["Longitud", "Latitud"],
            get_elevation="Hablantes",
            radius=5000,
            get_fill_color=[0, 255, 0],  # Verde
            pickable=True,
            auto_highlight=True
        ),
        pdk.Layer(
            "ColumnLayer",
            data=naranja_data,
            get_position=["Longitud", "Latitud"],
            get_elevation="Hablantes",
            radius=5000,
            get_fill_color=[255, 165, 0],  # Naranja
            pickable=True,
            auto_highlight=True
        ),
        pdk.Layer(
            "ColumnLayer",
            data=rojo_data,
            get_position=["Longitud", "Latitud"],
            get_elevation="Hablantes",
            radius=5000,
            get_fill_color=[255, 0, 0],  # Rojo
            pickable=True,
            auto_highlight=True
        ),
    ],
    tooltip=tooltip  # Añadimos la configuración del tooltip aquí
))

# Mostrar los datos filtrados en una tabla
st.subheader("Datos de las Lenguas Indígenas de Colombia")

# Filtrar columnas
data_display = data[["lengua", "también conocido como", "Hablantes", "lengua-href"]].copy()
data_display.columns = ["Lengua", "También Conocido Como", "Número de Hablantes", "Enlace de Referencia URL"]
data_display.insert(0, "Número", range(1, len(data_display) + 1))  # Agregamos una columna de números
st.dataframe(data_display)
