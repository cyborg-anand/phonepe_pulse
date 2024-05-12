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




def extract_transaction_data(root_directory):
    all_data = {
        'State': [],
        'Year': [],
        'Quarter': [],
        'Pincode': [],
        'Registered_users': [],
        
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
                        for user in data['data']['pincodes']:
                            transaction_pincode = user['name']
                            #formatted_district= case_remove_text(transaction_district)
                            registered_users = user['registeredUsers']
                           

                            all_data['State'].append(formatted_state)
                            all_data['Year'].append(year)
                            all_data['Quarter'].append(file.strip('.json'))
                            all_data['Pincode'].append(transaction_pincode)
                            all_data['Registered_users'].append(registered_users)
                            
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Create DataFrame
    return pd.DataFrame(all_data)


# Set the root directory path
root_directory = r'D:\Projects\pulse\data\top\user\country\india\state'

# Extract data and create DataFrame
top_user_pin_data = extract_transaction_data(root_directory)
print(top_user_pin_data)

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
        cursor.execute("TRUNCATE TABLE top_user_pin_data")

        # Insert new data into the MySQL database
        for index, row in top_user_pin_data.iterrows():
            sql_query = """
                INSERT INTO top_user_pin_data (State, Year, Quarter, Pincode, Registered_users)
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