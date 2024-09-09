DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS event_attendence;

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  address TEXT,
  dietary_info TEXT DEFAULT "None",
  password TEXT NOT NULL
);

CREATE TABLE event (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  draw_date DATE NOT NULL,
  event_date DATE NOT NULL,
  event_description MEDIUMTEXT NOT NULL,
  cost TEXT NOT NULL
);

CREATE TABLE event_attendence (
  user_id INTEGER REFERENCES user(user_id),
  event_id INTEGER REFERENCES event_info(event_id),
  joined BOOLEAN DEAFULT FALSE
)
