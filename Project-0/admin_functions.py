import mysql.connector

def connect_to_database(username, password, database):
    return mysql.connector.connect(
        host='localhost',
        user=username,
        password=password,
        database=database
    )

def admin():
    username = input("Enter your admin username: ")
    password = input("Enter your admin password: ")
    database = 'revtrends'

    # Connect as an admin user to validate credentials
    admin_connection = connect_to_database(username, password, database)

    if admin_connection.is_connected():
        print(f"Login successful. Welcome, {username}!")

        # Check user credentials and role
        cursor = admin_connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM db_users WHERE username = %s AND password = %s", (username, password))
        user_info = cursor.fetchone()

        if user_info and user_info['role'] == 'admin':
            print("You have admin privileges. You can perform CRUD operations.")

            # Enter the query and execute it
            query = input("Enter the query you want to execute: ")
            cursor.execute(query)

            # If the query is not a SELECT query, commit the changes
            if not query.strip().lower().startswith('select'):
                admin_connection.commit()
                print("Changes committed successfully.")

            # Fetch and print the results for SELECT queries
            if query.strip().lower().startswith('select'):
                results = cursor.fetchall()
                for row in results:
                    print(row)

        elif not user_info:
            print("Error: Invalid username or password.")

        else:
            print("Error: Insufficient privileges. Contact admin for assistance.")

        # Close the connection
        cursor.close()
        admin_connection.close()
        print("Connection closed")

    else:
        print("Login failed. Invalid username or password.")
