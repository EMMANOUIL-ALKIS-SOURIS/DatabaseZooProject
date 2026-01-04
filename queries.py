#Predetermined quries for direct refrences of each table/entity 
#These refrences refer to the directly connected tables (via foreign keys) of each entity/table

#Ticket table
def getTicketQueries():

    #Search for details of the employee (guide) associated with the ticket (if included in the ticket),
    #if it was a group ticket or an individual ticket and the areas the specific ticket grants access to
    return{
        "Details of Guide included": "SELECT e.Employee_ID, e.Surname, e.Name, e.Email FROM Ticket t JOIN Employee e ON t.Employee_ID = e.Employee_ID WHERE Ticket_ID = ?",
        "Ticket Type": 
        """
        SELECT 
	        CASE 
		        WHEN ind.Ticket_ID IS NOT NULL THEN 'Individual Ticket'
                WHEN grp.Ticket_ID IS NOT NULL THEN 'Group (Number of people: ' || grp.Num_of_people || ')'
                ELSE 'Unknown Type'
            END AS 'Ticket Type'
        FROM Ticket t
        LEFT JOIN Individual ind ON t.Ticket_ID = ind.Ticket_ID
        LEFT JOIN Groupp grp ON t.Ticket_ID = grp.Ticket_ID
        WHERE t.Ticket_ID = ?
        """,
        "Access to Areas": "SELECT a.Area_ID, a.Animal_Category FROM Tick_ref_area t JOIN Area a ON t.Area_ID = a.Area_ID WHERE Ticket_ID = ?"
    }

#Event table
def getEventQueries():

    #Search for details on the animal and employee associated with the event + the habitat where the event took place
    return{        
        "Animal of Event": "SELECT e.Animal_ID, a.Species, a.Name FROM Event e JOIN Animal a ON e.Animal_ID = a.Animal_ID WHERE e.Event_ID = ?",
        "Habitat Event took place in": "SELECT h.Habitat_ID,h.Type, h.Position FROM Event e JOIN Animal a ON e.Animal_ID = a.Animal_ID JOIN Habitat h ON a.Habitat_ID = h.Habitat_ID WHERE e.Event_ID = ?",        
        "Employee one Event": 
        """
        SELECT em.Employee_ID,
            CASE 
                WHEN k.Employee_ID IS NOT NULL THEN 'Keeper'
                WHEN v.Employee_ID IS NOT NULL THEN 'Vet'
                WHEN t.Employee_ID IS NOT NULL THEN 'Trainer'
                WHEN s.Employee_ID IS NOT NULL THEN 'Security'
                WHEN c.Employee_ID IS NOT NULL THEN 'Cleaner'
                WHEN g.Employee_ID IS NOT NULL THEN 'Guide'
                ELSE 'General Staff'
            END AS Role, em.Name, em.Surname, em.Email
        FROM Event e
        JOIN Employee em ON e.Employee_ID = em.Employee_ID
        LEFT JOIN Keeper k ON em.Employee_ID = k.Employee_ID
        LEFT JOIN Vet v ON em.Employee_ID = v.Employee_ID
        LEFT JOIN Trainer t ON em.Employee_ID = t.Employee_ID
        LEFT JOIN Security s ON em.Employee_ID = s.Employee_ID
        LEFT JOIN Cleaner c ON em.Employee_ID = c.Employee_ID
        LEFT JOIN Guide g ON em.Employee_ID = g.Employee_ID
        WHERE e.Event_ID = ?
        """
    }

#Animal table
def getAnimalQueries():

    #Search for the trainer of the animal, the vet that treats the animal, the diet that it follows, the habitat it lives in, the
    #keeper responsible for that habitat and any events that the animal was refrenced in in the last month
    return{
        "Animal's Trainer": "SELECT a.Employee_ID, e.Surname, e.Name, e.Email FROM Animal a JOIN Employee e  ON a.Employee_ID = e.Employee_ID WHERE a.Animal_ID = ?",
        "Animal's Vet": "SELECT v.Employee_ID, e.Surname, e.Name, e.Email FROM Vet_Treats_Animal v JOIN Employee e ON v.Employee_ID = e.Employee_ID WHERE v.Animal_ID = ?",
        "Animal's Diet and Alergies": "SELECT a.Diet_ID, d.Allergies FROM Animal a JOIN Diet d ON a.Diet_ID = d.Diet_ID WHERE a.Animal_ID = ?",
        "Animal's Habitat": "SELECT a.Habitat_ID, h.Type, h.Position FROM Animal a JOIN Habitat h ON a.Habitat_ID = h.Habitat_ID WHERE a.Animal_ID = ?",
        "Habitat's Keeper": 
        """
        SELECT k.Employee_ID, e.Surname, e.Name, e.Email 
        FROM Animal a 
        JOIN Habitat h ON a.Habitat_ID = h.Habitat_ID 
        JOIN Keeper_Maintains_Habitat k ON h.Habitat_ID = k.Habitat_ID 
        JOIN Employee e ON k.Employee_ID = e.Employee_ID 
        WHERE a.Animal_ID = ?
        """,
        "Recent Events (last month) involving the Animal": "SELECT e.Event_ID, e.Description, e.Date FROM Event e WHERE e.Animal_ID = ? AND e.Date >= DATE('now', '-1 month')"
    }

