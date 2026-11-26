import sqlite3

db = sqlite3.connect('novabiom.db')

c = db.cursor()
c.executescript( '''
    CREATE TABLE users(
  id INTEGER PRIMARY KEY,
  email VARCHAR NOT NULL UNIQUE,
  password_hash VARCHAR NOT NULL,
  full_name VARCHAR NOT NULL,
  role VARCHAR NOT NULL,
  is_active INTEGER NOT NULL CHECK (is_active IN (0, 1)),
  created_at VARCHAR
);

CREATE TABLE samples(
  id INTEGER PRIMARY KEY,
  serial_number VARCHAR NOT NULL UNIQUE,
  client_name VARCHAR NOT NULL,
  status VARCHAR NOT NULL,
  hold_status VARCHAR,
  status_changed_at VARCHAR NOT NULL, 
  created_at VARCHAR, 
  created_by INT,
  FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE  status_events (
  id INTEGER PRIMARY KEY,
  sample_id INTEGER NOT NULL,
  from_status VARCHAR,
  to_status VARCHAR NOT NULL,
  comment VARCHAR,
  actor_id INT,
  created_at VARCHAR,
  FOREIGN KEY (sample_id) REFERENCES samples(id),
  FOREIGN KEY (actor_id) REFERENCES users(id)
);

'''
)
db.commit()
db.close()

