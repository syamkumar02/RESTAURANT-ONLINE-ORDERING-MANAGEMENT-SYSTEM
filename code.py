import pyodbc
from prettytable import PrettyTable

# Database connection parameters
server = 'localhost'
database = 'RestMgmt'
username = 'sa'
password = 'Siddhu@1831'
driver = 'SQL Server'

# Connect to the database
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

try:
    # Query data from the database
    query = '''
            SELECT Customers.CustomerName, Orders.OrderDate, Restaurants.RestaurantName, Menus.ItemName, Orders.Quantity, Orders.Amount, Payments.PaymentMode
            FROM Orders
            INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
            INNER JOIN Restaurants ON Orders.RestaurantID = Restaurants.RestaurantID
            INNER JOIN Menus ON Orders.RestaurantID = Menus.RestaurantID AND Orders.Quantity > 0
            LEFT JOIN Payments ON Orders.OrderID = Payments.OrderID
            ORDER BY Orders.OrderDate DESC;
            '''
    
    cursor.execute(query)

    # Create a PrettyTable instance
    report_table = PrettyTable()
    report_table.field_names = ["Customer", "OrderDate", "Restaurant", "Item", "Quantity", "Amount", "PaymentMode"]

    # Add data to the table
    for row in cursor.fetchall():
        report_table.add_row([row.CustomerName, row.OrderDate, row.RestaurantName, row.ItemName, row.Quantity, row.Amount, row.PaymentMode])

    # Print the table
    print("Report:")
    print(report_table)

    # Save data to a text file
    with open('report.txt', 'w') as file:
        file.write("Report:\n")
        file.write(str(report_table))

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
