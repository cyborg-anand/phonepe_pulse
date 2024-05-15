# import streamlit as st
# import geopandas as gpd

# # Load GeoJSON data for India states
# india_states_path = "D:\\Projects\\phonepe_pulse\\state_shape\\india_states.geojson"

# # Read GeoJSON file into a GeoDataFrame
# india = gpd.read_file(india_states_path)

# def main():
#     st.title("India State Details")

#     # Display the first few rows of the GeoDataFrame
#     st.subheader("GeoDataFrame Details")
#     st.write(india.head())

#     # Display the state names from the GeoDataFrame
#     st.subheader("State Names")
#     st.write(india['st_nm'])

# if __name__ == "__main__":
#     main()
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import geopandas as gpd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load GeoJSON data for India states
india_states_path = "D:\\Projects\\phonepe_pulse\\state_shape\\india_states.geojson"

# Function to connect to the MySQL database
def connect_to_database():
    host = os.getenv('HOST')
    database = os.getenv('DATABASE')
    user = os.getenv('USER')
    password = os.getenv('PASS')
    
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return connection
    except mysql.connector.Error as error:
        st.error(f"Error while connecting to MySQL: {error}")

# Function to fetch distinct years from the database
def fetch_years(connection):
    query = "SELECT DISTINCT Year FROM agg_transaction_data;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        years = [year[0] for year in cursor.fetchall()]
    return years

# Function to fetch transaction data based on selected year and state
def fetch_transaction_data(connection, selected_year, selected_state):
    query = f"""
        SELECT Transaction_type, SUM(Transaction_amount) AS Total_Transaction_Amount
        FROM agg_transaction_data
        WHERE Year = '{selected_year}' AND State = '{selected_state}'
        GROUP BY Transaction_type;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        transaction_data = cursor.fetchall()
    return transaction_data

# Show Page 1 with India state map and transaction data
def show_page():
    st.title("Page 1")
    
    connection = connect_to_database()
    
    # Dropdown for selecting year
    selected_year = st.selectbox("Select Year", [""] + fetch_years(connection))
    
    if selected_year:
        # Load GeoJSON file for India states
        india_states = gpd.read_file(india_states_path)
        
        # Choropleth map of India
        fig = px.choropleth_mapbox(
            india_states,
            geojson=india_states.geometry,
            locations=india_states.index,
            color="ST_NM",
            mapbox_style="carto-positron",
            zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},
            opacity=0.5,
            labels={"ST_NM": "State"}
        )
        
        # Add interactivity to the map
        fig.update_traces(marker_line_width=1, marker_line_color="black")
        fig.update_layout(clickmode='event+select')
        
        # Plotly chart
        st.plotly_chart(fig)

        # Get clicked data
        selected_state = st.selectbox("Select State", india_states['ST_NM'].tolist())
        if selected_state:
            transaction_data = fetch_transaction_data(connection, selected_year, selected_state)
            df = pd.DataFrame(transaction_data, columns=["Transaction Type", "Total Transaction Amount"])
            st.write("Transaction Data:")
            st.dataframe(df)

if __name__ == "__main__":
    show_page()


