CREATE TABLE users(
userid VARCHAR(255) PRIMARY KEY,
fullname TEXT,
username VARCHAR(50) UNIQUE,
email VARCHAR(50) UNIQUE,
birthday DATE,
country TEXT,
gender TEXT,
password TEXT
);
