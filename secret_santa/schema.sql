DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS event;

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  address TEXT,
  dietary_info TEXT DEFAULT "None",
  password TEXT NOT NULL,
  giftee INTEGER REFERENCES user(user_id),
  has_joined_event BOOLEAN  DEFAULT FALSE NOT NULL
);

CREATE TABLE event (
  user_id INTEGER REFERENCES user(user_id) NOT NULL,
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_title TEXT NOT NULL,
  draw_date DATE NOT NULL,
  event_date DATE NOT NULL,
  event_description MEDIUMTEXT NOT NULL,
  cost TEXT NOT NULL
);
