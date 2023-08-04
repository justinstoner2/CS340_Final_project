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
nav.Bar('top',[
    nav.Item('index','index'),
    nav.Item('customers','customers'),
    nav.Item('campaigns','campaigns'),
    nav.Item('channels','channels'),
    nav.Item('inventory','inventory'),
    nav.Item('products','products'),
    nav.Item('sales','sales'),
    nav.Item('saleItem','saleItem')
])

# Routes 

@app.route('/')
def index():
    return render_template("index.j2")

@app.route('/customers')
def customers():
    query = "SELECT Customers.customerID, customerName, customerEmail, totalRevenue, (SELECT count(DISTINCT saleID) from Sales WHERE Customers.customerID = Sales.customerID) as salesCount FROM Customers JOIN (SELECT Sales.customerID, sum(quantity * productPrice) as totalRevenue FROM Sales JOIN SaleItems ON Sales.saleID = SaleItems.saleID JOIN Products ON SaleItems.productID = SaleItems.productID GROUP BY Sales.customerID) as t1 ON Customers.customerID = t1.customerID;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("customers.j2", customers=results)

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
        return render_template("campaigns.j2", campaigns = results)

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

@app.route('/inventory')
def inventory():
    query = "SELECT inventoryID,  productID, dateAdded, quantity, ((SELECT productPrice from Products WHERE Inventory.productID = Products.productID) * quantity) as totalValue FROM Inventory;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("inventory.j2", inventory=results)

# PRODUCTS
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

@app.route('/saleItems')
def saleItems():
    query = "SELECT saleItemID,  saleID, productID, quantity, ((SELECT productPrice from Products WHERE SaleItems.productID = Products.productID) * quantity) as totalLineItemCost FROM SaleItems;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("saleItems.j2", saleItems= results)

@app.route('/sales')
def sales():
    query = "SELECT Sales.saleID,  customerID, saleDate, totalSaleValue FROM Sales JOIN (SELECT saleID, (sum(quantity * productPrice)) as totalSaleValue FROM SaleItems JOIN Products ON SaleItems.productID = Products.productID GROUP BY saleID) as t1 ON Sales.saleID = t1.saleID;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("sales.j2", sales = results)


# Delete route for Campaigns
@app.route('/delete_campaign/<int:campaignID>')
def delete_campaign(campaignID):
    # query to delete a campaign row via caidinput passed from the delete button modal
    query = "DELETE FROM Campaigns WHERE campaignID = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(campaignID,))
    
    # return to campaign page
    return redirect("/campaigns")

# Update route for Campaigns
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

# Listener


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9858)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 