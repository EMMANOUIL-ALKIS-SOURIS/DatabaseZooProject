import queries
import sqlite3

def print_menu(adminFlag):

    options = {
        "1": "View/Edit Tables",
        "2": "Search with ID",
    }

    #Features only admins can access are added dynamically when admin mode is activated
    if adminFlag:
        options["3"] = "Statistics (Admin Only)"
        options["4"] = "Send SQL Query (Admin Only)"

    startupInterface = "\tZOO DATABASE TERMINAL INTERFACE"

    startupMessage = "\nPlease select one of the following options:\n"

    menu_body = [f"{k}. {v}" for k, v in sorted(options.items())]
    menu_body.append("0. Exit")

    print("="*50)
    print(startupInterface)
    print("="*50)
    print(startupMessage)
    print("\n".join(menu_body))
    
    #Return both the user input and the valid keys for validation
    return input("\nWaiting for input: ").strip(), list(options.keys()) + ["0"]


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


#Main Menu View/Edit + Send Queries (Vaggelis)
def get_table_row_count(cursor, table_name):
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        result = cursor.fetchone()
        return result[0] if result else 0
    except:
        return 0

def get_foreign_keys(db_connection, table_name):
    """
    Returns a dictionary of Foreign Keys for a table.
    Format: { 'ColumnName': ('ParentTable', 'ParentColumn') }
    """
    cursor = db_connection.cursor()
    fk_dict = {}
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    rows = cursor.fetchall()
    for row in rows:
        parent_table = row[2]
        child_col = row[3]
        parent_col = row[4]
        fk_dict[child_col] = (parent_table, parent_col)
    return fk_dict

# --- 1. INSPECT TABLE FUNCTION ---
def view_table_content(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description]
        
        print(f"\n--- VIEWING: {table_name} ---")
        
        # Headers
        header_str = " | ".join([f"{col:<15}" for col in column_names])
        print(header_str)
        print("-" * len(header_str))
        
        if not rows:
            print("(Table is empty)")
            return

        # Rows
        for row in rows:
            display_row = [str(item) if item is not None else "NULL" for item in row]
            row_str = " | ".join([f"{item:<15}" for item in display_row])
            print(row_str)
        print("\n")
            
    except sqlite3.Error as e:
        print(f"Error reading table: {e}")

# --- ASSIGN ROLE ---
def assign_employee_role(db_connection, employee_id):
    """Asks the user to assign a role to the newly created employee."""
    print("\n" + "*"*50)
    print(f"   ASSIGN ROLE TO EMPLOYEE {employee_id}")
    print("*"*50)
    print("1. Cleaner")
    print("2. Keeper")
    print("3. Security")
    print("4. Trainer")
    print("5. Vet")
    print("6. Guide")
    print("0. Skip (No specific role)")
    print("-" * 50)
    
    choice = input("Select a role (0-6): ").strip()
    
    role_map = {
        '1': 'Cleaner',
        '2': 'Keeper',
        '3': 'Security',
        '4': 'Trainer',
        '5': 'Vet',
        '6': 'Guide'
    }
    
    if choice in role_map:
        target_table = role_map[choice]
        print(f"\n>> Opening form for {target_table}...")
        add_row_to_table(db_connection, target_table, fixed_values={'Employee_ID': employee_id})
    else:
        print("\nSkipping role assignment.")

