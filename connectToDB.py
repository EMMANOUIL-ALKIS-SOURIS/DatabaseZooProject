import sqlite3

databasepath = "C:\\Users\\manos_pldjgff\\Documents\\7thSemester\\Databases\\Project\\Database\\VersionsWithData\\ZooProjectDataBaseDataV2.db"

def connect_to_db():

    try:
        connection = sqlite3.connect(databasepath)
        #print("Successfully connected to the database")
        
        return connection #returns a connection object
    
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        
        return None