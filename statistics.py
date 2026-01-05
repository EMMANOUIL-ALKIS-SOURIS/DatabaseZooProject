from tabulate import tabulate          

#Financial Statistics
def get_salary_expenses_report():
    
    #Fetches the total monthly salary expenses and breaks it down by employee roles.
    #This also shows where the budget is being allocated across different roles.

    title = "Monthly Salary Expenses (General & By Role)"

    query = """
        SELECT Role, SUM(Salary) AS Total_Monthly_Spend, COUNT(Employee_ID) AS Staff_Count
        FROM (
            SELECT 'Keeper' as Role, c.Salary, c.Employee_ID FROM Contract c JOIN Keeper k ON c.Employee_ID = k.Employee_ID
            UNION ALL
            SELECT 'Vet' as Role, c.Salary, c.Employee_ID FROM Contract c JOIN Vet v ON c.Employee_ID = v.Employee_ID
            UNION ALL
            SELECT 'Security' as Role, c.Salary, c.Employee_ID FROM Contract c JOIN Security s ON c.Employee_ID = s.Employee_ID
            UNION ALL
            SELECT 'Trainer' as Role, c.Salary, c.Employee_ID FROM Contract c JOIN Trainer t ON c.Employee_ID = t.Employee_ID
            UNION ALL
            SELECT 'Guide' as Role, c.Salary, c.Employee_ID FROM Contract c JOIN Guide g ON c.Employee_ID = g.Employee_ID
            UNION ALL
            SELECT 'Cleaner' as Role, c.Salary, c.Employee_ID FROM Contract c JOIN Cleaner cl ON c.Employee_ID = cl.Employee_ID
        ) as CombinedSalaries
        GROUP BY Role
        
        UNION ALL
        
        SELECT 'TOTAL' as Role, SUM(Salary), COUNT(Employee_ID)
        FROM Contract;
    """

    return title, query, ["Employee Role", "Total Monthly Spend ($)", "Staff Count"]

def get_ticket_revenue_report():
    
    #Fetches ticket sales revenue statistics broken down by ticket type and by area/category. 
    #It sorts the ticket sales by showing the highest revenue-generating combinations of ticket type, class and area first.
    #It also provides a grand total revenue figure.

    title = "Monthly Revenue: Ticket Types and Area Performance"

    query = """
        SELECT 
            COALESCE(a.Animal_Category, 'Unassigned') AS Area_Category,
            CASE 
                WHEN g.Ticket_ID IS NOT NULL THEN 'Group'
                WHEN i.Ticket_ID IS NOT NULL THEN 'Individual'
                ELSE 'Other'
            END AS Ticket_Class,
            t.Ticket_Type,
            SUM(t.Price + t.Extra_Cost) AS Total_Revenue,
            COUNT(t.Ticket_ID) AS Sold_Count
        FROM Ticket t
        LEFT JOIN Tick_ref_area tra ON t.Ticket_ID = tra.Ticket_ID
        LEFT JOIN Area a ON tra.Area_ID = a.Area_ID
        LEFT JOIN Groupp g ON t.Ticket_ID = g.Ticket_ID
        LEFT JOIN Individual i ON t.Ticket_ID = i.Ticket_ID
        GROUP BY Area_Category, Ticket_Class, t.Ticket_Type
        
        UNION ALL
        
        SELECT '---', '---', 'GRAND TOTAL', SUM(Price + Extra_Cost), COUNT(Ticket_ID)
        FROM Ticket
        ORDER BY Total_Revenue DESC;
    """

    return title, query, ["Area / Category", "Class", "Type", "Revenue ($)", "Qty"]

#Area, Habitat and Animal Statistics
def get_habitat_density_report():

    #Fetches each habitat's animal density and sorts the Areas they belong to by the highest number of animals present.

    title = "Habitat Occupancy and Animal Density"

    query = """
        SELECT 
            COALESCE(a.Animal_Category, 'N/A') as Area,
            h.Habitat_ID,
            h.Type as Habitat_Type,
            COUNT(an.Animal_ID) as Animal_Count,
            h.Status
        FROM Habitat h
        LEFT JOIN Animal an ON h.Habitat_ID = an.Habitat_ID
        LEFT JOIN Area a ON h.Area_ID = a.Area_ID
        GROUP BY h.Habitat_ID, a.Animal_Category, h.Type, h.Status
        ORDER BY Animal_Count DESC;
    """

    #Useful because it helps the admins identify which habitats are underutilized or overcrowded,
    #while also retrieving each habitat's status and providing insights into the distribution of animals 
    #across different areas of the zoo.

    return title, query, ["Area", "Habitat ID", "Habitat Type", "Animal Count", "Status"]

