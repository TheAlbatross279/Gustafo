from state import State
from db import SQLiteConn
from processor.nlp.chitChatProcessor import ChitChatProcessor
from processor.nlp.filter.filter import Filter
from nltk import pos_tag
from math import sqrt

class ChitChat(State):
    chat_words = dict()
    pos_phrases = dict()
    @staticmethod
    def init():
        ChitChat.processor = ChitChatProcessor(Filter())
    
        #initialize dictionary of chat words
        db_conn = SQLiteConn('db/ccie.db')
        query = "SELECT sani_utterance FROM DATA_PHRASES;"
        chat_phrases = db_conn.query(query)

        for phrase in chat_phrases:
            for entry in phrase:
                words = entry.split(" ")
                for word in words:
                    ChitChat.chat_words[word] = 1

        #initialize the syntactic pattern matching
        pattern_query = "SELECT * FROM DATA_POS_PATTERNS;"

        pos_patterns = db_conn.query(pattern_query)
        for pos_pattern in pos_patterns:
            ChitChat.pos_phrases[pos_pattern[0]] = pos_pattern[0]

        db_conn.close()
        
    @staticmethod
    def recognize(msg):
        #look up common chit chat
        confidence = 0

        string_msg = []
        for word in msg:
            if word in ChitChat.chat_words:
                confidence += ChitChat.chat_words[word]
                string_msg.append(word)

        confidence =  confidence / float(len(msg))

        #tag the words and look for pattern
        if ChitChat.check_pos(msg) == True:
            confidence =  sqrt(confidence)

        msg = " ".join(msg)
        return (confidence, {'msg': msg})
        
    @staticmethod
    def check_pos(msg):
        pos_tags = pos_tag(msg)
        tag_pattern = []
        for (word, tag) in pos_tags:
            tag_pattern.append(tag) 
        pattern =  " ".join(tag_pattern)
        if pattern in ChitChat.pos_phrases:
            return True
        else:
            return False
        

    @staticmethod
    def respond(context):
        response = ChitChat.processor.respond(context['msg'])
        return response
   


#State.register(ChitChat, True)


        