# --- 2. ADD ROW FUNCTION ---
def add_row_to_table(db_connection, table_name, fixed_values=None, skip_role_assignment=False):
    if fixed_values is None:
        fixed_values = {}

    special_tables = ['Employee', 'Cleaner', 'Keeper', 'Security', 'Guide', 'Vet', 'Trainer']
    cursor = db_connection.cursor()

    # --- PART A: SPECIAL LOGIC FOR EMPLOYEES ---
    if table_name in special_tables and table_name != 'Employee':
        
        # a. Recursive Call Fix (Base Employee Check)
        if 'Employee_ID' in fixed_values:
            target_id = fixed_values['Employee_ID']
            cursor.execute("SELECT 1 FROM Employee WHERE Employee_ID = ?", (target_id,))
            if not cursor.fetchone():
                print(f"\n[!] You are creating a {table_name} with ID {target_id}.")
                print(f"    However, no base Employee profile exists for ID {target_id} yet.")
                print(f">> Creating base Employee profile now...")
                
                add_row_to_table(
                    db_connection, "Employee", 
                    fixed_values={'Employee_ID': target_id}, 
                    skip_role_assignment=True 
                )
                
                cursor.execute("SELECT 1 FROM Employee WHERE Employee_ID = ?", (target_id,))
                if not cursor.fetchone():
                    print("[!] Employee creation failed. Cannot proceed.")
                    return None

        # b. Manual Entry Logic
        elif 'Employee_ID' not in fixed_values:
            print(f"\n[!] You are adding a {table_name}, which requires a valid Employee profile.")
            print("1. Create a NEW Employee first (Recommended)")
            print("2. Enter an EXISTING Employee ID manually")
            print("0. Cancel")
            
            sub_choice = input("Select option: ").strip()
            
            if sub_choice == '1':
                print(f"\n>> Redirecting to Employee creation...")
                new_emp_id = add_row_to_table(db_connection, "Employee")
                
                if new_emp_id:
                    cursor.execute(f"SELECT 1 FROM {table_name} WHERE Employee_ID = ?", (new_emp_id,))
                    if cursor.fetchone():
                        print(f"\n[!] {table_name} entry already exists. Done.")
                        return new_emp_id
                    
                    print(f"\n>> Employee {new_emp_id} created. Now finishing {table_name} entry...")
                    fixed_values['Employee_ID'] = new_emp_id
                else:
                    return None
            
            elif sub_choice == '2':
                while True:
                    existing_id = input("Enter the existing Employee ID (or '0' to Cancel): ").strip()
                    if existing_id == '0': return None
                    
                    cursor.execute("SELECT 1 FROM Employee WHERE Employee_ID = ?", (existing_id,))
                    if not cursor.fetchone():
                        print(f"\n[ERROR] Employee ID {existing_id} does NOT exist.")
                        continue
                    
                    cursor.execute(f"SELECT 1 FROM {table_name} WHERE Employee_ID = ?", (existing_id,))
                    if cursor.fetchone():
                        print(f"\n[ERROR] Employee {existing_id} is ALREADY a {table_name}.")
                        continue

                    print(f"[OK] Employee {existing_id} found. Proceeding...")
                    fixed_values['Employee_ID'] = existing_id
                    break
            else:
                return None 

    # --- PART B: STANDARD ENTRY WITH SMART FK LOGIC ---
    fk_constraints = get_foreign_keys(db_connection, table_name)
    
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"\n--- ADDING NEW ROW TO: {table_name} ---")
        if not fixed_values:
            print("Instructions: Type 'CANCEL' to abort.")
        
        new_values = []
        captured_pk_value = None 

        for col in columns:
            col_name = col[1]
            col_type = col[2]
            is_pk = col[5]
            
            # Use Fixed Values
            if col_name in fixed_values:
                val = fixed_values[col_name]
                print(f"-> Automatically setting {col_name} to: {val}")
                new_values.append(val)
                if is_pk: captured_pk_value = val
                continue
            
            valid_input = False
            final_val = None
            
            while not valid_input:
                prompt = f"Enter {col_name} ({col_type})"
                if is_pk:
                    prompt += " (PK)"
                    try:
                        if "INT" in col_type.upper():
                            cursor.execute(f"SELECT MAX({col_name}) FROM {table_name}")
                            max_val = cursor.fetchone()[0]
                            next_val = (int(max_val) + 1) if max_val is not None else 1
                            prompt += f" [Suggested: {next_val}]"
                    except: pass
                
                user_input = input(f"{prompt}: ").strip()
                if user_input.upper() == 'CANCEL':
                    print("\n[!] Operation cancelled.")
                    return None
                
                # --- FK CHECK ---
                if col_name in fk_constraints and user_input != "":
                    parent_table, parent_col = fk_constraints[col_name]
                    cursor.execute(f"SELECT 1 FROM {parent_table} WHERE {parent_col} = ?", (user_input,))
                    if cursor.fetchone():
                        final_val = user_input
                        valid_input = True
                    else:
                        print(f"\n[!] ID '{user_input}' not found in '{parent_table}'.")
                        print(f"1 -> Create new entry in {parent_table} with ID {user_input}")
                        print("2 -> Retry")
                        
                        sel = input("Select: ").strip()
                        if sel == '1':
                            print(f"\n>>> JUMPING TO {parent_table} CREATION >>>")
                            new_parent_id = add_row_to_table(db_connection, parent_table, fixed_values={parent_col: user_input})
                            
                            if new_parent_id:
                                print(f"\n<<< RETURNING TO {table_name} FORM <<<")
                                # [FIX] Use user_input (the ID we typed) instead of return value (which might be rowid)
                                final_val = user_input  
                                valid_input = True
                            else:
                                print(f"\n<<< RETURNED (No entry created) <<<")
                        else:
                            continue 
                else:
                    final_val = user_input
                    valid_input = True

            if final_val == "" and is_pk:
                new_values.append(None)
            elif final_val == "" and table_name == "Ticket":
                # Special Case: For Ticket table, empty input means NULL (None)
                new_values.append(None)
            else:
                new_values.append(final_val)
                if is_pk: captured_pk_value = final_val

        # INSERT
        placeholders = ", ".join(["?" for _ in new_values])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(query, new_values)
        db_connection.commit()
        print(f"\n[SUCCESS] Row added to {table_name}!")
        
        if captured_pk_value is None or captured_pk_value == "":
             captured_pk_value = cursor.lastrowid

        if table_name == "Employee" and not skip_role_assignment:
            cursor.close()
            assign_employee_role(db_connection, captured_pk_value)
            
        return captured_pk_value

    except sqlite3.IntegrityError as e:
        print(f"\n[ERROR] Constraint failed: {e}")
        db_connection.rollback()
        return None
    except sqlite3.Error as e:
        print(f"\n[ERROR] Database error: {e}")
        db_connection.rollback()
        return None
    finally:
        try: cursor.close()
        except: pass

