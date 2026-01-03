from connectToDB import connect_to_db
import terminalFeatures as gui

def run_app():
    
    # 1.Open the connection once for the entire session
    db_connection = connect_to_db()

    if not db_connection:
        print("Connection failed. Aborting database operations.")
        return   

    try:

        # 2.Get user identification
        user_id, user_name = gui.user_login(db_connection)
        is_admin = (user_id is False) #is_admin is True when the user inputs '0' and thus user_is is False

        # 3.Dynamic Welcome Message
        if is_admin:
            print("\nWelcome Admin. Accessing full database...")
        else:
            #Fetch and display the specific name for employee user
            print(f"\nWelcome {user_name}!")

        # 4.Main Program Loop - Menu and Choices
        while True:
            choice = gui.validate_menu_choice(is_admin)
            
            match choice:
                case "0":
                    print("Exiting program...")
                    exit(0)
                case "1":
                    #print("\n[Search with ID selected]")
                    user_input = input("Enter the ID to search for:\n")
                    res = gui.search_by_id(db_connection, user_input)
                    print(f"{res}")
                case "2":
                    print("\n[Statistics selected]")
                case "3":
                    print("\n[Manage Enclosures selected]")
                case "4":
                    print("\n[Employee Records selected]")
            
            input("\nPress Enter to return to the menu...")

    except Exception as e:
        print(f"\nA runtime error occurred: {e}")

    finally:
        #Ensure connection closes regardless of what happens when running the program (even if errors occur and the program crashes)
        db_connection.close()

if __name__ == "__main__":
    run_app()