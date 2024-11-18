INSERT INTO user (username, email, address, dietary_info, password, has_joined_event)
VALUES
  ('test_user3', 'test4@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', True),
  ('test_user4', 'test5@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', True),
  ('test_user5', 'test6@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', True),
  ('test_user6', 'test90@gmail.com', 'Flat 4, Bristol', "", 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', True);

INSERT INTO event (event_id, user_id, event_title, draw_date, event_date, event_description, cost)
VALUES
  (1, 1, 'test title', '2018-01-01', '2018-01-01', 'my event description', 'ten english pounds');
