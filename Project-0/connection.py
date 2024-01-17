import mysql.connector
import pandas as pd

host = 'localhost'
database = 'revtrends'

def connect_to_database(username, password):
    return mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )




def new_user():
    username = input("Enter a new username: ")
    password = input("Enter a password: ")

    # Connect as admin to grant privileges and insert the new user into the users table
    admin_connection = connect_to_database('admin', 'Nikhil@1907')

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
                admin_cursor.execute("INSERT INTO db_users (username, password, role) VALUES (%s, %s, %s)", (username, password, 'regular_user'))
                admin_connection.commit()

                print("New user created successfully with SELECT privileges.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the admin connection
            admin_cursor.close()
            admin_connection.close()
            print("Admin connection closed")

def User():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        # Connect as a regular user to validate credentials
        user_connection = connect_to_database(username, password)

        if user_connection.is_connected():
            print(f"Login successful. Welcome, {username}!")

            # Check user credentials and role
            cursor = user_connection.cursor(dictionary=True)
            cursor.execute("SELECT role FROM db_users WHERE username = %s AND password = %s", (username, password))
            user_info = cursor.fetchone()

            if user_info and user_info['role'] == 'regular_user':
                print("You have regular user privileges.")

                # Offer additional option to the user
                print("\nOptions:")
                print("1. Execute your own query")
                print("2. See which platform got more likes")
                print("3. See Which Category Got Trend")
                print("4. see Which Sentiment Got Trend")
                option = input("Enter your choice: ")

                if option == '1':
                    # Enter the query and execute it
                    query = input("Enter the query you want to execute: ")
                    cursor.execute(query)

                    # Fetch and print the results
                    results = cursor.fetchall()
                    for row in results:
                        print(row)

                elif option == '2':
                    # Execute the query to see which platform got more likes
                    platform_likes_query = """
                        SELECT p.platform, SUM(m.Likes) AS TotalLikes
                        FROM main_table m
                        JOIN platform p ON m.Platform_id = p.Platform_id
                        WHERE m.Year = 2023
                        GROUP BY p.Platform_id
                        ORDER BY TotalLikes DESC
                        LIMIT 1;
                        

                    """
                    cursor.execute(platform_likes_query)

                    # Fetch and print the results
                    platform_likes_result = cursor.fetchall()
                    for row in platform_likes_result:
                        print(f"The platform with the most likes is {row['platform']} with {row['TotalLikes']} likes.")

                elif option == '3':
                    # Execute the query to see which category got more likes
                    trending_category=""" select c.categories,count(*) as C_count
                                                from main_table m
                                                join categories c on m.categories_id=c.category_id
                                                where Year=2023                                   
                                                group by c.category_id
                                                order by  C_count desc
                                                limit 1;
                                            """
                    cursor.execute(trending_category)

                    # Fetch and print the results
                    trending_category_result = cursor.fetchall()
                    for row in trending_category_result:
                        print(f"The Most Trending Category is >> {row['categories']} <<  with {row['C_count']} likes.")


                elif option == '4':
                    # Execute the query to see which category got more likes
                    trending_sentiment=""" select s.sentiment,count(*) as S_count
                                                from main_table m
                                                join sentiment s on m.sentiment_id=s.sentiment_id
                                                where Year=2023                                   
                                                group by s.sentiment_id
                                                order by  S_count desc
                                                limit 1;
                                            """
                    cursor.execute(trending_sentiment)

                    # Fetch and print the results
                    trending_sentiment_result = cursor.fetchall()
                    for row in trending_sentiment_result:
                        print(f"The Most Trending Sentiment is >> {row['sentiment']} <<  with {row['S_count']} likes.")

                        

                else:
                    print("Invalid option.")

            elif not user_info:
                print("Error: Invalid username or password.")

            else:
                print("Error: Insufficient privileges. Contact admin for assistance.")

            # Close the connection
            cursor.close()
            user_connection.close()
            print("Connection closed")

    except mysql.connector.Error as e:
        if "Access denied" in str(e):
            print("Error: Access denied. Username is not matched with the database.")
        else:
            print(f"Error: {e}")


def admin():
    username = input("Enter your admin username: ")
    password = input("Enter your admin password: ")

    # Connect as an admin user to validate credentials
    admin_connection = connect_to_database(username, password)

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




while True:
    print("\nPress 1 if you are a new user.")
    print("Press 2 if you want to login.")
    print("Press 3 if you are a Admin.")
    print("Press any other key to exit.")

    choice = input("Enter your choice: ")

    if choice == '1':
        new_user()

    elif choice == '2':
        User()
    
    elif choice == '3':
        admin()

    else:
        print("Exiting authentication.")
        break
        



# from sqlalchemy import create_engine

# loading a excel file 
# def load_data_from_excel():
#     user = 'admin1'
#     password = 'nikhil123'
#     excel_file_path = "D:\Revature\P0_dataset\Main_table.xlsx"

#     try:
#         # Read data from Excel file into a pandas DataFrame
#         df = pd.read_excel(excel_file_path)

#         # Connect to the MySQL database
#         connection = connect_to_database('root', 'Nikhil@1907')

#         if connection.is_connected():
#             cursor = connection.cursor()

#             try:
#                 # Create an SQLAlchemy engine
#                 engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@localhost/revtrends".format(
#                     user,password
#                 ))

#                 # Write DataFrame to MySQL database using the SQLAlchemy engine
#                 df.to_sql(name='main_table', con=engine, if_exists='replace', index=False)

#                 print("Data loaded successfully into main_table.")

#             except mysql.connector.Error as err:
#                 print(f"Error: {err}")

#             finally:
#                 # Close the cursor and connection
#                 cursor.close()
#                 connection.close()
#                 print("Connection closed")

#     except Exception as e:
#         print(f"Error: {e}")

# load_data_from_excel()