import plotly.express as px
import geopandas as gpd
import streamlit as st

# Load GeoJSON data for India states
india_states_path = "D:\\Projects\\phonepe_pulse\\state_shape\\india_states.geojson"

def indian_states():
    #Load GeoJSON file
    india_states = gpd.read_file(india_states_path)

    # Choropleth map of India
    fig = px.choropleth(
        india_states,
        geojson=india_states.geometry,
        locations=india_states.index,
        color="State_Name",
        projection="mercator"
    )

    fig.update_geos(fitbounds="locations", visible=False)

    st.plotly_chart(fig)