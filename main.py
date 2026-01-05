from connectToDB import connect_to_db
import terminalFeatures as features
import statistics as stat

def run_app():
    
    # 1.Open the connection once for the entire session
    db_connection = connect_to_db()

    if not db_connection:
        print("Connection failed. Aborting database operations.")
        return   

    try:

        #First menu welcome message
        print("\n" + "="*40)
        print("\tWELCOME TO THE ZOO DATABASE")
        print("="*40)

        # 2.Get user identification
        user_id, user_name = features.user_login(db_connection)
        is_admin = (user_id is False) #is_admin is True when the user inputs '0' and thus user_is is False

        # 3.Dynamic Welcome Message
        if is_admin:
            print("\nWelcome Admin. Accessing full database...\n")
        else:
            #Fetch and display the specific name for employee user
            print(f"\nWelcome {user_name}!\n")

        # 4.Main Program Loop - Menu and Choices
        while True:
            choice = features.validate_menu_choice(is_admin)
            
            match choice:
                case "0":
                    print("Exiting program...")
                    exit(0)
                case "1":
                    features.list_tables_and_select(db_connection)
                    continue
                case "2":                    
                    res = features.search_by_id(db_connection)
                    continue                    
                case "3":
                    features.statistics_menu(db_connection)
                    continue
                case "4":
                    features.run_admin_query(db_connection)
            
            input("\nPress Enter to return to the menu...")

    except Exception as e:
        print(f"\nA runtime error occurred: {e}")

    finally:
        #Ensure connection closes regardless of what happens when running the program (even if errors occur and the program crashes)
        db_connection.close()

if __name__ == "__main__":
    run_app()