# --- 3. DELETE ROW FUNCTION ---
def delete_row_from_table(db_connection, table_name):
    cursor = db_connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    pk_columns = [col for col in columns if col[5] > 0]
    pk_columns.sort(key=lambda x: x[5])
    pk_names = [col[1] for col in pk_columns]
    
    if not pk_names:
        print(f"\n[ERROR] Table '{table_name}' appears to have NO Primary Key defined.")
        return

    print(f"\n--- DELETING ROW FROM: {table_name} ---")
    print("Please provide the Primary Key(s) to identify the row.")
    
    pk_values = []
    for pk_col in pk_names:
        val = input(f"Enter value for {pk_col}: ").strip()
        if val.upper() == 'CANCEL':
            print("Operation cancelled.")
            return
        pk_values.append(val)
    
    where_clause = " AND ".join([f"{name} = ?" for name in pk_names])
    query = f"SELECT rowid, * FROM {table_name} WHERE {where_clause}"
    cursor.execute(query, pk_values)
    row_data = cursor.fetchone()
    
    if not row_data:
        print(f"\n[ERROR] No record found.")
        return
        
    rowid = row_data[0]
    actual_data = row_data[1:]
    
    print("\n" + "!"*40)
    print("WARNING: YOU ARE ABOUT TO DELETE THIS RECORD:")
    
    col_names = [col[1] for col in columns]
    for name, val in zip(col_names, actual_data):
        print(f"{name:<15}: {val}")
        
    print("-" * 40)
    confirm = input("Are you sure? (Type 'YES' to delete): ").strip().upper()
    
    if confirm == 'YES':
        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?", (rowid,))
            db_connection.commit()
            print(f"\n[SUCCESS] Record deleted.")
        except sqlite3.Error as e:
            print(f"\n[ERROR] Cannot delete: {e}")
            db_connection.rollback()
    else:
        print("\n[!] Deletion cancelled.")

