import pandas as pd
import json
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Function to convert string to camel case with space instead of "-"
def to_camel_case(s):
    words = s.split('-')
    return ' '.join([word.capitalize() for word in words])

def replace_ampersand(state):
    if state.count("&") > 1:
        state = state.replace("&", "and")
    return state

def extract_transactionUser_data(root_directory):
    all_data = {
        'State': [],
        'Year': [],
        'Quarter': [],
        'Brand': [],
        'User_count': [],
        'Percentage': []
    }

    # Loop through each state directory
    for state in os.listdir(root_directory):
        state_path = os.path.join(root_directory, state)
         # Format state name to camel case and remove special characters
        formatted_state = replace_ampersand (to_camel_case(state))
        # Process year and file subdirectories within the state directory
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                file_path = os.path.join(year_path, file)
                
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        # Use 'or []' to handle case when data['data']['usersByDevice'] is None
                        for user in data['data']['usersByDevice'] or []:
                            brand = user['brand']
                            user_count = user['count']
                            percentage = user['percentage']
                            all_data['State'].append(formatted_state)
                            all_data['Year'].append(year)
                            all_data['Quarter'].append(file.strip('.json'))
                            all_data['Brand'].append(brand)
                            all_data['User_count'].append(user_count)
                            all_data['Percentage'].append(percentage)
                        
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Create DataFrame
    return pd.DataFrame(all_data)

# Set the root directory path
root_directory = r'D:\Projects\pulse\data\aggregated\user\country\india\state'

# Extract data and create DataFrame
agg_user_data = extract_transactionUser_data(root_directory)
print(agg_user_data)

# Define database connection parameters
host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASS')

# Establish connection to the MySQL database
try:
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    if connection.is_connected():
        cursor = connection.cursor()

        # Truncate the table to remove existing data
        cursor.execute("TRUNCATE TABLE agg_user_data")

        # Insert new data into the MySQL database
        for index, row in agg_user_data.iterrows():
            sql_query = """
                INSERT INTO agg_user_data (State, Year, Quarter, Brand, User_count, Percentage)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_query, tuple(row))
        
        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

except mysql.connector.Error as error:
    print(f"Error while connecting to MySQL: {error}")

finally:
    # Close connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
