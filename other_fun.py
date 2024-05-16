# Function to fetch distinct years from the database
def fetch_years(connection):
    query = "SELECT DISTINCT Year FROM agg_transaction_data;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        years = [year[0] for year in cursor.fetchall()]
    return years

# Function to fetch distinct state names from the database
def fetch_states(connection):
    query = "SELECT DISTINCT State FROM agg_transaction_data;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        states = [state[0] for state in cursor.fetchall()]
    return states

# Function to format transaction amount
def format_transaction_amount(amount):
    if amount >= 10000000:  # Crores
        return f"{amount / 10000000:.2f} Crores"
    elif amount >= 100000:  # Lakhs
        return f"{amount / 100000:.2f} Lakhs"
    elif amount >= 1000:  # Thousands
        return f"{amount / 1000:.2f} Thousands"
    elif amount >= 100:  # Hundreds
        return f"{amount:.2f}"
    elif amount >= 10:  # Tens
        return f"{amount:.2f}"
    else:  # Ones
        return f"{amount:.2f}"
    
# Fetch and display transaction data based on selected year and state
def fetch_and_display_transaction_data(connection, selected_year, selected_state):
    
    query1 = f"""
        SELECT Transaction_type, SUM(Transaction_amount) AS Total_Amount
        FROM agg_transaction_data
        WHERE Year = '{selected_year}' AND State = '{selected_state}'
        GROUP BY Transaction_type;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query1)
        transaction_data = cursor.fetchall()
    
    # Format transaction amount
    formatted_data = [(transaction_type, format_transaction_amount(amount)) for transaction_type, amount in transaction_data]

    return formatted_data
def fetch_map_data(connection, selected_year, selected_state):
    query2 = f"""
        SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount
        FROM agg_transaction_data
        WHERE Year = '{selected_year}' AND State = '{selected_state}'
        GROUP BY State AND Year;
    """
    with connection.cursor() as cursor:
        cursor.execute(query2)
        transaction_data1 = cursor.fetchall()
    formatted_data1 =[(State, format_transaction_amount(amount1)) for State, amount1 in  transaction_data1]

    return formatted_data1 

    
