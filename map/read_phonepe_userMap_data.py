import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Function to convert string to camel case with space instead of "-"
def to_camel_case(s):
    words = s.split('-')
    return ' '.join([word.capitalize() for word in words])

def replace_ampersand(state):
    if state.count("&") > 1:
        state = state.replace("&", "and")
    return state

def case_remove_text(d):
    rwords=d.rsplit(' ', 1)[0]
    rwords_caps= rwords.title()
    return rwords_caps


def extract_transaction_data(root_directory):
    all_data = {
        'State': [],
        'Year': [],
        'Quarter': [],
        'District': [],
        'RegisteredUsers': []
    }

    # Loop through each state directory
    for state in os.listdir(root_directory):
        state_path = os.path.join(root_directory, state)

        # Format state name to camel case and remove special characters
        formatted_state = replace_ampersand(to_camel_case(state))

        # Process year and file subdirectories within the state directory
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                file_path = os.path.join(year_path, file)

                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        for district, district_data in data['data']['hoverData'].items():
                            formatted_district = case_remove_text(district)
                            registered_users = district_data['registeredUsers']

                            # Append data to respective lists
                            all_data['State'].append(formatted_state)
                            all_data['Year'].append(year)
                            all_data['Quarter'].append(file.strip('.json'))
                            all_data['District'].append(formatted_district)
                            all_data['RegisteredUsers'].append(registered_users)

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Check if all arrays have the same length
    length_check = len(set(len(v) for v in all_data.values()))
    if length_check != 1:
        raise ValueError("All arrays must be of the same length")

    # Create DataFrame
    return pd.DataFrame(all_data)


# Set the root directory path
root_directory = r'D:\Projects\pulse\data\map\user\hover\country\india\state'

# Extract data and create DataFrame
map_user_dist_data = extract_transaction_data(root_directory)
print(map_user_dist_data)

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
        cursor.execute("TRUNCATE TABLE map_user_dist_data")

        # Insert new data into the MySQL database
        for index, row in map_user_dist_data.iterrows():
            sql_query = """
                INSERT INTO map_user_dist_data (State, Year, Quarter, District, Registered_users)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_query, tuple(row))
        
        # Commit the user
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

