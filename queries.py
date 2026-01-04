#Predetermined quries for direct refrences of each table/entity 
#These refrences refer to the directly connected tables (via foreign keys) of each entity/table

#Ticket table
def getTicketQueries():

    #Search for details of the employee (guide) associated with the ticket (if included in the ticket) 
    #and if it was a group ticket or an individual ticket
    return{


    }

#Event table
def getEventQueries():

    #Search for details on the animal and employee (guide) associated with the event
    return{


    }

#Animal table
def getAnimalQueries():

    #Search for the vet that treats the animal, the diet that it follows, the habitat it lives in, the
    #keeper responsible for that habitat and any events that the animal was refrenced in in the last month
    return{


    }

#Contract table
def getContractQueries():

    #Search for the employee's details (name, surname, AFM and contact info) associated with the contract and where he's currently working
    return{


    }

#Diet table
def getDietQueries():

    #Search for which foods make up the diet, the foods' quantity, units and frequency and which animals follow it
    return{


    }

#Employee table
def getEmployeeQueries():
    
    #Search for the employee's contract/contracts and their weekly schedule/shifts
    #Based on their role:
    #Keeper -> Habitats they maintain
    #Vet -> Animals they treat
    #Trainer -> Animals they train
    #Security -> Areas they overwatch
    #Cleaner -> Areas they clean
    #Guide -> How many tickets they were included in in the last month
    return{


    }


#Food table
def getFoodQueries():

    #Search where food is stored, how much of it remains in stock and in what diets it's used in
    return{ 
        "Stored in storage position" : "SELECT Aisle, Row, Shelf FROM Is_stored WHERE Food_ID = ?",
        "Remaining quantity" : "SELECT Remaining_Quantity, Unit_Type FROM Stock WHERE Food_ID = ?",
        "Used in diets": "SELECT Diet_ID FROM Diet_Contains_Food WHERE Food_ID = ?"
    }

#Area table
def getAreaQueries():

    #Search for habitats contained in the area and employees (Security & Cleaner) assigned to it (++ maybe how many tickets were sold for this area)
    return{


    }

#Habitat table
def getHabitatQueries():

    #Search for animals living in the habitat and the keeper responsible for it
    return{


    }


#Dynamically searching the references of each entity type
def referenceSearchQueries(table_name, entity_id, cursor, queries_dictionary):

    print(f"\n=== Associated References of {table_name} with ID: {entity_id} ===\n")

    for name, query in queries_dictionary.items():
        try:
            cursor.execute(query, (entity_id,))
            results = cursor.fetchall()

            if results:
                #Extracting the elements from each tuple
                
                values = []

                for r in results:
                    
                    if len(r) > 1:
                        rowString = "-".join([str(val) for val in r])
                        values.append(rowString)
                    else:
                        values.append(str(r[0]))

                print(f"-> {name}: {', '.join(values)}")    
            else:
                print(f"-> {name}: None found")

        except Exception as e:
            print(f"Error fetching {name}: {e}")