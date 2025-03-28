CREATE TABLE customer (
    custID varchar(10),
    primary key (custID)
);

CREATE TABLE non_member (
    custID varchar(10),
    primary key (custID),
    foreign key (custID) references customer(custID)
);

CREATE TABLE member (
    custID varchar(10),
    startDate date,
    expDate date,
    loyaltyPoints decimal(10,2),
    primary key (custID)
    foreign key (custID) references customer(custID)
);

CREATE TABLE cart(
    custID varchar(10),
    commodityID varchar(10),
    quantity int,
    add_date date,
    primary key (custID, commodityID),
    foreign key (custID) references customer(custID) on delete cascade
);

CREATE TABLE order(
    orderID varchar(10),
    order_date date,
    delivery_type varchar(10),
    primary key (orderID)
)

CREATE TABLE order_items(
    orderID varchar(10),
    commodityID varchar(10),
    quantity int,
    name varchar(50),
    primary key (orderID, commodityID),
    foreign key (orderID) references order(orderID) on delete cascade
)

CREATE TABLE payment_regist(
    custID varchar(10),
    cardID varchar(10),
    card_type varchar(10),
    primary key (custID, cardID),
    foreign key (custID) references customer(custID) on delete cascade
)

CREATE TABLE paid(
    custID varchar(10),
    cardID varchar(10),
    orderID varchar(10),
    pay_status varchar(10),
    primary key (custID, cardID, orderID),
    foreign key (custID, cardID) references payment_regist(custID, cardID),
    foreign key (orderID) references order(orderID)
)

CREATE TABLE checkout(
    custID varchar(10),
    orderID varchar(10),
    date_shipped date,
    primary key (custID, orderID),
    foreign key (custID) references customer(custID),
    foreign key (orderID) references order(orderID)
);