# --- 4. EDIT ROW FUNCTION ---
def edit_row_in_table(db_connection, table_name):
    cursor = db_connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    pk_columns = [col for col in columns if col[5] > 0]
    pk_columns.sort(key=lambda x: x[5])
    pk_names = [col[1] for col in pk_columns]
    
    if not pk_names:
        print(f"\n[ERROR] Table '{table_name}' appears to have NO Primary Key.")
        return

    print(f"\n--- EDITING ROW IN: {table_name} ---")
    print("Please provide the Primary Key(s).")
    
    pk_values = []
    for pk_col in pk_names:
        val = input(f"Enter value for {pk_col}: ").strip()
        if val.upper() == 'CANCEL': return
        pk_values.append(val)
    
    where_clause = " AND ".join([f"{name} = ?" for name in pk_names])
    query = f"SELECT rowid, * FROM {table_name} WHERE {where_clause}"
    
    cursor.execute(query, pk_values)
    row_data = cursor.fetchone()
    
    if not row_data:
        print(f"\n[ERROR] No record found.")
        return
        
    perform_edit(db_connection, table_name, columns, pk_names, row_data[0], row_data[1:])

def perform_edit(db_connection, table_name, columns, pk_names, rowid, current_data):
    print(f"\n[OK] Record found. Editing mode.")
    print("Instructions: Type NEW value, press ENTER to SKIP, 'CANCEL' to abort.")
    
    fk_constraints = get_foreign_keys(db_connection, table_name)
    new_values = []
    cursor = db_connection.cursor()
    protect_pk = (len(pk_names) == 1)

    for index, col in enumerate(columns):
        col_name = col[1]
        col_type = col[2]
        current_val = current_data[index]
        
        if col_name in pk_names and protect_pk:
            print(f" -> {col_name}: {current_val} (PK - Protected)")
            new_values.append(current_val)
            continue
            
        valid_input = False
        final_val = current_val
        
        while not valid_input:
            prompt = f"Change {col_name} ({col_type}) [Current: {current_val}]"
            user_input = input(f"{prompt}: ").strip()
            
            if user_input.upper() == 'CANCEL':
                print("\n[!] Edit cancelled.")
                return 
            
            if user_input.upper() == 'SKIP' or user_input == "":
                final_val = current_val
                valid_input = True
            
            elif col_name in fk_constraints:
                parent_table, parent_col = fk_constraints[col_name]
                cursor.execute(f"SELECT 1 FROM {parent_table} WHERE {parent_col} = ?", (user_input,))
                if cursor.fetchone():
                    final_val = user_input
                    valid_input = True
                else:
                    print(f"\n[!] ID '{user_input}' not found in '{parent_table}'.")
                    print(f"1 -> Create new entry in {parent_table} with ID {user_input}")
                    print("2 -> Retry")
                    sel = input("Select: ").strip()
                    
                    if sel == '1':
                        print(f"\n>>> JUMPING TO {parent_table} CREATION >>>")
                        new_id = add_row_to_table(db_connection, parent_table, fixed_values={parent_col: user_input})

                        if new_id:
                            print(f"\n<<< RETURNING TO EDIT <<<")
                            # [FIX] Use user_input here too
                            final_val = user_input 
                            valid_input = True
                        else:
                            print("Creation cancelled.")
                    else:
                         continue 
            else:
                final_val = user_input
                valid_input = True

        new_values.append(final_val)

    set_clause = ", ".join([f"{col[1]} = ?" for col in columns])
    query = f"UPDATE {table_name} SET {set_clause} WHERE rowid = ?"
    new_values.append(rowid)
    
    try:
        cursor.execute(query, new_values)
        db_connection.commit()
        print(f"\n[SUCCESS] Row updated successfully!")
    except sqlite3.Error as e:
        print(f"\n[ERROR] Update failed: {e}")
        db_connection.rollback()


