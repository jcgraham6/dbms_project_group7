CREATE TABLE Vendor (
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(10),
    email VARCHAR(50),
    address VARCHAR (250)
    PRIMARY KEY (vendorID) VARCHAR(50),
);

CREATE TABLE Inventory_Order ( 
    commodityID VARCHAR(25) NOT NULL,
    product_name VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    vendorID VARCHAR(50),
    PRIMARY KEY inventory_orderID VARCHAR(50),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);

CREATE TABLE Contract (
    storeID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50),
    order_frequency VARCHAR(50),
    delivery_schedule VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE,
    pricing DECIMAL(10, 2),
    PRIMARY KEY contractID VARCHAR(50),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);

CREATE TABLE Delivery (
    storeID VARCHAR(50) NOT NULL,
    vendorID VARCHAR(50),
    commodityID VARCHAR(50),
    orderdate DATE NOT NULL,
    expected_time TIME,
    discrepancy TEXT,
    received_status VARCHAR(50),
    PRIMARY KEY deliveryID VARCHAR(50),
    FOREIGN KEY (vendorID) REFERENCES Vendor(vendorID)
);


