from tabulate import tabulate          

#Financial Statistics
def financial_statistics(connection):
    #asd
    #print("Financial statistics placeholder")

    return "test", "Financial statistics data", ["Column1", "Column2"]

#Area, Habitat and Animal Statistics
def areaHabitatAnimal_statistics(connection):
    #re
    pass

#Food Statistics
def get_inventory_report(connection):
    
    #Fetches food items that are running low based on their stock in the Stock table and therefore need ordering.
    
    title = "Food Inventory Report - Critical Stock Levels"

    #Unit type list (each unit has its own threshold)
    unit_thresholds = {
        "Bags": 50,
        "Bales": 10,
        "Heads": 60,
        "Kilos": 100,
        "Trays": 50,
        "Units": 40
    }

    case_parts = [f"WHEN s.Unit_Type = '{u}' THEN s.Remaining_Quantity <= {t}" for u, t in unit_thresholds.items()]

    caseStatement = " ".join(case_parts)

    query = f"""
        SELECT f.Name, s.Remaining_Quantity, s.Unit_Type 
        FROM Food f
        JOIN Stock s ON f.Food_ID = s.Food_ID
        WHERE CASE
            {caseStatement}
            ELSE s.Remaining_Quantity < 200
        END
        ORDER BY s.Remaining_Quantity ASC;
    """

    return title, query, ["Food Item", "Remaining", "Unit"]

def statFunction(connection, statFuncFlag):

    financialStatFunctions = [financial_statistics]

    areaHabitatAnimalStatFunctions = [areaHabitatAnimal_statistics]

    foodStatFunctions = [get_inventory_report]

    statFunctions = [
        financialStatFunctions,
        areaHabitatAnimalStatFunctions,
        foodStatFunctions
    ]
    statSelected = statFunctions[statFuncFlag]
    
    cursor = connection.cursor()

    for func in statSelected:
        # query, head = func(connection)
        title, query, head = func(connection)

        try:
            
            cursor.execute(query)
            res = cursor.fetchall()

        except Exception as e:
            print(f"An error occurred while fetching data for {title}: {e}")
            res = None

        printStats(title, res, head)

def full_zoo_report(connection):
    
    statFunction(connection, 0) #Financial statistics
    
    statFunction(connection, 1) #Area, Habitat, Animal statistics

    statFunction(connection, 2)  #Food statistics

#General print method
def printStats(title, results, headersList):
    
    print(f"\n{'='*5} STATISTIC: {title.upper()} {'='*5}")

    if not results:
        print("No data available for this statistic.")
        return

    if isinstance(results, str):
        #If results is just a string
        print(results)
    else:
        print(tabulate(results, headers=headersList, tablefmt="psql"))

    print(f"{'='*50}\n")
