CREATE TABLE IF NOT EXISTS Users
(
    user_id     char(36),
    email       varchar(100) UNIQUE,
    password    TEXT,
    created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    picture_url TEXT,
    PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS Buyers
(
    user_id    char(36),
    first_name varchar(100),
    last_name  varchar(100),
    username   varchar(100) UNIQUE,
    birth_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS Sellers
(
    user_id            char(36),
    seller_name        varchar(100),
    seller_description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS Categories
(
    category_name varchar(100),
    PRIMARY KEY (category_name)
);
CREATE TABLE IF NOT EXISTS Items
(
    item_id     char(36),
    name        varchar(100),
    description TEXT,
    price       FLOAT(2),
    quantity    integer,
    category    varchar(100),
    seller_id   char(36),
    FOREIGN KEY (category) REFERENCES Categories (category_name),
    FOREIGN KEY (seller_id) REFERENCES Sellers (user_id),
    PRIMARY KEY (item_id)
);
CREATE TABLE IF NOT EXISTS Items_tags
(
    item_id char(36),
    tag     varchar(100),
    FOREIGN KEY (item_id) REFERENCES Items (item_id),
    PRIMARY KEY (item_id, tag)
);
CREATE TABLE IF NOT EXISTS Comments
(
    comment_id char(36),
    buyer_id   char(36),
    item_id    char(36),
    content    TEXT,
    rating     integer(1),
    created    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES Buyers (user_id),
    FOREIGN KEY (item_id) REFERENCES Items (item_id),
    PRIMARY KEY (comment_id)
);
CREATE TABLE IF NOT EXISTS Transactions
(
    transaction_id char(36),
    buyer_id       char(36),
    seller_id      char(36),
    item_id        char(36),
    price          FLOAT(2),
    quantity       integer,
    timestamp      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES Buyers (user_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers (user_id),
    PRIMARY KEY (buyer_id, seller_id, item_id, timestamp)
);

DROP PROCEDURE IF EXISTS validate_uuid;
DELIMITER //
CREATE PROCEDURE validate_uuid(
    IN in_uuid char(36)
)
    DETERMINISTIC
    NO SQL
BEGIN
    IF NOT (SELECT in_uuid REGEXP
                   '[[:alnum:]]{8,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{12,}') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID provided is not valid UUID format';
    END IF;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS validate_email;
DELIMITER //
CREATE PROCEDURE validate_email(
    IN in_email varchar(100)
)
    DETERMINISTIC
    NO SQL
BEGIN
    IF NOT (SELECT in_email REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'E-mail address provided is not valild e-mail format';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_user_id
    BEFORE INSERT
    ON Users
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.user_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_item_id
    BEFORE INSERT
    ON Items
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.item_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_comment_id
    BEFORE INSERT
    ON Comments
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.comment_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_transaction_id
    BEFORE INSERT
    ON Transactions
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.transaction_id);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_user_email
    BEFORE INSERT
    ON Users
    FOR EACH ROW
BEGIN
    CALL validate_email(New.email);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER adjust_item_quantity
    AFTER INSERT
    ON Transactions
    FOR EACH ROW
BEGIN
    UPDATE Items
    SET Items.quantity = Items.quantity - New.quantity
    WHERE Items.item_id = New.item_id;
END//
DELIMITER ;