# --- 5. MENU ---
def table_operations_menu(db_connection, table_name):
    while True:
        print(f"\n" + "="*40)
        print(f"   MENU FOR TABLE: {table_name}")
        print("="*40)
        print("1. Inspect Table (View All)")
        print("2. Add Row")
        print("3. Edit Row")
        print("4. Delete Row")
        print("0. Back to Table List")
        print("-" * 40)
        
        choice = input("Select an action: ").strip()
        
        if choice == '1':
            view_table_content(db_connection.cursor(), table_name)
            input("Press Enter to continue...")
        elif choice == '2':
            add_row_to_table(db_connection, table_name)
            input("Press Enter to continue...")
        elif choice == '3':
            edit_row_in_table(db_connection, table_name)
            input("Press Enter to continue...")
        elif choice == '4':
            delete_row_from_table(db_connection, table_name)
            input("Press Enter to continue...")
        elif choice == '0':
            break
        else:
            print("Invalid selection.")


#-- Main Menu-->1 --
def list_tables_and_select(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]
    
    if not tables:
        print("No tables found.")
        return

    while True:

        #Print table menu
        print("\n" + "="*60)
        print(f"{'#':<4} {'Table Name':<40} | {'Row Count'}")
        print("-" * 60)
        for index, table_name in enumerate(tables):
            count = get_table_row_count(cursor, table_name)
            num_str = f"{index + 1})"
            print(f"{num_str:<4} {table_name:<40} | {count}")
        print("="*60)

        choice = input("\nEnter table number (or 0 to main menu): ").strip()
        
        if choice.isdigit():
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(tables):
                selected_table = tables[choice_idx]
                table_operations_menu(db_connection, selected_table)
            elif choice_idx == -1: return
            else: print("Invalid number selection.")
        else: print("Invalid input.")


#-- Main Menu-->4 --
def run_admin_query(db_connection):
    cursor = db_connection.cursor()
    print("\n" + "="*50)
    print("   ADMINISTRATOR SQL CONSOLE")
    print("="*50)
    print("INSTRUCTIONS:")
    print("1. Type or Paste your query below.")
    print("2. When finished, type 'GO' on a new line and press Enter.")
    print("3. Type 'CANCEL' to exit without running.")
    print("-" * 50)

    query_buffer = []
    
    # --- Multi-line Input Loop ---
    while True:
        prompt = "SQL > " if not query_buffer else "    > "
        line = input(prompt)

        # Check for the stop signal
        if line.strip().upper() == 'GO':
            break
        if line.strip().upper() == 'CANCEL':
            print("Query cancelled.")
            return

        query_buffer.append(line)

    # Join all lines into one string
    full_query = "\n".join(query_buffer)

    if not full_query.strip():
        print("Empty query. Returning.")
        return

    # --- Execute ---
    try:
        cursor.execute(full_query)
        
        # Check if this was a SELECT query (returns data) or action (INSERT/UPDATE)
        if cursor.description:
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            
            print(f"\n[SUCCESS] Query executed. {len(rows)} rows returned.")
            print("-" * 60)
            
            # Print Header
            header = " | ".join([f"{col:<15}" for col in col_names])
            print(header)
            print("-" * len(header))
            
            # Print Rows
            for row in rows:
                # Handle None values nicely
                clean_row = [str(item) if item is not None else "NULL" for item in row]
                print(" | ".join([f"{item:<15}" for item in clean_row]))
            print("\n")
        else:
            # For UPDATE/DELETE/INSERT
            db_connection.commit()
            print(f"\n[SUCCESS] Statement executed. Rows affected: {cursor.rowcount}")

    except sqlite3.Error as e:
        print(f"\n[SQL ERROR]: {e}")
        db_connection.rollback()
    
    input("Press Enter to continue...")
#End Vaggelis