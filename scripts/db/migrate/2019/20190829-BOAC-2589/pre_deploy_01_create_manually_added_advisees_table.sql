BEGIN;

CREATE TABLE manually_added_advisees (
  sid VARCHAR(80) PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

COMMIT;