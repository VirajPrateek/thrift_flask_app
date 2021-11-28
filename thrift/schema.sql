DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS expenditure;
DROP TABLE IF EXISTS income;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS personal;


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
 category TEXT NOT NULL,
 requested_by TEXT NOT NULL, 
 request_date DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
 remarks TEXT,
 FOREIGN KEY (requested_by) REFERENCES user(username)
 );

 CREATE TABLE personal(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dated DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
  user TEXT NOT NULL,
  primary_type TEXT NOT NULL,
  secondary_type TEXT NOT NULL,
  amount DOUBLE(5,2) NOT NULL,
  details TEXT,
  FOREIGN KEY (user) REFERENCES user(username)
  )

-- -- 
-- CREATE TABLE lpg (
--  id INTEGER PRIMARY KEY AUTOINCREMENT,
--  from_date TEXT NOT NULL,
--  to_date TEXT,
--  inserted_by TEXT NOT NULL,
--  remarks TEXT,
--  FOREIGN KEY (inserted_by) REFERENCES user (username)
--  );

 -- update lpg set to_date='2001-10-10' where id = (select max(id) from lpg);
