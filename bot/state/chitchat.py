from state import State
from db import SQLiteConn
from processor.nlp.chitChatProcessor import ChitChatProcessor
from processor.nlp.filter.filter import Filter

class ChitChat(State):
    chat_words = dict()
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
        db_conn.close()
        
    @staticmethod
    def recognize(msg):
        #look up common chit chat
        confidence = 0

        string_msg = []
        for (word, pos) in msg:
            if word in ChitChat.chat_words:
                confidence += ChitChat.chat_words[word]
                string_msg.append(word)

        string_msg = " ".join(string_msg)
        return (confidence / float(len(msg)), {'msg': string_msg})
        
    @staticmethod
    def respond(context):
        response = ChitChat.processor.respond(context['msg'])
        return response

State.register(ChitChat, True)


        
