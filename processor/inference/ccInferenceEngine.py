"""
Retrieves appropriate response to query given as input for the chit-chat state.
@author Kim Paterson
"""

from db import SQLiteConn
from operator import itemgetter
from math import ceil 
import sqlite3
import random

class CCInferenceEngine():
   def __init__(self):
      self.last_msg = None
      self.db_conn = SQLiteConn('db/ccie.db')

   def infer(self, msg):
      """Infers a resonse given a message.

      Takes list of strings as input, returns a string.
      """
      msg_id = self.find_id(msg)
      response = ""
      
      #if msg does not exist in db
      if msg_id is None: 
          self.add_msg(msg, msg, self.last_msg)
          response = self.gen_response(msg)
      #if exists, find response
      else:
          response = self.lookup_response(msg, msg_id)
          self.update_db_stats(msg_id, True)
          self.add_use_case(msg_id)
      return response


   def find_id_original(self, msg):
      """Finds Id of phrase in db"""
      #lookup in db 
      query = ("SELECT id FROM DATA_PHRASES WHERE orig_utterance = '"  + msg + "';")
      result = self.db_conn.query(query)
      
      if result:
         return result[0]
      else:
         return None

   def find_id(self, msg):
      """Finds Id of phrase in db"""
      #lookup in db 
      query = ("SELECT id FROM DATA_PHRASES WHERE sani_utterance = '"  + msg + "';")
      result = self.db_conn.query(query)
      
      if result:
         return result[0]
      else:
         return None


   def lookup_response(self, msg, msg_id):
      """Looks up an appropirate response, given a known msg id"""
      if msg_id: 
      #given msg_id, find all responses to msg_id in convo_pairs
         response_query = ("SELECT orig_utterance "
                        "FROM DATA_PHRASES "
                        "WHERE id = (SELECT id " 
                                      "FROM DATA_PHRASE_STATS "
                                      "WHERE id IN (SELECT response_id "
                                                    "FROM DATA_CONVO_PAIRS "
                                                    "WHERE utterance_id = %s) "
                                      "ORDER BY user_use desc, gust_use asc "
                                      "LIMIT 1);" % msg_id[0])
   
         responses = self.db_conn.query(response_query)

         if responses is not None:
            if len(responses) > 0:
               self.last_msg = self.find_id_original(responses[0][0])[0]
               return responses[0][0]
         else:
            return "No idea!"

   def gen_response(self, msg):
      """generates a new response"""
      
      #find random response to go back with
      phrases = ['I once got my head stuck in some railings...', 
                 "I don't want to talk about that",
                 "Let's talk about something else",
                 "Can we move on?", 
                 "Can we change the subject?",
                 "Why?"]
      
      responses = self.db_conn.query("SELECT id, orig_utterance from DATA_PHRASES WHERE sani_utterance like 'what%'")

      rand_ndx = random.randint(0, len(responses) - 1)
      self.last_msg = str(responses[rand_ndx][0])
      return responses[rand_ndx][1]


   def update_db_stats(self, msg_id, user=False):
      """Updates the usage stats for a message in the db"""

      update_query = "UPDATE DATA_PHRASE_STATS SET"

      if user == True:
         update_query = (update_query + " user_use = user_use + 1 Where ID = %s" % msg_id[0])
      else: 
        update_query = (update_query + " gust_use = gust_use + 1 Where ID = %s" % msg_id[0])

      #push to db
      self.db_conn.query(update_query, True)
      

   def add_use_case(self, utterance_id):
      """ Adds a use case of a phrase being said in response to utterance_id phrase. 
      Updates DATA_CONVO_PAIRS and DATA_STATS
      """
      if len(utterance_id) > 0:
         utterance_id = utterance_id[0]
      if (self.last_msg != None and (self.last_msg != '1' 
                                     and self.last_msg != '2'
                                     and self.last_msg != '3'
                                     and self.last_msg != '4'
                                     and self.last_msg != '5')):
         update_query = ("INSERT INTO DATA_CONVO_PAIRS ( utterance_id, response_id )"
                         " VALUES (%s, '%s');" % (self.last_msg, utterance_id))
         try:
            self.db_conn.query(update_query, True)
         except sqlite3.IntegrityError:
            pass

   def add_msg(self, filtered_msg, unfiltered_msg, utterance_id):
      """Adds a new message to the db and pairs it with the utterance_id"""
       #insert into DATA_Phrases
      insert_statement1 = ('INSERT INTO DATA_PHRASES (orig_utterance, sani_utterance) VALUES ("%s", "%s");'
                           % (unfiltered_msg, filtered_msg))
      self.db_conn.query(insert_statement1, True)
      
      #get id
      response_id = self.find_id(filtered_msg)
      if response_id != None:
         self.add_use_case(response_id)
         #insert into DATA_stats
         insert_statement3 = ('INSERT INTO DATA_PHRASE_STATS (id, user_use, gust_use)' +
                              ' VALUES (%s, %s, %s);' % (response_id[0], "1", "0"))
         self.db_conn.query(insert_statement3, True)


def main():
   ccie = CCInferenceEngine()
   print "How are you?"
   ccie.lookup_response(['how', 'are', 'you'], '1')
   ccie.lookup_response(['heya'], '2')
