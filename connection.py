import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Databse Connection
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