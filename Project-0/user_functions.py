import mysql.connector
import matplotlib.pyplot as plt

def connect_to_database(username, password, database):
    return mysql.connector.connect(
        host='localhost',
        user=username,
        password=password,
        database=database
    )

def User():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    database = 'revtrends'

    try:
        # Connect as a regular user to validate credentials
        user_connection = connect_to_database(username, password, database)

        if user_connection.is_connected():
            print(f"Login successful. Welcome, {username}!")

            while True:

                # Check user credentials and role
                cursor = user_connection.cursor(dictionary=True)
                cursor.execute("SELECT role FROM db_users WHERE username = %s AND password = %s", (username, password))
                user_info = cursor.fetchone()

                if user_info and user_info['role'] == 'regular_user':
                    # print("You have regular user privileges.")

                    # Offer additional option to the user
                    print("\nOptions:")
                    print("1. Execute your own query")
                    print("2. See which platform got more likes")
                    print("3. See which category got trend")
                    print("4. See which sentiment got trend")
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
                            ;
                        """
                        cursor.execute(platform_likes_query)

                        # Fetch and print the results
                        platform_likes_result = cursor.fetchall()
                        print(platform_likes_result)

                        platform=[entry['platform'] for entry in platform_likes_result]
                        Likes=[count['TotalLikes'] for count in platform_likes_result]

                        max_likes_index=Likes.index(max(Likes))
                        colors=['green' if i==max_likes_index else 'blue' for i in range(len(platform))]

                        plt.bar(platform,Likes,color=colors)
                        plt.xlabel('Platforms')
                        plt.ylabel('Likes')
                        plt.title("Platform Analysis")
                        plt.show()

                    elif option == '3':
                        # Execute the query to see which category got more likes
                        trending_category_query = """
                            SELECT c.categories, COUNT(*) AS C_count
                            FROM main_table m
                            JOIN categories c ON m.categories_id = c.category_id
                            WHERE m.Year = 2023
                            GROUP BY c.category_id
                            ;
                        """
                        cursor.execute(trending_category_query)

                        # Fetch and print the results
                        trending_category_result = cursor.fetchall()
                        print(trending_category_result)
                        

                        categories=[entry['categories'] for entry in trending_category_result]
                        counts=[count['C_count'] for count in trending_category_result]

                        max_likes_index=counts.index(max(counts))
                        colors=['green' if i==max_likes_index else 'blue' for i in range(len(categories))]  

                        plt.bar(categories,counts,color=colors)
                        plt.xlabel('Categories')
                        plt.ylabel('counts')
                        plt.title("Categories Analysis")
                        plt.show()


                    elif option == '4':
                        # Execute the query to see which sentiment got more likes
                        trending_sentiment_query = """
                            SELECT s.sentiment, COUNT(*) AS S_count
                            FROM main_table m
                            JOIN sentiment s ON m.sentiment_id = s.sentiment_id
                            WHERE m.Year = 2023
                            GROUP BY s.sentiment_id
                            ;
                        """
                        cursor.execute(trending_sentiment_query)

                        # Fetch and print the results
                        trending_sentiment_result = cursor.fetchall()
                        for row in trending_sentiment_result:
                            print(row)
                            # print(f"The most trending sentiment is {row['sentiment']} with {row['S_count']} likes.")

                        # plot the matplotlib.
                        sentiment=[entry['sentiment'] for entry in trending_sentiment_result]
                        counts=[count['S_count'] for count in trending_sentiment_result]
                        plt.bar(sentiment,counts,color=['Green','blue','blue'])
                        plt.xlabel('Sentiments')
                        plt.ylabel('counts')
                        plt.title("sentiment Analysis")
                        plt.show()

                    elif option.lower() == 'exit':
                            # Break out of the analysis loop
                            break

                    else:
                        print("Invalid option. Please enter a valid option or 'exit' to go back to the main menu.")

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
