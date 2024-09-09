INSERT INTO user (username, email, address, dietary_info, password)
VALUES
  ('test', 'test@gmail.com', "", "", 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'test2@gmail.com', "", 'Im a veggie', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'),
  ('test_user', 'test3@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO event (event_title, draw_date, event_date, event_description, cost)
VALUES
  ('test title', '2018-01-01', '2018-01-01', 'my event description', 'ten english pounds'),
  ('test title 2024', '2024-01-01', '2024-01-01', 'the recent event', 'twenty english pounds');