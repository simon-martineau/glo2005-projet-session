CREATE TABLE user
(
    id         INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name  VARCHAR(50),
    username   VARCHAR(50),
    email      VARCHAR(50),
    birth_date DATE
);

CREATE TABLE item
(

);

CREATE TABLE buyers
(
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);
CREATE TABLE sellers
(
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id)
)
;

