--Table: ID | Original String | Sanitized String -- maps id to phrase

CREATE TABLE IF NOT EXISTS DATA_PHRASES (
  id integer NOT NULL PRIMARY KEY,
  orig_utterance VARCHAR(500),
  sani_utterance VARCHAR(500)
);
