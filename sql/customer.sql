CREATE TABLE customer (
    custID varchar(50),
    primary key (custID)
);

CREATE TABLE non_member (
    custID varchar(50),
    primary key (custID),
    foreign key (custID) references customer(custID)
);

CREATE TABLE member (
    custID varchar(50),
    startDate date,
    expDate date,
    loyaltyPoints decimal(10,2),
    primary key (custID),
    foreign key (custID) references customer(custID)
);

CREATE TABLE cart(
    custID varchar(50),
    commodityID varchar(10),
    quantity int,
    add_date date,
    primary key (custID, commodityID),
    foreign key (custID) references customer(custID) on delete cascade
);

CREATE TABLE orders(
    orderID varchar(10),
    order_date date,
    delivery_type varchar(10)CHECK (delivery_type IN ('standard', 'express', 'pickup')),
    primary key (orderID)
);

CREATE TABLE order_items(
    orderID varchar(10),
    commodityID varchar(10),
    quantity int CHECK (quantity>0),
    name varchar(50),
    primary key (orderID, commodityID),
    foreign key (orderID) references orders(orderID) on delete cascade
);

CREATE TABLE payment_regist(
    custID varchar(50),
    cardID varchar(10),
    card_type varchar(10),
    primary key (custID, cardID),
    foreign key (custID) references customer(custID) on delete cascade
);

CREATE TABLE paid(
    custID varchar(50),
    cardID varchar(10),
    orderID varchar(10),
    pay_status varchar(10),
    primary key (custID, cardID, orderID),
    foreign key (custID, cardID) references payment_regist(custID, cardID),
    foreign key (orderID) references orders(orderID)
);

CREATE TABLE checkout(
    custID varchar(50),
    orderID varchar(10),
    date_shipped date,
    primary key (custID, orderID),
    foreign key (custID) references customer(custID),
    foreign key (orderID) references orders(orderID)
);

CREATE TABLE Return_Request(
returnID NUMBER PRIMARY KEY, 
orderID varchar(10), 
returnReason CLOB, 
dateCreated DATE, 
status VARCHAR2(50),
custID varchar(50),
FOREIGN KEY(orderID) REFERENCES orders,
FOREIGN KEY (custID) REFERENCES customer(custID)
);

CREATE TABLE Review(
reviewID NUMBER PRIMARY KEY,
commodityID NUMBER,
rating NUMBER NOT NULL,
comment CLOB, 
reviewDate DATE,
FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

CREATE TABLE Account(
createDate DATE, 
phone NUMBER NOT NULL,
password VARCHAR2(50),
email VARCHAR2(50) PRIMARY KEY,
username VARCHAR2(50),
saveditem VARCHAR2(50), 
paypref VARCHAR2(50)
);

CREATE TABLE Subscription(
subscriptionID NUMBER PRIMARY KEY, 
commodityID NUMBER, 
frequency VARCHAR2(50),
status VARCHAR2(50), 
nextdeliverydate DATE,
FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

CREATE TABLE Preferences(
prefID NUMBER PRIMARY KEY, 
prefcategory VARCHAR2(50)NOT NULL, 
dietaryrestric VARCHAR2(50), 
prefbrands VARCHAR2(50)
);

CREATE TABLE Messages(
messageID NUMBER PRIMARY KEY, 
content CLOB NOT NULL, 
"date" DATE NOT NULL
);

CREATE TABLE Message_Type(
messageType VARCHAR2(255),
messageID NUMBER,
PRIMARY KEY (messageID, messageType),
FOREIGN KEY (messageID) REFERENCES Messages(messageID) ON DELETE CASCADE
);

CREATE TABLE browse(
browse_date DATE,
custID VARCHAR(50),
commodityID NUMBER,
PRIMARY KEY (custID, commodityID), 
FOREIGN KEY (custID) REFERENCES customer(custID),
FOREIGN KEY (commodityID) REFERENCES commodity_store(commodityID)
);

CREATE TABLE setup(
start_date DATE, 
subsciptionID NUMBER,
custID varchar(10),
PRIMARY KEY (custID, subscriptionID),
FOREIGN KEY (custID) REFERENCES Member(custID),
FOREIGN KEY (subscriptionID) REFERENCES Subscription(subscriptionID)
);

CREATE TABLE leaves(
custID VARCHAR(10),
reviewID NUMBER,
PRIMARY KEY(custID, reviewID),
FOREIGN KEY (custID) REFERENCES Member(custID),
FOREIGN KEY(reviewID) REFERENCES Review(reviewID)
);

CREATE TABLE login(
custID VARCHAR(10),
email VARCHAR2(50),
PRIMARY KEY(custID, email),
FOREIGN KEY(custID) REFERENCES Member(custID),
FOREIGN KEY(email) REFERENCES Account(email)
);

CREATE TABLE sets(
custID VARCHAR(10),
prefID NUMBER,
PRIMARY KEY(custID, prefID),
FOREIGN KEY(custID) REFERENCES Member(custID),
FOREIGN KEY(prefID) REFERENCES Preferences(prefID)
);

CREATE TABLE opt_in(
custID VARCHAR(10),
messageID NUMBER,
PRIMARY KEY(custID, messageID),
FOREIGN KEY(custID) REFERENCES Member(custID),
FOREIGN KEY(messageID) REFERENCES Messages(messageID)
);