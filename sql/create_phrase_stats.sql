--Table ID | UserUse | GUse -- stats on how many times something is used

CREATE TABLE IF NOT EXISTS DATA_PHRASE_STATS (
  id INT PRIMARY KEY,
  user_use INT NOT NULL,
  gust_use INT NOT NULL
);
