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
mysql = MySQL(app)

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

@app.route('/customers', methods = ["POST", "GET"])
def customers():
    if request.method == 'GET':
        query = "SELECT * FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("customers.j2", customers=results)

@app.route('/deleteCustomer/<int:id>')
def deleteCustomers(id):
    
    query = "DELETE FROM Customers WHERE customerID = '%s';"
    cursor = db.execute_query(db_connection = db_connection, query=query)
    results = cursor.fet

    return redirect("/customers")
@app.route('/campaigns',methods = ["POST", "GET"])
def campaigns():
     # Create function for campaigns, relies on modal for input raw data
    if request.method == "POST":
        # used when the user presses the add campaign button
        print("post is working")
        
        print("insert is working")
        channelID = request.form["chidinput_dd"]
            
        startDate = request.form["chstartinput"]
        endDate = request.form["chendinput"]
        productID = request.form["pidinput_dd"]

        # this mess below accounts for several possible null variataions, for sanity lets default to all fields to blank (vs 0)
        if channelID == "" and productID == "" and endDate == "":
            query = "INSERT INTO Campaigns (startDate) VALUES (%s);" 
            cursor = db.execute_query(db_connection=db_connection, query=query)
    
        elif channelID == "" and productID == "":
            query = "INSERT INTO Campaigns (startDate, endDate) VALUES (%s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query) 

        elif channelID == "":
            query = "INSERT INTO Campaigns (startDate, endDate, productID) VALUES (%s, %s, %s);" 
            cursor = db.execute_query(db_connection=db_connection, query=query)

        elif productID == "":
            query = "INSERT INTO Campaigns (channelID, startDate, endDate) VALUES (%s, %s, %s);" 
            cursor = db.execute_query(db_connection=db_connection, query=query)
    
        else: 
            query = "INSERT INTO Campaigns (channelID, startDate, endDate, productID) VALUES (%s, %s, %s, %s);" 
            print("productID"+productID)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(channelID,startDate,endDate,productID))
            
            

            
        
        # return to product page
        print("about to redirect")
        return redirect("/campaigns")
    
    if request.method == "GET":
        query = "SELECT campaignID,  channelID, startDate, endDate, productID, (datediff(endDate, startDate) * (SELECT rate FROM Channels  WHERE Campaigns.channelID = Channels.channelID)) as cost FROM Campaigns;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("campaigns.j2", campaigns = results)


@app.route('/channels', methods = ["POST", "GET"])
def channels():
    query = "SELECT * FROM Channels;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("channels.j2",channels = results)

@app.route('/inventory', methods = ["POST", "GET"])
def inventory():
    query = "SELECT * FROM Inventory;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("inventory.j2", inventory=results)

@app.route('/products', methods = ["POST", "GET"])
def products():
    query = "SELECT * FROM Products;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("products.j2", products=results)

@app.route('/saleItems', methods = ["POST", "GET"])
def saleItems():
    query = "SELECT * FROM SaleItems;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("saleItems.j2", saleItems= results)

@app.route('/sales', methods = ["POST", "GET"])
def sales():
    query = "SELECT * FROM Sales;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("sales.j2", sales = results)

@app.route("/delete_campaign/<int:campaignID>")
def delete_campaign(campaignID):
    query = "DELETE FROM Campaigns WHERE campaignID = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(campaignID,))
    return redirect("/campaigns")
# Listener


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9854)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 