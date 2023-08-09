from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request 
from flask_navigation import Navigation
import database.db_connector as db
import os

# Configuration

app = Flask(__name__)
nav = Navigation(app)
db_connection = db.connect_to_database()
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

#initializing Navigations
#nav.Bar('top',[
#    nav.Item('index','index'),
 #   nav.Item('customers','customers'),
  #  nav.Item('campaigns','campaigns'),
   # nav.Item('channels','channels'),
    #nav.Item('inventory','inventory'),
    #nav.Item('products','products'),
    #nav.Item('sales','sales'),
    #nav.Item('saleItem','saleItem')
#])

# Routes 

@app.route('/')
def index():
    return render_template("index.j2")

#CRUD for Customers
########################################################################################################################################################

#Create and Read
@app.route('/customers', methods = ["POST", "GET"])
def customers():
    if request.method == "POST":
            customerName = request.form["cnameInput"]
            customerEmail = request.form["cemailInput"]

            query = "INSERT INTO Customers(customerName,customerEmail) VALUES(%s,%s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customerName,customerEmail,))
            return redirect("/customers")

    if request.method == "GET":
        query = "SELECT Customers.customerID, customerName, customerEmail, totalRevenue, (SELECT count(DISTINCT saleID) from Sales WHERE Customers.customerID = Sales.customerID) as salesCount FROM Customers JOIN (SELECT Sales.customerID, sum(quantity * productPrice) as totalRevenue FROM Sales JOIN SaleItems ON Sales.saleID = SaleItems.saleID JOIN Products ON SaleItems.productID = SaleItems.productID GROUP BY Sales.customerID) as t1 ON Customers.customerID = t1.customerID;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("customers.j2", customers=results)

########################################################################################################################################################



#CRUD for Campaigns
########################################################################################################################################################

#Create and Read
@app.route('/campaigns', methods = ["POST", "GET"])
def campaigns():

    # used when the user presses the add campaign button
    if request.method == "POST":
            channelID = request.form["chidinput_dd"]
            startDate = request.form["chstartinput"]
            endDate = request.form["chendinput"]
            productID = request.form["pidinput_dd"]

            # basic error handling for when endDate is empty
            if endDate == "":
                query = "INSERT INTO Campaigns (channelID, startDate, productID) VALUES (%s, %s, %s);;" 
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(channelID, startDate, productID,))
            
            else: 
                query = "INSERT INTO Campaigns (channelID, startDate, endDate, productID) VALUES (%s, %s, %s, %s);" 
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(channelID, startDate, endDate, productID,))
        
            # return to product page
            return redirect("/campaigns")
    
    if request.method == "GET":
        query = "SELECT campaignID,  channelID, startDate, endDate, productID, (datediff(endDate, startDate) * (SELECT rate FROM Channels  WHERE Campaigns.channelID = Channels.channelID)) as cost FROM Campaigns;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        query2 = "SELECT channelID, channelName  FROM Channels"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        channel_results = cursor.fetchall()
        return render_template("campaigns.j2", campaigns = results, channels = channel_results)
    

#Update
@app.route('/update_campaign/<int:caidinput>', methods=["Post", "Get"])

def update_campaign(caidinput):
    if request.method == "GET":
        # query to grab the data for the campaign to be updated
        query = "SELECT * FROM Campaigns WHERE campaignID = %s" % (caidinput)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # query to grab channel name data from dropdown
        query2 = "SELECT channelID, channelName  FROM Channels"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        channel_results = cursor.fetchall()
        
        # query to grab product name data from dropdown
        query3 = "SELECT productID, productName  FROM Products"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        product_results = cursor.fetchall()
        
        # render update_people page passing all the query data above
        return render_template("updateCampaign.j2", data = results, channels = channel_results, products = product_results)
    
    if request.method == "POST":

        # grab user form inputs
        #campaignID = request.form["chidinput_dd"]
        channelID = request.form["chidinput_dd"]
        startDate = request.form["chstartinput"]
        endDate = request.form["chendinput"]
        productID = request.form["pidinput_dd"]

    # this mess below accounts for several possible null variataions, for sanity lets default to all fields to blank (vs 0)

        if (channelID == "" and productID == ""):
            query = "UPDATE Campaigns SET channelID = NULL, startDate = %s, endDate = %s, productID = NULL WHERE campaignID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(startDate, endDate, campaignID,))

        elif channelID == "":
            query = "UPDATE Campaigns SET channelID = NULL, startDate = %s, endDate = %s, productID = %s WHERE campaignID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(startDate, endDate, productID, campaignID,))
        elif productID == "":
            query = "UPDATE Campaigns SET channelID = NULL, startDate = %s, endDate = %s, productID = %s WHERE campaignID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(channelID, startDate, endDate, campaignID,))

        else:
            query = "UPDATE Campaigns SET channelID = %s, startDate = %s, endDate = %s, productID =%s WHERE campaignID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(channelID, startDate, endDate, productID, caidinput,))
    # return to campaign page
    return redirect("/campaigns")


# Delete route for Campaigns
@app.route('/delete_campaign/<int:campaignID>')
def delete_campaign(campaignID):
    # query to delete a campaign row via caidinput passed from the delete button modal
    query = "DELETE FROM Campaigns WHERE campaignID = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(campaignID,))
    
    # return to campaign page
    return redirect("/campaigns")
