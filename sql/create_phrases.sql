--Table: ID | Original String | Sanitized String -- maps id to phrase

CREATE TABLE DATA_PHRASES (
  id INT NOT NULL PRIMARY KEY,
  orig_utterance VARCHAR(),
  sani_utterance VARCHAR()

);
