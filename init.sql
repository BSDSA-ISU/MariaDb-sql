create database if not exists passwordv2;;
use passwordv2;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE password_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    username VARCHAR(255),
    password VARCHAR(255),
    website VARCHAR(255),
    comment VARCHAR(255) DEFAULT 'My important password',

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

