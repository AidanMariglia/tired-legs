BEGIN;

DROP TABLE IF EXISTS bench;

CREATE TABLE bench (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_number TEXT,
    address_street TEXT,
    side TEXT,
    search_street TEXT
);

COMMIT;