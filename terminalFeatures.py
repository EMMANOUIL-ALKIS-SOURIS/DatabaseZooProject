

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
    \n----ZOO DATABASE TERMINAL INTERFACE----\n
Please select one of the following options:
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

        print(f"\n[!] Invalid input. Please select from: {', '.join(sorted(valid_keys))}")

def get_id():

    while True:
        user_input = input("Enter your ID:\n")
        
        if len(user_input) == 6 and user_input.startswith('20') and user_input.isdigit():
            return user_input
        elif user_input == '0':
            return False #False to activate admin mode
        
        print("Invalid ID. Must be a valid employee ID.")


if __name__ == "__main__":

    #Get user ID
    user_id = get_id()
    is_admin = (user_id is False) #is_admin is True when the user inputs '0' and thus user_is is False

    

    if is_admin:
        print("\nWelcome Admin. Accessing full database...")
    else:
        print(f"\nWelcome, User {user_id}!")
    
    final_choice = validate_menu_choice(is_admin)
    print(f"\nProceeding to option: {final_choice}")
