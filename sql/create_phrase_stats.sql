--Table ID | UserUse | GUse -- stats on how many times something is used

CREATE TABLE DATA_PHRASE_STATS {
  id INT NOT NULL PRIMARY KEY,
  user_use INT NOT NULL,
  gust_use INT NOT NULL
};
