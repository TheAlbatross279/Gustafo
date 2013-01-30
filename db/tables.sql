CREATE TABLE question (
    qid INTEGER PRIMARY KEY,
    creator VARCHAR(255) REFERENCES user,
    editor VARCHAR(255) REFERENCES user,
    title VARCHAR(255),
    text VARCHAR(65535),
    rating INTEGER,
    favorited INTEGER,
    created DATE,
    edited DATE
);

CREATE TABLE answer (
    aid INTEGER PRIMARY KEY,
    qid INTEGER REFERENCES question,
    user VARCHAR(255) REFERENCES user,
    text VARCHAR(65535),
    rating INTEGER,
    time DATE
);

CREATE TABLE qcomment (
    qcid INTEGER PRIMARY KEY,
    qid INTEGER REFERENCES question,
    user VARCHAR(255) REFERENCES user,
    text VARCHAR(65535),
    rating INTEGER,
    time DATE
);

CREATE TABLE acomment (
    acid INTEGER PRIMARY KEY,
    aid INTEGER REFERENCES answer,
    user VARCHAR(255) REFERENCES user,
    text VARCHAR(65535),
    rating INTEGER,
    time DATE
);

CREATE TABLE user (
    user VARCHAR(255) PRIMARY KEY,
    reputation INTEGER,
    gold_badge INTEGER,
    silver_badge INTEGER,
    bronze_badge INTEGER
);

CREATE TABLE tag (
    tag VARCHAR(32) PRIMARY KEY
);

-- Many to many relationship
-- Tags can references many questions, and questions can reference many tags
CREATE TABLE tag_question (
    tag VARCHAR(32) REFERENCES tag,
    qid INTEGER REFERENCES question
);
