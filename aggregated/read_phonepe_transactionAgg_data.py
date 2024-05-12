import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import json
import os

load_dotenv()

class DataExtractor:
    def __init__(self, root_directory):
        self.root_directory = root_directory

    # Function to convert string to camel case with space instead of "-"
    def format_state_name(self, state):
        words = state.split('-')
        formatted_state = ' '.join([word.capitalize() for word in words])
        if formatted_state.count("&") > 1:
            formatted_state = formatted_state.replace("&", "and")
        return formatted_state

    def extract_transaction_data(self):
        all_data = {
            'State': [],
            'Year': [],
            'Quarter': [],
            'Transaction_type': [],
            'Transaction_count': [],
            'Transaction_amount': []
        }

        # Loop through each state directory
        for state in os.listdir(self.root_directory):
            state_path = os.path.join(self.root_directory, state)

            # Format state name to camel case and remove special characters
            formatted_state = self.format_state_name(state)

            # Process year and file subdirectories within the state directory
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                for file in os.listdir(year_path):
                    file_path = os.path.join(year_path, file)
                    
                    try:
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                            for transaction in data['data']['transactionData']:
                                transaction_type = transaction['name']
                                transaction_count = transaction['paymentInstruments'][0]['count']
                                transaction_amount = transaction['paymentInstruments'][0]['amount']

                                all_data['State'].append(formatted_state)
                                all_data['Year'].append(year)
                                all_data['Quarter'].append(file.strip('.json'))
                                all_data['Transaction_type'].append(transaction_type)
                                all_data['Transaction_count'].append(transaction_count)
                                all_data['Transaction_amount'].append(transaction_amount)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

        # Create DataFrame
        return pd.DataFrame(all_data)

# Set the root directory path
root_directory = r'D:\Projects\pulse\data\aggregated\transaction\country\india\state'

# Create an instance of DataExtractor
data_extractor = DataExtractor(root_directory)

# Extract data and create DataFrame
agg_data = data_extractor.extract_transaction_data()
print(agg_data)

# Define the database connection parameters
host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASS')

# Create a connection to the MySQL database
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Define the table name
table_name = 'agg_transaction_data'  # Change this to the desired table name

# Save the DataFrame as a table in the MySQL database
agg_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Close the database connection
engine.dispose()

print("DataFrame saved as a table in the MySQL database.")
