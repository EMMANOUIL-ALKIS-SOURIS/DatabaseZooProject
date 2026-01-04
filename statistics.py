from tabulate import tabulate          


def get_inventory_report(connection):
    
    #Fetches food items that are running low based on their stock in the Stock table and therefore need ordering.
    
    cursor = connection.cursor()
    
    query = """
        SELECT f.Name, s.Remaining_Quantity, s.Unit_Type 
        FROM Food f
        JOIN Stock s ON f.Food_ID = s.Food_ID
        WHERE s.Remaining_Quantity < 200
        ORDER BY s.Remaining_Quantity ASC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n--- CRITICAL STOCK LEVELS ---")
    if results:
        print(tabulate(results, headers=["Food Item", "Remaining", "Unit"], tablefmt="psql"))
    else:
        print("All stock levels are sufficient.")

# You can add more functions here (e.g., get_revenue_stats, get_animal_density)