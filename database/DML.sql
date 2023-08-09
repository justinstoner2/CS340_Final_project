-- CRUD queries for Group34

-- ALL READ OPERATIONS: reads all rows from the relevant table

-- Read all relevant data from Customers table
SELECT customerID, customerName, customerEmail, totalRevenue, salesCount
FROM Customers;

-- Read all relevant data from Products table
SELECT productID,  productName, productPrice
FROM Products;

-- Read all relevant data from Channels table
SELECT channelID,  channelName, channelEmail, rate
FROM Channels;

-- Read all relevant data from Campaigns table
SELECT campaignID,  channelID, startDate, endDate, productID, cost
FROM Campaigns;

-- Read all relevant data from Sales table
SELECT saleID,  customerID, saleDate, totalSaleValue
FROM Sales;

-- Read all relevant data from SaleItems table
SELECT saleItemID,  saleID, productID, quantity, totalLineItemCost
FROM SaleItems;

-- Read all relevant data from Inventory table
SELECT inventoryID,  productID, dateAdded, quantity, totalValue
FROM Inventory;


-- ALL CREATE OPERATIONS: creates a new row in the relevant table 

-- Insert into Customers table
INSERT INTO Customers (customerID, customerName, customerEmail, totalRevenue, salesCount)
VALUES (:cidinput, :cnameinput, :cemailinput, :ctotalrevinput, :csalesinput);

-- Insert into Products table
INSERT INTO Products (productID, productName, productPrice)
VALUES (:pidinput, :pnameinput, :ppriceinput);

-- Insert into Channels table
INSERT INTO Channels (channelID, channelName, channelEmail, rate)
VALUES (:chidinput, :chnameinput, :chemailinput, :chrateinput);

-- Insert into Campaigns table
INSERT INTO Campaigns (campaignID, channelID, startDate, endDate, productID, cost)
VALUES (:caidinput, :chidinput_dd, :chstartinput, :chendinput, :pidinput_dd, :cacostinput);

-- Insert into Sales table
INSERT INTO Sales (saleID, customerID, saleDate, totalSaleValue)
VALUES (:saidinput, :cidinput_dd, :sdateinput, :stotsaleinput);

-- Insert into SaleItems table
INSERT INTO SaleItems (saleItemID, saleID, productID, quantity, totalLineItemCost)
VALUES (:siidinput, :saidinput_dd, :pidinput_dd, :siqtyinput, :sicostinput);

-- Insert into Inventory table
INSERT INTO Inventory (inventoryID, productID, dateAdded, quantity, totalValue)
VALUES (:iidinput, :pidinput_dd, :iaddinput, :iqtyinput, :itotvalinput);


-- ALL DELETE OPERATIONS: deletes a row in the relevant table identified by primary key

-- Delete a record from the Customers table
DELETE FROM Customers
WHERE customerID = cidinput;

-- Delete a record from the Products table
DELETE FROM Products
WHERE productID = pidinput;

-- Delete a record from the Channels table
DELETE FROM Channels
WHERE channelID = chidinput;

-- Delete a record from the Campaigns table
DELETE FROM Campaigns
WHERE campaignID = caidinput;

-- Delete a record from the Sales table
DELETE FROM Sales
WHERE saleID = saidinput;

-- Delete a record from the SaleItems table
DELETE FROM saleItemID
WHERE saleItemID = siidinput;

-- Delete a record from the Inventory table
DELETE FROM Inventory
WHERE inventoryID = iidinput;


-- ALL UPDATE OPERATIONS: updates a row in the relevant table identified by primary key

-- Update a record from the Customers table
UPDATE Customers
SET 
customerName = :cnameinput,
customerEmail = :cemailinput,
totalRevenue = :ctotalrevinput,
salesCount = :csalesinput
WHERE customerID = :cidinput;

-- Update a record from the Products table
UPDATE Products
SET 
productName = :cnameinput,
productPrice = :cemailinput
WHERE productID = :pidinput;

-- Update a record from the Channels table
UPDATE Channels
SET 
channelName = :chnameinput,
channelEmail = :chemailinput,
rate = :chrateinput
WHERE channelID = :chidinput;

-- Update a record from the Campaigns table
UPDATE Campaigns
SET 
channelID = :chidinput_dd,
startDate = :chstartinput,
endDate = :chendinput,
productID = :pidinput_dd,
cost = :cacostinput
WHERE campaignID = :caidinput;

-- Update a record from the Sales table
UPDATE Sales
SET 
customerID = :cidinput_dd,
saleDate = :sdateinput,
totalSaleValue = :stotsaleinput
WHERE saleID = :saidinput;

-- Update a record from the SaleItems table
UPDATE SaleItems
SET 
saleID = :saidinput_dd,
productID = :pidinput_dd,
quantity = :siqtyinput,
totalLineItemCost = :sicostinput
WHERE saleItemID = :siidinput;

-- Update a record from the Inventory table
UPDATE Inventory
SET 
productID = :pidinput_dd,
dateAdded = :iaddinput,
quantity = :iqtyinput,
totalValue = :itotvalinput
WHERE inventoryID = :iidinput;


-- DROPDOWN queries to surface all channels and products by name to website

-- Get all channel names to populate drop down field
SELECT DISTINCT channelName, channelID
FROM Channels;

-- Get all product names to populate drop down field
SELECT DISTINCT productName, productID
FROM Products;

-- Get all customer names to populate drop down field
SELECT DISTINCT customerName, customerID
FROM Customers;

-- Get an aggregate value to represent each sale via the customer name, sale date, and total sale value. 
SELECT CONCAT(customerName, ' ', saleDate, ' ') as salesName, saleID
FROM Sales as t1
JOIN Customers as t2
WHERE t1.customerID = t2.customerID;



