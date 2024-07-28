from functions import register_user, login_user  # Import functions from functions.py

def main():
    while True:
        try:
            print("Welcome to the authentication system!")
            action = input("Do you want to (1) Register or (2) Login? Enter 1 or 2: ")

            if action == '1':
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                password = input("Enter your password: ")

                if register_user(name, email, password):
                    print("Congratulations! You have successfully registered.")
                    login_now = input("Do you want to login now? (yes/no): ")
                    if login_now.lower() == 'yes':
                        if login_user(email, password):
                            print(f"Welcome back, {name}!")
                            break  # Exit the loop if login is successful
                        else:
                            print("Login failed. Please check your credentials and try again.")
                else:
                    print("Registration failed. Please try again.")

            elif action == '2':
                email = input("Enter your email: ")
                password = input("Enter your password: ")

                if login_user(email, password):
                    print("Welcome to the system!")
                    break  # Exit the loop if login is successful
                else:
                    print("Login failed. Please check your credentials and try again.")

            else:
                print("Invalid choice. Please enter 1 or 2.")

        except ValueError as e:
            print(f"Error: {e}. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")




if __name__ == "__main__":
    main()
