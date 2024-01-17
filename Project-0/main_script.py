from admin_functions import admin
from new_user_functions import new_user
from user_functions import User

while True:
    print("\nPress 1 if you are a new user.")
    print("Press 2 if you want to login.")
    print("Press 3 if you are an Admin.")
    print("Press any other key to exit.")

    choice = input("Enter your choice: ")

    if choice == '1':
        new_user()

    elif choice == '2':
        User()

    elif choice == '3':
        admin()

    else:
        print("Invalid choice.")
        break
