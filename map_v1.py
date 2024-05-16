# page1.py
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from connection import connect_to_database as connect_db
from other_fun import fetch_years, fetch_states, fetch_and_display_transaction_data

# Load GeoJSON data for India states
india_states_path = "D:\\Projects\\phonepe_pulse\\india_states.geojson"

# Show Page 1 with dropdowns and transaction data
def show_page():
    st.write("Transaction details")
    st.write("Select a year and state to view transaction data:")

    # connect to Database
    connection = connect_db()
    
    # Dropdowns for selecting year and state
    selected_year = st.selectbox("Select Year", [""] + fetch_years(connection))
    selected_state = st.selectbox("Select State", [""] + fetch_states(connection))
    
    if selected_state and selected_year:
        # Fetch and display transaction data based on selected year and state
        transaction_data = fetch_and_display_transaction_data(connection, selected_year, selected_state)
        st.write(f"Transaction data for {selected_state} in {selected_year}:")
        df = pd.DataFrame(transaction_data, columns=["Transaction Type", "Total Transaction Amount"])
        st.dataframe(df)
        
        # Load GeoJSON file
        india_states = gpd.read_file(india_states_path)
        
        # Filter GeoDataFrame to include only the selected state
        selected_state_data = india_states[india_states['State_Name'] == selected_state]

        # Plot choropleth map for the selected state
        fig = px.choropleth(
            selected_state_data,
            geojson=selected_state_data.geometry,
            locations=selected_state_data.index,
            color='State_Name'  # Color based on state name
           
            
            )
        
        fig.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig)

if __name__ == "__main__":
    show_page()
