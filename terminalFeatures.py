
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
                    #ID exists, and we have the name
                    return user_input, result[0]
                else:
                    print(f"Access Denied: ID {user_input} not found in our records.")
            except Exception as e:
                print(f"Database error: {e}")
        else:
            print("Invalid ID. Please provide a valid employee ID.")


def search_by_id(connection, entity_id):
    
    if len(entity_id) == 6 and entity_id.startswith('8') and entity_id.isdigit():
        #Fetch the ticket's details from the database using the provided ticket_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Ticket WHERE Ticket_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")

    elif len(entity_id) == 6 and entity_id.startswith('9') and entity_id.isdigit():
        #Fetch the event's details from the database using the provided event_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Event WHERE Event_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")

    elif len(entity_id) == 6 and entity_id.startswith('10') and entity_id.isdigit():
        #Fetch the animal's details from the database using the provided animal_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Animal WHERE Animal_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")

    elif len(entity_id) == 6 and entity_id.startswith('12') and entity_id.isdigit():
        #Fetch the contract's details from the database using the provided contract_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Contract WHERE Contract_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")

    elif len(entity_id) == 6 and entity_id.startswith('15') and entity_id.isdigit():
        #Fetch the diet's details from the database using the provided diet_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Diet WHERE Diet_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")

    elif len(entity_id) == 6 and entity_id.startswith('20') and entity_id.isdigit():
        #Fetch the employee's details from the database using the provided employee_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Employee WHERE Employee_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")
    
    elif len(entity_id) == 6 and entity_id.startswith('30') and entity_id.isdigit():
        #Fetch the food's details from the database using the provided food_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Food WHERE Food_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")

    elif len(entity_id) == 6 and entity_id.startswith('44') and entity_id.isdigit():
        #Fetch the area's details from the database using the provided area_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Area WHERE Area_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")

    elif len(entity_id) == 6 and entity_id.startswith('54') and entity_id.isdigit():
        #Fetch the habitat's details from the database using the provided habitat_id
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Habitat WHERE Habitat_ID = ?", (entity_id,))
            result = cursor.fetchall()
            
            if result:
                #ID exists
                return result[0]
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")
    
    else:
        print("Invalid ID format. Please ensure the ID is correct.")
