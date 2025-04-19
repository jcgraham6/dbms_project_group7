DROP TABLE monitor;
DROP TABLE inventory;
DROP TABLE employee;
CREATE TABLE employee (
    ssn VARCHAR(9),
    name VARCHAR(50),
    birthday DATE,
    salary DECIMAL(10, 2),
    position VARCHAR(20),
    password varchar(20),
    PRIMARY KEY (ssn)
);

INSERT INTO employee (ssn, name, birthday, salary, POSITION, password) VALUES
('12305456', 'Henry', TO_DATE('1989/06/04 00:00:00', 'yyyy/mm/dd hh24:mi:ss'), 70000, 'inventory_manager', 'abc');

SELECT * FROM employee;


CREATE TABLE inventory(
    iid VARCHAR(10),
    location VARCHAR(30),
    PRIMARY KEY (iid)
);

INSERT INTO inventory (iid, location) VALUES ('001', '123 highland street');

SELECT * FROM inventory;


CREATE TABLE monitor(
    ssn VARCHAR(9),
    iid VARCHAR(10),
    assigned_date DATE,
    PRIMARY KEY (ssn, iid),
    FOREIGN KEY (ssn) REFERENCES employee(ssn),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);

INSERT INTO monitor (ssn, iid, assigned_date) VALUES ('12305456', '001', TO_DATE('2024/08/08 00:00:00', 'yyyy/mm/dd hh24:mi:ss'));

SELECT * FROM monitor;

CREATE TABLE commodity_store(
    commodityID varchar(10),
    name VARCHAR(50),
    price DECIMAL(10, 2),
    category VARCHAR(10),
    discount DECIMAL(10, 2),
    expDate DATE,
    quantity DECIMAL(10, 2),
    threshold DECIMAL(10, 2),
    iid VARCHAR(10) NOT NULL,
    PRIMARY KEY (commodityID),
    FOREIGN KEY (iid) REFERENCES inventory(iid)
);

INSERT INTO commodity_store (commodityID, name, price, category, discount, expDate, quantity, threshold, iid) VALUES
('12305456', 'apple', 1.2, 'fruit', 1.0, TO_DATE('2025/05/04 00:00:00', 'yyyy/mm/dd hh24:mi:ss'), 300, 50, '001');

SELECT * FROM commodity_store;

select * from commodity_store where commodityID = '001';