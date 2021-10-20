DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS expenditure;
DROP TABLE IF EXISTS income;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE expenditure (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  inserted_by TEXT NOT NULL,
  spent_by TEXT NOT NULL,
  spent_date TEXT NOT NULL,
  items TEXT NOT NULL,
  category TEXT NOT NULL,
  amount DOUBLE(5,2) NOT NULL,
  reciept_img BLOB,
  FOREIGN KEY (inserted_by) REFERENCES user (username)
);

CREATE TABLE income (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 added_date TEXT NOT NULL,
 source TEXT NOT NULL,
 inserted_by TEXT NOT NULL,
 received_by TEXT NOT NULL,
 amount DOUBLE(5,2) NOT NULL,
 remarks TEXT,
 FOREIGN KEY (inserted_by) REFERENCES user (username)
 );

 CREATE TABLE request(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 item TEXT NOT NULL,
 requested_by TEXT NOT NULL,
 request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 remarks TEXT,
 FOREIGN KEY (requested_by) REFERENCES user(username)

 )