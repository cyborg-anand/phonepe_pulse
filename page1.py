import streamlit as st
import pandas as pd
from connection import connect_to_database as connect_db
from other_fun import fetch_years, fetch_states, fetch_and_display_transaction_data
from india_states import indian_states

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
        indian_states()

if __name__ == "__main__":
    show_page()