def get_vet_workload_report():

    #Fetched the number of medical interventions each veterinarian has performed
    #It also identifies which animal species are most frequently treated.

    title = "Veterinary Workload & Animal Health Overview"

    query = """
        SELECT 
            e.Employee_ID,
            e.Surname AS Vet_Name,
            a.Species,
            a.Animal_ID,
            a.Name AS Animal_Name,
            COUNT(vta.Animal_ID) AS Treatment_Count
        FROM Vet v
        JOIN Employee e ON v.Employee_ID = e.Employee_ID
        JOIN Vet_Treats_Animal vta ON v.Employee_ID = vta.Employee_ID
        JOIN Animal a ON vta.Animal_ID = a.Animal_ID
        GROUP BY e.Employee_ID, a.Species, a.Name
        ORDER BY Treatment_Count DESC, Vet_Name ASC;
    """

    #Useful because it helps zoo management monitor veterinarian workloads,
    #but most importantly it highlights which animal species may require more medical attention,
    #indicating potential health issues within those populations and or bad habitat conditions.

    return title, query, ["Employee ID", "Veterinarian", "Species", "Animal ID", "Animal Name", "Treatments"]

def get_area_popularity_density_report():

    #Fetches the popularity of each area based on visitor counts (tickets sold) relative to the number of animals housed there.

    title = "Area Popularity & Crowd Density (Animals vs. Visitors)"

    query = """
        SELECT 
            a.Animal_Category AS Area_Name,
            COALESCE(Visitor_Counts.Total_Tickets, 0) AS Visitor_Count,
            COALESCE(Animal_Counts.Total_Animals, 0) AS Animal_Count,
            CASE 
                WHEN COALESCE(Animal_Counts.Total_Animals, 0) = 0 THEN 'N/A'
                ELSE ROUND(CAST(COALESCE(Visitor_Counts.Total_Tickets, 0) AS FLOAT) / Animal_Counts.Total_Animals, 2)
            END AS Visitors_Per_Animal
        FROM Area a
        LEFT JOIN (
            SELECT Area_ID, COUNT(Ticket_ID) AS Total_Tickets 
            FROM Tick_ref_area 
            GROUP BY Area_ID
        ) AS Visitor_Counts ON a.Area_ID = Visitor_Counts.Area_ID
        LEFT JOIN (
            SELECT h.Area_ID, COUNT(an.Animal_ID) AS Total_Animals
            FROM Habitat h
            JOIN Animal an ON h.Habitat_ID = an.Habitat_ID
            GROUP BY h.Area_ID
        ) AS Animal_Counts ON a.Area_ID = Animal_Counts.Area_ID
        ORDER BY Visitors_Per_Animal DESC;
    """

    #Useful because it helps zoo management understand which areas attract the most visitors relative to their animal populations.
    #High Visitors + Low Animals = High-Efficiency / "Star" Area.
    #Low Visitors + High Animals = Low-Visibility Area.

    return title, query, ["Area Category", "Visitors", "Animal Pop.", "Visitor/Animal Ratio"]

#Food Statistics
def get_inventory_report():
    
    #Fetches food items that are running low based on their stock (and unit type) in the Stock table and therefore need ordering.
    
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

def get_food_consumption_stats():

    #Fetches the most 'popular' food items based on how many animal diets they are part of
    #and the total quantity required per feeding cycle.

    title = "Food Consumption Rate and Popularity"

    query = """
        SELECT 
            f.Name, 
            COUNT(dcf.Diet_ID) AS Animal_Count, 
            SUM(dcf.Quantity) AS Total_Required_Qty,
            f.Category
        FROM Food f
        JOIN Diet_Contains_Food dcf ON f.Food_ID = dcf.Food_ID
        GROUP BY f.Food_ID, f.Name, f.Category
        ORDER BY Animal_Count DESC, Total_Required_Qty DESC;
    """

    return title, query, ["Food Item", "Diet Count", "Total Qty/Feeding", "Category"]

#Full Zoo Report - All statistics
def full_zoo_report(connection):
    
    statFunction(connection, 0) #Financial statistics
    
    statFunction(connection, 1) #Area, Habitat, Animal statistics

    statFunction(connection, 2)  #Food statistics

#General statistic function handler
def statFunction(connection, statFuncFlag):

    financialStatFunctions = [get_salary_expenses_report, get_ticket_revenue_report]

    areaHabitatAnimalStatFunctions = [get_habitat_density_report, get_vet_workload_report, get_area_popularity_density_report]

    foodStatFunctions = [get_inventory_report, get_food_consumption_stats]

    statFunctions = [
        financialStatFunctions,
        areaHabitatAnimalStatFunctions,
        foodStatFunctions
    ]
    statSelected = statFunctions[statFuncFlag]
    
    cursor = connection.cursor()

    for func in statSelected:
        # query, head = func(connection)
        title, query, head = func()

        try:            
            cursor.execute(query)
            res = cursor.fetchall()

        except Exception as e:
            print(f"An error occurred while fetching data for {title}: {e}")
            res = None

        printStats(title, res, head)

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

    print(f"\n{'='*50}\n")
