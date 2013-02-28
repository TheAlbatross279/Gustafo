--Creates the POS Patterns table

CREATE TABLE IF NOT EXISTS DATA_POS_PATTERNS (
  pos_id integer NOT NULL PRIMARY KEY, 
  pos_pattern VARCHAR(200)
);
