import sys
import re
from processor.nlp.filter.normalTokFilter import NormalTokFilter
from db import SQLiteConn
import sqlite3
class ProcessLogs():
    def process(self, log_file):
        log =  open(log_file, "r")
    
        content = log.read()

        content = re.split("\n", content)

        messages = []
        for line in content:
            if re.match("[^0-9:0-9 (PM|AM)]", line) != None:
                line = line.strip()
                messages.append(line[line.find(":") +1:])
            
        return messages  


    def filter_msgs(self, messages):
        filt = NormalTokFilter()
        message_pairs = []
        for msg in messages:
            filt_msg = " ".join(filt.filter(msg))
            temp = (msg.strip(), filt_msg.strip())
            message_pairs.append(temp)
#            print temp
        return message_pairs

    def add_to_db(self, msg_pairs):
        db_conn = SQLiteConn('db/ccie.db')

        ids = []

        for msg_p in msg_pairs:
            insert_statement1 = ('INSERT INTO DATA_PHRASES (orig_utterance, sani_utterance) VALUES ("%s", "%s");'
                                 % (msg_p[0], msg_p[1]))
            try:
                db_conn.query(insert_statement1, True)
            except sqlite3.IntegrityError:
                pass

            #print insert_statement1

            query = ("SELECT id FROM DATA_PHRASES WHERE sani_utterance = '"  + msg_p[1] + "';")

            results = None
            try:
                result = db_conn.query(query)
            except sqlite3.IntegrityError:
                pass


            if result:
                ids.append((result[0][0], msg_p[1]))

#        print ids

        for x in range(len(msg_pairs)-1):
#            print ids[x], ids[x+1]

            update_query = ("INSERT INTO DATA_CONVO_PAIRS ( utterance_id, response_id )"
                                " VALUES (%s, '%s');" % (ids[x][0], ids[x+1][0]))
            try:
                db_conn.query(update_query, True)
            except sqlite3.IntegrityError:
                pass



def main(file):
#    print file
    pl = ProcessLogs()
    messages = pl.process(file)
#    print messages
    pairs = pl.filter_msgs(messages)
    pl.add_to_db(pairs)
