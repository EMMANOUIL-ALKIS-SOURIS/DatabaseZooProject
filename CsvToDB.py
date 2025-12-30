import sqlite3
import csv
import os

# --- Configuration ---
DATABASE_NAME = "C:\\Users\\manos_pldjgff\\Documents\\7thSemester\\Databases\\Project\\Database\\BaseScript\\ZooProjectDataBase.db"
CSV_DIRECTORY = "./TableCSVs"

IMPORT_ORDER = [
    'Employee', 'Food', 'Cleaner', 'Guide', 'Security', 'Vet', 'Trainer',
    'Keeper', 'Stock', 'Keeper_Maintains_Habitat', 'Location_In_Storage',
    'Is_Stored', 'Ticket', 'Individual', 'Groupp', 'Area', 'Security_Overwatches_Area', 'Tick_ref_Area',
    'Habitat', 'Diet', 'Diet_Contains_Food', 'Shift', 'Contract', 
    'Cleaner_Cleans_Area', 'Animal', 'Consumes', 'Vet_Treats_Animal', 'Event'

]

def import_csv_to_sqlite(table_name, csv_file_path, conn):
    """Reads a CSV and inserts its data into the specified table."""
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            
            # Create a placeholder string for the SQL INSERT statement:
            # e.g., '?, ?, ?, ?' for 4 columns
            placeholders = ', '.join(['?'] * len(header))
            
            # Construct the full SQL INSERT statement
            sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            
            # Prepare data: convert all empty strings to None (NULL in SQL)
            data_to_insert = [
                [None if item == '' else item for item in row] 
                for row in reader
            ]

            # Execute the bulk insertion
            cursor = conn.cursor()
            cursor.executemany(sql, data_to_insert)
            conn.commit()
            print(f"Successfully inserted {len(data_to_insert)} rows into {table_name}")
            return True

    except sqlite3.OperationalError as e:
        print(f"Error inserting data into {table_name}: {e}")
        print("Check if table schema matches CSV columns/types.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred for {table_name}: {e}")
        return False

# --- Main Execution ---
def run_bulk_import():
    conn = None
    sucessful_imports = 0
    total_tables = len(IMPORT_ORDER)
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DATABASE_NAME)
        
        print(f"Starting bulk import into {DATABASE_NAME}...")

        for table_name in IMPORT_ORDER:
            csv_file = os.path.join(CSV_DIRECTORY, f'{table_name}.csv')
            
            if os.path.exists(csv_file):
                print(f"\nProcessing file: {table_name}.csv")
                if import_csv_to_sqlite(table_name, csv_file, conn):
                    sucessful_imports += 1
            else:
                print(f"Warning: CSV file not found for table {table_name}")

        print(f"\nSuccessfully imported {sucessful_imports} of {total_tables} tables")

    except Exception as e:
        print(f"A connection error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == '__main__':
    run_bulk_import()