
def print_menu(adminFlag):

    options = {
        "1": "Search with ID",
        "2": "Statistics",
    }

    #Features only admins can access are added dynamically when admin mode is activated
    if adminFlag:
        options["3"] = "Manage Enclosures (Admin Only)"
        options["4"] = "Employee Records (Admin Only)"

    startupMessage = """
    \n----ZOO DATABASE TERMINAL INTERFACE----
    \nPlease select one of the following options:
    """

    menu_body = [f"{k}. {v}" for k, v in sorted(options.items())]
    menu_body.append("0. Exit")

    print(startupMessage)
    print("\n".join(menu_body))
    
    #Return both the user input and the valid keys for validation
    return input("\nWaiting for input... "), list(options.keys()) + ["0"]


def validate_menu_choice(adminFlag):
        
    while True:
        choice, valid_keys = print_menu(adminFlag)

        if choice in valid_keys:
            match choice:
                case "0":
                    print("Exiting program...")
                    exit(0)
                
            return choice

        print(f"\nInvalid input. Please select from: {', '.join(sorted(valid_keys))}")

def user_login(connection):

    while True:
        user_input = input("Enter your ID:\n")
        
        if user_input == '0':
            return False, "Admin" #False to activate admin mode
        
        if len(user_input) == 6 and user_input.startswith('20') and user_input.isdigit():
            #Fetch the employee name from the database using the provided user_id
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT Name FROM Employee WHERE Employee_ID = ?", (user_input,))
                result = cursor.fetchone()
                
                if result:
                    # Success: ID exists, and we have the name
                    return user_input, result[0]
                else:
                    print(f"Access Denied: ID {user_input} not found in our records.")
            except Exception as e:
                print(f"Database error: {e}")
        else:
            print("Invalid ID. Please provide a valid employee ID.")
