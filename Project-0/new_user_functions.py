import mysql.connector

def connect_to_database(username, password, database):
    return mysql.connector.connect(
        host='localhost',
        user=username,
        password=password,
        database=database
    )

def new_user():
    username = input("Enter a new username: ")
    password = input("Enter a password: ")
    database = 'revtrends'

    # Connect as admin to grant privileges and insert the new user into the users table
    admin_connection = connect_to_database('admin', 'Nikhil@1907', database)

    if admin_connection.is_connected():
        admin_cursor = admin_connection.cursor()

        try:
            # Check if the username already exists
            admin_cursor.execute("SELECT * FROM db_users WHERE username = %s", (username,))
            existing_user = admin_cursor.fetchone()

            if existing_user:
                print("Username already exists. Please choose a different username.")
            else:
                # Grant SELECT privileges to the new user
                admin_cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';")
                admin_cursor.execute(f"GRANT SELECT ON {database}.* TO '{username}'@'localhost';")
                admin_connection.commit()

                # Insert the new user into the users table
                admin_cursor.execute("INSERT INTO db_users (username, password, role) VALUES (%s, %s, %s)",
                                    (username, password, 'regular_user'))
                admin_connection.commit()

                print("New user created successfully with SELECT privileges.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the admin connection
            admin_cursor.close()
            admin_connection.close()
            print("connection closed")

