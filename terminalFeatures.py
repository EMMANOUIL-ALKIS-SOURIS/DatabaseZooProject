import queries


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


def search_by_id(connection):

    while True:
        entity_id = input("Enter the ID to search for or type 'Cancel' to return to the menu:\n")
        
        if entity_id.lower() == 'cancel':
            return None

        #Sepcific prefixes for each entity type
        prefixes = {
            "8": "Ticket",
            "9": "Event",
            "10": "Animal",
            "12": "Contract",
            "15": "Diet",
            "20": "Employee",
            "30": "Food",
            "44": "Area",
            "54": "Habitat"
        }

        #Check the provided ID's format
        if not (len(entity_id) == 6 and entity_id.isdigit()):
            print("Invalid ID format. Please ensure the ID is correct.")
            continue

        #Scan through all available tables to see whether the ID's prefix matches any known entity
        table_name = None
        for prefix, table in prefixes.items():
            if entity_id.startswith(prefix):
                table_name = table
                break

        #Case where no matching table is found with provided 6 digit ID
        if not table_name:
            print("Invalid ID format. Please ensure the ID is correct.")
            continue

        #Being here means that the ID's prefix matches a known entity and we're ready to retrieve data from the database
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM {table_name} WHERE {table_name}_ID = ?"
            cursor.execute(query, (entity_id,))
            result = cursor.fetchone()
            
            if result:
                #**Being here means that given ID exists**
                
                #Fetch sepcific's data and metadata (column names)

                column_names = [description[0] for description in cursor.description]
                
                output_parts = [f"\n'{name}' : {val}" for name, val in zip(column_names, result)]
                formatted_output = " ".join(output_parts)
                
                print(f"\nMatching record of type '{table_name}' found:")
                print(formatted_output)

                #Dynamically searching the references of each entity type
                if table_name == "Ticket":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getTicketQueries())

                elif table_name == "Event":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getEventQueries())

                elif table_name == "Animal":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getAnimalQueries())

                elif table_name == "Contract":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getContractQueries())

                elif table_name == "Diet":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getDietQueries())

                elif table_name == "Employee":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getEmployeeQueries())
                
                elif table_name == "Food":                    
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getFoodQueries())                

                elif table_name == "Area":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getAreaQueries())

                elif table_name == "Habitat":
                    queries.referenceSearchQueries(table_name, entity_id, cursor, queries.getHabitatQueries())

                return result #Returns first matching record with specified ID (in case it's needed in invoking method)
            else:
                print(f"ID {entity_id} not found in our records.")

        except Exception as e:
            print(f"Database error: {e}")


