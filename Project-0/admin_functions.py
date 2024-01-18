
# import mysql.connector

# def connect_to_database(username, password, database):
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user=username,
#             password=password,
#             database=database
#         )
#         return connection

#     except mysql.connector.Error as err:
#         if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Error: Access denied. Invalid username or password.")
#             return None
#         else:
#             print(f"Error: {err}")
#             raise  # Re-raise other errors to terminate the program if connection fails

# def admin():
#     username = input("Enter your admin username: ")
#     password = input("Enter your admin password: ")
#     database = 'revtrends'

#     # Connect as an admin user to validate credentials
#     admin_connection = connect_to_database(username, password, database)
#     exit=False

#     if admin_connection is not None:  # Check if connection is successful
#         try:
#             print(f"Login successful. Welcome, {username}!")

#             while True:

#             # Check user credentials and role
#                 cursor = admin_connection.cursor(dictionary=True)
#                 cursor.execute("SELECT role FROM db_users WHERE username = %s AND password = %s", (username, password))
#                 user_info = cursor.fetchone()

#                 if user_info and user_info['role'] == 'admin':
#                     print("You have admin privileges. You can perform CRUD operations.")

#                     # Enter the query and execute it
#                     query = input("Enter the query you want to execute: ")
#                     cursor.execute(query)

#                     # If the query is not a SELECT query, commit the changes
#                     if not query.strip().lower().startswith('select'):
#                         admin_connection.commit()
#                         print("Changes committed successfully.")

#                     # Fetch and print the results for SELECT queries
#                     if query.strip().lower().startswith('select'):
#                         results = cursor.fetchall()
#                         for row in results:
#                             print(row)
#                     elif query.lower() == 'exit':
#                         exit=True
#                         break

#                     # else:
#                     #     print("Invalid option. Please enter a valid option or 'exit' to go back to the main menu.")        

#                 elif not user_info:
#                     print("Error: Invalid username or password.")

#                 else:
#                     print("Error: Insufficient privileges. Contact admin for assistance.")

#         except mysql.connector.Error as e:
#             if "Access denied" in str(e):
#                 print("Error: Access denied. Username is not matched with the database.")
            
#             elif exit:
#                 None
            
#             elif exit==False and 'SQL syntax' in str(e):
#                 print('Syntax Error, Please check the query')
#             else:
#                 print(f"Error: {e}")

#         finally:
#             # Close the connection
#             cursor.close()
#             admin_connection.close()
#             print("Connection closed")

#     else:
#         print("Login failed. Invalid username or password.")



import mysql.connector
from prettytable import PrettyTable

def connect_to_database(username, password, database):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=username,
            password=password,
            database=database
        )
        return connection

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Invalid username or password.")
            return None
        else:
            print(f"Error: {err}")
            return None

def execute_query(connection, query):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)

        # If the query is not a SELECT query, commit the changes
        if not query.strip().lower().startswith('select'):
            connection.commit()
            print("Changes committed successfully.")

        # Fetch and print the results for SELECT queries
        if query.strip().lower().startswith('select'):
            results = cursor.fetchall()
            for row in results:
                print(row)

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()

def admin_menu():
    print("Admin Menu:")
    print("1. Insert")
    print("2. Update")
    print("3. Delete the user")
    print("4. See Which Test has Positive Sentiment")
    print("5. Exit")

def admin():
    username = input("Enter your admin username: ")
    password = input("Enter your admin password: ")
    database = 'revtrends'

    # Connect as an admin user to validate credentials
    admin_connection = connect_to_database(username, password, database)

    if admin_connection is not None:  # Check if connection is successful
        print(f"Login successful. Welcome, {username}!")
        cursor = admin_connection.cursor(dictionary=True)

        while True:
            admin_menu()

            # Get user choice
            choice = input("Enter your choice (1-5): ")

            if choice == '5':
                print("Exiting admin mode.")
                break

            if choice not in ['1', '2', '3', '4']:
                print("Invalid option. Please enter a valid option.")
                continue

            # Get table name and execute query
            # table_name = input("Enter the table name: ")
            query = ''

            if choice == '1':  # Insert
                columns = input("Enter column names (comma-separated): ")
                values = input("Enter values (comma-separated): ")
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            elif choice == '2':  # Update
                column_value_pairs = input("Enter column-value pairs (comma-separated): ")
                condition = input("Enter the WHERE condition: ")
                query = f"UPDATE {table_name} SET {column_value_pairs} WHERE {condition}"
            elif choice == '3':
                # Display data from db_users table
                query_display = "SELECT * FROM db_users"
                cursor.execute(admin_connection, query_display)
                results=cursor.fetchall()

                for row in results:
                    print({
                        'user_id': row['user_id'],
                        'username': row['username'],
                        'password': row['password'],
                        'role': row['role']
                    })

                # Get username to delete
                username_to_delete = input("Enter the username to delete: ")

                # Delete user from db_users table
                query_delete = f"DELETE FROM db_users WHERE username = '{username_to_delete}'"
                execute_query(admin_connection, query_delete)


                # Display updated data from db_users table
                query_display_updated = "SELECT * FROM db_users"
                execute_query(admin_connection, query_display_updated)
            elif choice == '4':  # Read
                query = f"SELECT main_table.text,sentiment.sentiment FROM main_table join sentiment on main_table.sentiment_id=sentiment.sentiment_id limit 10"

                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    # Create a PrettyTable instance
                    table = PrettyTable()
                    table.field_names = ["text", "sentiment"]

                    # Add rows to the table
                    for row in results:
                        table.add_row([row['text'], row['sentiment']])

                    # Set the table align style
                    table.align = 'l'

                    # Print the table
                    print(table)
                else:
                    print("No results found.")
            # execute_query(admin_connection, query)

        # Close the connection
        admin_connection.close()
        print("Connection closed")

    else:
        print("Login failed. Invalid username or password.")

# Run the admin function