#Contract table
def getContractQueries():

    #Search for the employee's details (name, surname, AFM and contact info) associated with the contract and where he's currently working
    return{        
        "Employee details":
        """
        SELECT em.Employee_ID, em.Surname, em.Name, em.AFM, em.Email, em.Phone,
	        CASE 
		        WHEN k.Employee_ID IS NOT NULL THEN 'Currently employed as Keeper'
                WHEN v.Employee_ID IS NOT NULL THEN 'Currently employed as Vet'
                WHEN t.Employee_ID IS NOT NULL THEN 'Currently employed as Trainer'
                WHEN s.Employee_ID IS NOT NULL THEN 'Currently employed as Security'
                WHEN cl.Employee_ID IS NOT NULL THEN 'Currently employed as Cleaner'
                WHEN g.Employee_ID IS NOT NULL THEN 'Currently employed as Guide'
                ELSE 'General Staff'
            END AS Role
        FROM Contract c
        JOIN Employee em ON c.Employee_ID = em.Employee_ID
        LEFT JOIN Keeper k ON em.Employee_ID = k.Employee_ID
        LEFT JOIN Vet v ON em.Employee_ID = v.Employee_ID
        LEFT JOIN Trainer t ON em.Employee_ID = t.Employee_ID
        LEFT JOIN Security s ON em.Employee_ID = s.Employee_ID
        LEFT JOIN Cleaner cl ON em.Employee_ID = cl.Employee_ID
        LEFT JOIN Guide g ON em.Employee_ID = g.Employee_ID
        WHERE c.Contract_ID = ?
        """,
        "Current Assignments":  
        """
        SELECT 
	        CASE 
		        WHEN t.Employee_ID IS NOT NULL THEN '\n' || 'Animal ID: ' || a.Animal_ID
                WHEN k.Employee_ID IS NOT NULL THEN '\n' || 'Habitat ID: ' || kmh.Habitat_ID
                WHEN s.Employee_ID IS NOT NULL THEN '\n' || 'Area ID: ' || soa.Area_ID
                WHEN cl.Employee_ID IS NOT NULL THEN '\n' || 'Area ID: ' || cca.Area_ID
                WHEN v.Employee_ID IS NOT NULL THEN '\n' || 'Animal ID: ' || vta.Animal_ID
                WHEN g.Employee_ID IS NOT NULL THEN 'Responsible for all Guest Services'
                ELSE 'General Administration'
	        END as Assignment
        FROM Contract c
        LEFT JOIN Trainer t ON c.Employee_ID = t.Employee_ID
        LEFT JOIN Animal a ON t.Employee_ID = a.Employee_ID
        LEFT JOIN Keeper k ON c.Employee_ID = k.Employee_ID
        LEFT JOIN Keeper_Maintains_Habitat kmh ON k.Employee_ID = kmh.Employee_ID
        LEFT JOIN Security s ON c.Employee_ID = s.Employee_ID
        LEFT JOIN Security_Overwatches_Area soa ON s.Employee_ID = soa.Employee_ID
        LEFT JOIN Cleaner cl ON c.Employee_ID = cl.Employee_ID
        LEFT JOIN Cleaner_Cleans_Area cca ON cl.Employee_ID = cca.Employee_ID
        LEFT JOIN Vet v ON c.Employee_ID = v.Employee_ID
        LEFT JOIN Vet_Treats_Animal vta ON v.Employee_ID = vta.Employee_ID
        LEFT JOIN Guide g ON c.Employee_ID = g.Employee_ID
        WHERE c.Contract_ID = ?
        """
    }

