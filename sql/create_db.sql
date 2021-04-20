CREATE TABLE IF NOT EXISTS Users
(
    user_id     char(36) UNIQUE NOT NULL,
    email       varchar(100) UNIQUE NOT NULL,
    password    TEXT NOT NULL,
    created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS Buyers
(
    user_id    char(36) UNIQUE NOT NULL,
    first_name varchar(100) NOT NULL,
    last_name  varchar(100) NOT NULL,
    username   varchar(100) UNIQUE NOT NULL,
    birth_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS Sellers
(
    user_id     char(36) UNIQUE NOT NULL,
    name        varchar(100) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS Categories
(
    category_id integer AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    PRIMARY KEY (category_id)
);
CREATE TABLE IF NOT EXISTS Items
(
    item_id     char(36) UNIQUE NOT NULL,
    name        varchar(100) NOT NULL,
    description TEXT NOT NULL,
    price       FLOAT(2) NOT NULL,
    quantity    integer NOT NULL,
    category_id integer NOT NULL,
    seller_id   char(36) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories (category_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers (user_id),
    PRIMARY KEY (item_id)
);
CREATE TABLE IF NOT EXISTS Comments
(
    comment_id char(36) UNIQUE NOT NULL,
    buyer_id   char(36) NOT NULL,
    item_id    char(36) NOT NULL,
    content    TEXT NOT NULL,
    rating     integer(1) NOT NULL,
    created    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES Buyers (user_id),
    FOREIGN KEY (item_id) REFERENCES Items (item_id),
    PRIMARY KEY (comment_id)
);
CREATE TABLE IF NOT EXISTS Transactions
(
    transaction_id char(36) UNIQUE NOT NULL,
    buyer_id       char(36) NOT NULL,
    seller_id      char(36) NOT NULL,
    item_id        char(36) NOT NULL,
    price          FLOAT(2) NOT NULL,
    quantity       integer NOT NULL,
    timestamp      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES Buyers (user_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers (user_id),
    PRIMARY KEY (transaction_id)
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
CREATE TRIGGER verify_quantity_available
    BEFORE INSERT
    ON Transactions
    FOR EACH ROW
BEGIN
    IF (SELECT I.quantity FROM Items I WHERE I.item_id=NEW.item_id) < NEW.quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The quantity left for this item is not sufficient';
    END IF;
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
