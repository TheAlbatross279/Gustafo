from sqlite import SQLiteConn
from nltk import pos_tag

def parse_all():
    db_conn = SQLiteConn('./ccie.db')
    
    pos_patterns = dict()
    query = "SELECT sani_utterance FROM DATA_PHRASES;"
    chat_phrases = db_conn.query(query)
    for phrase in chat_phrases:
        phrase = phrase[0].split(" ")
        pos_tags = pos_tag(phrase[0])
        tag_pattern = []
        for (word, tag) in pos_tags:
            tag_pattern.append(tag) 

        pos_patterns[" ".join(tag_pattern)] = True

    insert_statement = "INSERT INTO DATA_POS_PATTERNS VALUES "
    inserts = []
    for i, pos_pattern in enumerate(pos_patterns):
        inserts.append("('" + pos_pattern + "')")
        if i != len(pos_patterns)-1:
            inserts.append(", \n")

    insert_statement = insert_statement + " ".join(inserts) + ";"
    

    print insert_statement
    db_conn.close()

    f = open('create_pos_patterns.sql', 'w')
    f.write(insert_statement)
    f.close()
parse_all()
