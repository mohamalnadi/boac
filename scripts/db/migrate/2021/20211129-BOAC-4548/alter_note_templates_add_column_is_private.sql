BEGIN;

ALTER TABLE note_templates ADD COLUMN is_private BOOLEAN DEFAULT FALSE NOT NULL;

COMMIT;
