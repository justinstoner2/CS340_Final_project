-- phpMyAdmin SQL Dump
-- version 5.2.1-1.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 16, 2023 at 09:55 PM
-- Server version: 10.6.12-MariaDB-log
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ProjStep2_grp34`
-- This SQL file will import all of the databases and sample data for project step 2, group 34.
-- Please import this file to evaluate our report. 
-- Group 34 members: Sheng Feng, Justin Stoner

-- --------------------------------------------------------

--
-- Table structure for table `Campaigns`
--

CREATE TABLE `Campaigns` (
  `campaignID` int(11) NOT NULL,
  `channelID` int(11),
  `startDate` date NOT NULL,
  `endDate` date,
  `productID` int(11)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `Campaigns`
--

INSERT INTO `Campaigns` (`campaignID`, `channelID`, `startDate`, `endDate`, `productID`) VALUES
(1, 1, '2023-05-15', '2023-06-30', 2),
(2, 1, '2023-06-01', '2023-06-15', 3),
(3, 2, '2023-02-01', '2023-02-28', 1),
(4, 2, '2023-04-15', '2023-04-15', 3);

-- --------------------------------------------------------

--
-- Table structure for table `Channels`
--

CREATE TABLE `Channels` (
  `channelID` int(11) NOT NULL,
  `channelName` varchar(50) NOT NULL,
  `channelEmail` varchar(50) NOT NULL,
  `rate` decimal(19,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `Channels`
--

INSERT INTO `Channels` (`channelID`, `channelName`, `channelEmail`, `rate`) VALUES
(1, 'Koolguy', 'kguy@gmail.com', 1000.00),
(2, 'Supermom', 's_mom@yahoo.com.', 5000.00),
(3, 'Influencer', 'influ@outlook.com', 10000.00);

-- --------------------------------------------------------

--
-- Table structure for table `Customers`
--

CREATE TABLE `Customers` (
  `customerID` int(11) NOT NULL,
  `customerName` varchar(50) NOT NULL,
  `customerEmail` varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `Customers`
--

INSERT INTO `Customers` (`customerID`, `customerName`, `customerEmail`) VALUES
(1, 'Bill', 'bill@gmail.com'),
(2, 'Dale', 'dale@yahoo.com'),
(3, 'Hank', 'hank@outlook.com');

-- --------------------------------------------------------

--
-- Table structure for table `Inventory`
--

CREATE TABLE `Inventory` (
  `inventoryID` int(11) NOT NULL,
  `productID` int(11),
  `dateAdded` date NOT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `Inventory`
--

INSERT INTO `Inventory` (`inventoryID`, `productID`, `dateAdded`, `quantity`) VALUES
(1, 1, '2023-07-10', 500),
(2, 1, '2023-07-16', 750),
(3, 2, '2023-05-10', 200),
(4, 2, '2023-06-05', 400),
(5, 3, '2023-07-01', 300);

-- --------------------------------------------------------

--
-- Table structure for table `Products`
--

CREATE TABLE `Products` (
  `productID` int(11) NOT NULL,
  `productName` varchar(50) NOT NULL,
  `productPrice` decimal(19,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `Products`
--

INSERT INTO `Products` (`productID`, `productName`, `productPrice`) VALUES
(1, 'Fan', 20.00),
(2, 'Scarf', 100.00),
(3, 'Tie', 40.00);

-- --------------------------------------------------------

--
-- Table structure for table `SaleItems`
--

CREATE TABLE `SaleItems` (
  `saleItemID` int(11) NOT NULL,
  `saleID` int(11),
  `productID` int(11),
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `SaleItems`
--

INSERT INTO `SaleItems` (`saleItemID`, `saleID`, `productID`, `quantity`) VALUES
(1, 1, 2, 50),
(2, 1, 1, 250),
(3, 2, 2, 600),
(4, 3, 3, 1000);

-- --------------------------------------------------------

--
-- Table structure for table `Sales`
--

CREATE TABLE `Sales` (
  `saleID` int(11) NOT NULL,
  `customerID` int(11),
  `saleDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `Sales`
--

INSERT INTO `Sales` (`saleID`, `customerID`, `saleDate`) VALUES
(1, 1, '2023-05-15'),
(2, 1, '2023-06-01'),
(3, 2, '2023-02-10'),
(4, 2, '2023-04-05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Campaigns`
--
ALTER TABLE `Campaigns`
  ADD PRIMARY KEY (`campaignID`),
  ADD KEY `channelID` (`channelID`),
  ADD KEY `productID` (`productID`);

--
-- Indexes for table `Channels`
--
ALTER TABLE `Channels`
  ADD PRIMARY KEY (`channelID`);

--
-- Indexes for table `Customers`
--
ALTER TABLE `Customers`
  ADD PRIMARY KEY (`customerID`);

--
-- Indexes for table `Inventory`
--
ALTER TABLE `Inventory`
  ADD PRIMARY KEY (`inventoryID`),
  ADD KEY `productID` (`productID`);

--
-- Indexes for table `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`productID`);

--
-- Indexes for table `SaleItems`
--
ALTER TABLE `SaleItems`
  ADD PRIMARY KEY (`saleItemID`),
  ADD KEY `saleID` (`saleID`),
  ADD KEY `productID` (`productID`);

--
-- Indexes for table `Sales`
--
ALTER TABLE `Sales`
  ADD PRIMARY KEY (`saleID`),
  ADD KEY `customerID` (`customerID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Campaigns`
--
ALTER TABLE `Campaigns`
  MODIFY `campaignID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Channels`
--
ALTER TABLE `Channels`
  MODIFY `channelID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Customers`
--
ALTER TABLE `Customers`
  MODIFY `customerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Inventory`
--
ALTER TABLE `Inventory`
  MODIFY `inventoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Products`
--
ALTER TABLE `Products`
  MODIFY `productID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `SaleItems`
--
ALTER TABLE `SaleItems`
  MODIFY `saleItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Sales`
--
ALTER TABLE `Sales`
  MODIFY `saleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Campaigns`
--
ALTER TABLE `Campaigns`
  ADD CONSTRAINT `Campaigns_ibfk_1` FOREIGN KEY (`channelID`) REFERENCES `Channels` (`channelID`) ON DELETE SET NULL,
  ADD CONSTRAINT `Campaigns_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `Products` (`productID`) ON DELETE CASCADE;

--
-- Constraints for table `Inventory`
--
ALTER TABLE `Inventory`
  ADD CONSTRAINT `Inventory_ibfk_1` FOREIGN KEY (`productID`) REFERENCES `Products` (`productID`) ON DELETE SET NULL;

--
-- Constraints for table `SaleItems`
--
ALTER TABLE `SaleItems`
  ADD CONSTRAINT `SaleItems_ibfk_1` FOREIGN KEY (`saleID`) REFERENCES `Sales` (`saleID`) ON DELETE SET NULL,
  ADD CONSTRAINT `SaleItems_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `Products` (`productID`) ON DELETE SET NULL;

--
-- Constraints for table `Sales`
--
ALTER TABLE `Sales`
  ADD CONSTRAINT `Sales_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `Customers` (`customerID`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