########################################################################################################################################################



#CRUD for Channels
########################################################################################################################################################

#Create and Read
@app.route('/channels', methods = ["POST", "GET"])
def channels():
    
    # Create function for channels, relies on modal for input raw data
    if request.method == "POST":
        # used when the user presses the add channel button
        channelName = request.form["chnameinput"]
        channelEmail = request.form["chemailinput"]
        rate = request.form["chrateinput"]
        
        query = "INSERT INTO Channels (channelName, channelEmail, rate) VALUES (%s, %s, %s);" 
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(channelName, channelEmail, rate,))
        # return to channel page
        return redirect("/channels")
    
    if request.method == "GET":
        query = "SELECT * FROM Channels;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("channels.j2",channels = results)

# Channel Delete
@app.route("/delete_channel/<int:channelID>")
def delete_channel(channelID):
    query = "DELETE FROM Channels WHERE channelID = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(channelID,))
    return redirect("/channels")

########################################################################################################################################################



#CRUD for Inventory
########################################################################################################################################################

#Create and Read
@app.route('/inventory', methods = ["POST", "GET"])
def inventory():
    if request.method == "POST":
            productID = request.form["ipinput"]
            dateAdded = request.form["idainput"]
            quantity = request.form["iqinput"]

            query = "INSERT INTO Inventory (productID, dateAdded, quantity) VALUES (%s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection,query=query, query_params=(productID,dateAdded,quantity,))
            return redirect("/inventory")

    if request.method == "GET":
        query = "SELECT inventoryID,  productID, dateAdded, quantity, ((SELECT productPrice from Products WHERE Inventory.productID = Products.productID) * quantity) as totalValue FROM Inventory;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        query3 = "SELECT productID, productName  FROM Products"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        product_results = cursor.fetchall()

        return render_template("inventory.j2", inventory=results, products = product_results)

#Delete
@app.route("/delete_inventory/<int:inventoryID>")
def delete_inventory(inventoryID):
    query = "DELETE FROM Inventory WHERE inventoryID = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(inventoryID,))
    return redirect("/inventory")

########################################################################################################################################################


#CRUD for Products
########################################################################################################################################################

# Create and Read
@app.route('/products', methods = ["POST", "GET"])
def products():
    
    # Create for products, relies on modal for input raw data
    if request.method == "POST":
        # used when the user presses the add product button
        productName = request.form["pnameinput"]
        productPrice = request.form["ppriceinput"]
        
        query = "INSERT INTO Products (productName, productPrice) VALUES (%s, %s);" 
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(productName, productPrice,))
        print("productName"+productName)
        # return to product page
        return redirect("/products")

    if request.method == "GET":
        query = "SELECT * FROM Products;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        
        return render_template("products.j2", products=results)
    


# Product Delete
@app.route("/delete_product/<int:productID>")
def delete_product(productID):
    query = "DELETE FROM Products WHERE productID = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(productID,))
    return redirect("/products")

########################################################################################################################################################

#CRUD for SaleItems
########################################################################################################################################################

#Create and Read
@app.route('/saleItems', methods = ["POST", "GET"])
def saleItems():
    if request.method == "POST":
        saleID = request.form["saidinput_dd"]
        productID = request.form["pidinput_dd"]
        quantity = request.form["siqtyinput"]
        print( saleID)

        query="INSERT INTO SaleItems (saleID, productID, quantity) VALUES (%s, %s, %s);"
        cursor = db.execute_query(db_connection=db_connection,query=query,query_params=(saleID,productID,quantity,))
        return redirect("/saleItems")

    if request.method == "GET":
        query = "SELECT saleItemID,  saleID, productID, quantity, ((SELECT productPrice from Products WHERE SaleItems.productID = Products.productID) * quantity) as totalLineItemCost FROM SaleItems;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        query2 = "SELECT CONCAT(customerName, ' ', saleDate, ' ') as SaleName, saleID FROM Sales as t1 JOIN Customers as t2 WHERE t1.customerID = t2.customerID;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        sale_results = cursor.fetchall()
        

        query3 = "SELECT productID, productName  FROM Products"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        product_results = cursor.fetchall()
        

        return render_template("saleItems.j2", saleItems= results, products = product_results, sales = sale_results)

########################################################################################################################################################


#CRUD for Sales
########################################################################################################################################################

#Create and Read
@app.route('/sales', methods = ["POST", "GET"])
def sales():
    if request.method == "POST":
        customerID = request.form["scustomerID_input"]
        salesDate = request.form["ssalesDate_input"]

        query="INSERT INTO Sales (customerID, saleDate) VALUES (%s, %s);"
        cursor = db.execute_query(db_connection=db_connection,query=query,query_params=(customerID,salesDate,))
        return redirect("/sales")
    
    if request.method == "GET":
        query = "SELECT Sales.saleID,  customerID, saleDate, totalSaleValue FROM Sales JOIN (SELECT saleID, (sum(quantity * productPrice)) as totalSaleValue FROM SaleItems JOIN Products ON SaleItems.productID = Products.productID GROUP BY saleID) as t1 ON Sales.saleID = t1.saleID;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        query2 ="SELECT DISTINCT customerName, customerID FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        customer_results = cursor.fetchall()
        print(customer_results)
        return render_template("sales.j2", sales = results, customers = customer_results)
########################################################################################################################################################


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9859)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 