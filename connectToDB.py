import sqlite3

databasepath = "C:\\Users\\manos_pldjgff\\Documents\\7thSemester\\Databases\\Project\\Database\\ZooProjectDataBase.db"

def connect_to_db(db_local_path):

    try:
        connection = sqlite3.connect(db_local_path)
        print("Successfully connected to the database")
        
        return connection #returns a connection object
    
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        
        return None
    
if __name__ == "__main__":
    
    db_connection = connect_to_db(databasepath)

    if db_connection:
        try:
            
            cursor = db_connection.cursor()
        
            cursor.execute("SELECT * FROM Employee;")
            
            print(f"Query results: {cursor.fetchall()}")
        except sqlite3.Error as e:
            
            print(f"An error occurred during query execution: {e}")
        finally:
            
            db_connection.close()
            print("Connection closed.")
    else:
        
        print("Connection failed. Aborting database operations.")
            