DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS journals;
DROP TABLE IF EXISTS weather;

CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    email TEXT NOT NULL, 
    password_hash TEXT NOT NULL
);

CREATE TABLE journals (
    id INTEGER PRIMARY KEY, 
    user_id INTEGER, 
    body TEXT, 
    mood INTEGER, 
    date DATETIME DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE weather (
    id INTEGER PRIMARY KEY, 
    title TEXT, 
    description TEXT, 
    icon TEXT, 
    temp NUMERIC, 
    feels_like NUMERIC, 
    cloudiness TEXT, 
    journal_id INTEGER, 
    FOREIGN KEY(journal_id) REFERENCES journals(id)
);