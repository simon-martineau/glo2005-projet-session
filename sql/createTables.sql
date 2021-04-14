CREATE TABLE users
(
    id         INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name  VARCHAR(50),
    username   VARCHAR(50),
    birth_date DATE
);
CREATE TABLE buyers
(
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);
CREATE TABLE sellers(
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id)
)
;
CREATE TABLE users
(
    first_name VARCHAR,
    last_name  VARCHAR,
    username   VARCHAR,
    birth_date DATE
);
