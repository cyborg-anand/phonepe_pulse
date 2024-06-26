# page1.py
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from connection import connect_to_database as connect_db
from other_fun import fetch_years, fetch_states, fetch_and_display_transaction_data,fetch_map_data

# Load GeoJSON data for India states
india_states_path = "D:\\Projects\\phonepe_pulse\\india_states.geojson"
# Load GeoJSON file
india_states_geojson = gpd.read_file(india_states_path)


def get_map_colors(selected_state):
  # Define default colors
  fill_color = '#d3d3d3'  # Light gray for unselected states
  line_color = 'black'  # Black border for all states

  # Change fill color for selected state (optional)
  if selected_state:
    fill_color = '#ffc107'  # Example highlight color for selected state

  return fill_color, line_color


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
        df = pd.DataFrame(transaction_data, columns=["Transaction Type", "Total Amount"])
        st.dataframe(df)
       
        # Use formatted_data1 for the map
        map_data = fetch_map_data(connection, selected_year, selected_state)
        df1=pd.DataFrame(map_data,columns=["State","Total Transaction Amount"])
        st.dataframe(df1)

        
if __name__ == "__main__":
    show_page()
