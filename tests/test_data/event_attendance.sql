INSERT INTO user (username, email, address, dietary_info, password)
VALUES
  ('test_user3', 'test4@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'),
  ('test_user4', 'test5@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'),
  ('test_user5', 'test6@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79'),
  ('test_user6', 'test90@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO event (event_id, user_id, event_title, draw_date, event_date, event_description, cost)
VALUES
  (1, 1, 'test title', '2018-01-01', '2018-01-01', 'my event description', 'ten english pounds'),
  (2, 1, 'test title 2024', '2024-01-01', '2024-01-01', 'the recent event', 'twenty english pounds');