#Diet table
def getDietQueries():

    #Search for which foods make up the diet, the foods' quantity, units and frequency and which animals follow it
    return{
        "Diet Composition (Food-Qty-Freq (Min/Day))": 
        """
        SELECT f.Food_ID, f.Name, dcf.Quantity, s.Unit_Type, dcf.Feeding_Freq 
        FROM Diet_Contains_Food dcf 
        JOIN Food f ON dcf.Food_ID = f.Food_ID 
        JOIN Stock s ON dcf.Food_ID = s.Food_ID 
        WHERE dcf.Diet_ID = ?
        """,
        "Animals following this Diet": "SELECT Animal_ID, Species, Name FROM Animal WHERE Diet_ID = ?"
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
    #Guide -> Services they provide
    return{        
        "Employee's current role":
        """
        SELECT
	        CASE 
                WHEN k.Employee_ID IS NOT NULL THEN 'Keeper'
                WHEN v.Employee_ID IS NOT NULL THEN 'Vet'
                WHEN t.Employee_ID IS NOT NULL THEN 'Trainer'
                WHEN s.Employee_ID IS NOT NULL THEN 'Security'
                WHEN cl.Employee_ID IS NOT NULL THEN 'Cleaner'
                WHEN g.Employee_ID IS NOT NULL THEN 'Guide'
                ELSE 'General Staff'
            END AS Role
        FROM Employee e
        LEFT JOIN Keeper k ON e.Employee_ID = k.Employee_ID
        LEFT JOIN Vet v ON e.Employee_ID = v.Employee_ID
        LEFT JOIN Trainer t ON e.Employee_ID = t.Employee_ID
        LEFT JOIN Security s ON e.Employee_ID = s.Employee_ID
        LEFT JOIN Cleaner cl ON e.Employee_ID = cl.Employee_ID
        LEFT JOIN Guide g ON e.Employee_ID = g.Employee_ID
        WHERE e.Employee_ID = ?
        """,
        "Current Assignments":  
        """
        SELECT 
	        CASE 
		        WHEN t.Employee_ID IS NOT NULL THEN '\n' || 'Animal ID: ' || a.Animal_ID
                WHEN k.Employee_ID IS NOT NULL THEN '\n' || 'Habitat ID: ' || kmh.Habitat_ID
                WHEN s.Employee_ID IS NOT NULL THEN '\n' || 'Area ID: ' || soa.Area_ID
                WHEN cl.Employee_ID IS NOT NULL THEN '\n' || 'Area ID: ' || cca.Area_ID
                WHEN v.Employee_ID IS NOT NULL THEN '\n' || 'Animal ID: ' || vta.Animal_ID
                WHEN g.Employee_ID IS NOT NULL THEN 'Responsible for all Guest Services'
                ELSE 'General Administration'
	        END as Assignment
        FROM Employee e
        LEFT JOIN Trainer t ON e.Employee_ID = t.Employee_ID
        LEFT JOIN Animal a ON t.Employee_ID = a.Employee_ID
        LEFT JOIN Keeper k ON e.Employee_ID = k.Employee_ID
        LEFT JOIN Keeper_Maintains_Habitat kmh ON k.Employee_ID = kmh.Employee_ID
        LEFT JOIN Security s ON e.Employee_ID = s.Employee_ID
        LEFT JOIN Security_Overwatches_Area soa ON s.Employee_ID = soa.Employee_ID
        LEFT JOIN Cleaner cl ON e.Employee_ID = cl.Employee_ID
        LEFT JOIN Cleaner_Cleans_Area cca ON cl.Employee_ID = cca.Employee_ID
        LEFT JOIN Vet v ON e.Employee_ID = v.Employee_ID
        LEFT JOIN Vet_Treats_Animal vta ON v.Employee_ID = vta.Employee_ID
        LEFT JOIN Guide g ON e.Employee_ID = g.Employee_ID
        WHERE e.Employee_ID = ?
        """,
        "Weekly Schedule (Day-Start-End)":
        """
        SELECT '\n' || Day, Time_Start, Time_End 
        FROM Shift 
        WHERE Employee_ID = ?
        ORDER BY CASE 
            WHEN Day = 'Monday' THEN 1
            WHEN Day = 'Tuesday' THEN 2
            WHEN Day = 'Wednesday' THEN 3
            WHEN Day = 'Thursday' THEN 4
            WHEN Day = 'Friday' THEN 5
            WHEN Day = 'Saturday' THEN 6
            WHEN Day = 'Sunday' THEN 7
        END
        """,
        "Contract History (ContractID-Salary-//Start-//End)": "SELECT Contract_ID, Salary, '//' || Date_Start, '//' ||  Date_End FROM Contract WHERE Employee_ID = ? ORDER BY Date_Start DESC"
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

    #Search for habitats contained in the area and employees (Security & Cleaner) assigned to it
    return{
        "Habitats contained in Area": "SELECT Habitat_ID, Position, Type, Status FROM Habitat WHERE Area_ID = ?",
        "Security that overwatches Area": "SELECT s.Employee_ID, e.Surname, e.Name, e.Phone FROM Security_Overwatches_Area s JOIN Employee e ON s.Employee_ID = e.Employee_ID WHERE s.Area_ID = ?",
        "Cleaner that cleans Area": "SELECT c.Employee_ID, e.Surname, e.Name, e.Email, e.Phone FROM Cleaner_Cleans_Area c JOIN Employee e ON c.Employee_ID = e.Employee_ID WHERE c.Area_ID = ?"

    }

#Habitat table
def getHabitatQueries():

    #Search for the area that the habitat is in, the animals living in the habitat and the keeper responsible for it
    return{
        "Area where habitat is located at": "SELECT h.Area_ID, a.Animal_Category FROM Habitat h JOIN Area a ON h.Area_ID = a.Area_ID WHERE Habitat_ID = ?",
        "Animals in Habitat": "SELECT Animal_ID, Species, Name FROM Animal WHERE Habitat_ID = ?",
        "Keeper that maintains Habitat": "SELECT k.Employee_ID, e.Surname, e.Name, e.Email FROM Keeper_Maintains_Habitat k JOIN Employee e ON k.Employee_ID = e.Employee_ID WHERE k.Habitat_ID = ?"
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

