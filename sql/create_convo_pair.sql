--Table InitID | ResID -- stored pairs of initiation and response


CREATE TABLE DATA_CONVO_PAIR (
  utterance_id INT NOT NULL,
  response_id INT NOT NULL,
  PRIMARY KEY(utterance_id, response_id)
);
