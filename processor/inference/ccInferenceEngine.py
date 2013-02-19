"""
Retrieves appropriate response to query given as input for the chit-chat state.
@author Kim Paterson
"""
from db import SQLiteConn
from operator import itemgetter
from math import ceil 
import sqlite3

class CCInferenceEngine():
   def __init__(self):
      self.last_msg = None
      self.db_conn = SQLiteConn('db/ccie.db')

      #retrieve all data from DATA_PHRASES
      find_id_query = "SELECT * FROM DATA_PHRASES;"
      self.phrase_results = self.db_conn.query(find_id_query)
#      print self.phrase_results


      #build dictionary from results
      self.phrases_by_phrase = dict()
      self.phrases_by_id = dict()
      self.phrases_unsani = dict()

      #create dictionary for fast lookup
      for tup in self.phrase_results:
         self.phrases_by_phrase[tup[2]] = tup[0]
         self.phrases_by_id[tup[0]] = tup[2]
         self.phrases_unsani[tup[0]] = tup[1]

      #retrieve all data from DATA_CONVO_PAIRS
      find_convos_query = "SELECT * FROM DATA_CONVO_PAIRS;"
      self.convo_pairs_results = self.db_conn.query(find_convos_query)
#      print self.convo_pairs_results
 
   
      #create dictionary for data_conovos
      self.convo_pairs = dict()
      
      for tup in self.convo_pairs_results:
         if tup[0] not in self.convo_pairs.keys():
            self.convo_pairs[tup[0]] = []
         self.convo_pairs[tup[0]].append(tup[1])   

      #retrieve all data from DATA_PHRASE_STATS
      find_stats_query = "SELECT * FROM DATA_PHRASE_STATS;"
      self.stats_results = self.db_conn.query(find_stats_query)
#      print self.stats_results

      self.user_use_stats = dict()
      self.gust_use_stats = dict()

      #build dictionary for stats for Gustafo's use and User's use
      for tup in self.stats_results:
         self.user_use_stats[tup[0]] = tup[1]
         self.gust_use_stats[tup[0]] = tup[2]

#      print self.user_use_stats, self.gust_use_stats

   def infer(self, msg):
      """Infers a resonse given a message.

      Takes list of strings as input, returns a string.
      """
#      print msg
      msg_id = self.find_id(msg)
      response = ""
      
      #if msg does not exist in db
      if msg_id is None: 
          response = self.gen_response(msg)
      #if exists, find response
      else:
          response = self.lookup_response(msg, msg_id)
          self.update_db_stats(msg_id, True)
      return response


   def find_id(self, msg):
      """Finds Id of phrase in db"""
      if msg in self.phrases_by_phrase.keys():
         return self.phrases_by_phrase[msg]
      else: 
         return None


   def lookup_response(self, msg, msg_id):
      """Looks up an appropirate response, given a known msg id"""
      if msg_id not in self.convo_pairs.keys():
         return None

      #given msg_id, find all responses to msg_id in convo_pairs
      responses = self.convo_pairs[msg_id]

      if responses is not None:
         response_u_stat = dict()
         for response_id in responses: 
            response_u_stat[response_id] = self.user_use_stats[response_id]

#         print response_u_stat
         #build list of valid responses and stats tuples sorted
         response_u_stat = sorted(response_u_stat.iteritems(), 
                                  key=lambda item: int(item[1]), reverse=True)

#         print response_u_stat
         
         #choose top 60% of user-used phrases, round up
         response_u_stat = response_u_stat[:int(ceil(len(response_u_stat) * (0.6)))]
#         print response_u_stat

         response_id = response_u_stat[0][0]
         min_count = int(self.gust_use_stats[response_id])
         response_id = self.gust_use_stats[response_u_stat[0][0]]

         #calculate rank of responses based on: count_user_use - count_gustafo_use = rank
         ranked_results = [(res[0], int(res[1]) - 
                            int(self.gust_use_stats[res[0]])) for res in response_u_stat]
         #sort list by largest rank first
         ranked_results = sorted(ranked_results, key= lambda x: x[1], reverse= True)
#         print self.phrases_by_id

         #choose the first element since it is the highest ranked response
         response_id = ranked_results[0][0]

         #find unsantized response and set as response
         response = self.phrases_unsani[response_id]
#         print response

         #update db-stats
         self.update_db_stats(response_id)
         
         #adds use case for the current message and the previous one
         self.add_use_case(msg_id)
         #update this msg as the last one he used
         self.last_msg = msg_id

         return response

      #message exists in db but there are no responses to it -- this should never happen
      else: 
         print "No responses!"


   def gen_response(self, msg):
      """generates a new response"""
      print msg
      #TODO fix this logic
      if self.last_msg != None:
         self.add_msg(msg, msg, self.last_msg)
      return "I'm not sure what's going on!"


   def update_db_stats(self, msg_id, user=False):
      """Updates the usage stats for a message in the db"""
      update_query = "UPDATE DATA_PHRASE_STATS SET"

      if user == True:
         if msg_id not in self.user_use_stats:
            self.user_use_stats[msg_id] = 0
         self.user_use_stats[msg_id] = int(self.user_use_stats[msg_id]) + 1
         update_query = (update_query + " user_use = %s WHERE id = %s;" 
                         % (self.user_use_stats[msg_id], msg_id))
      else: 
         if msg_id not in self.gust_use_stats:
            self.gust_use_stats[msg_id] = 0

         self.gust_use_stats[msg_id] = int(self.gust_use_stats[msg_id]) + 1
         update_query = (update_query + " gust_use = %s WHERE id = %s;" 
                         % (self.gust_use_stats[msg_id], msg_id))

      #push to db
      self.db_conn.query(update_query, True)
      

   def add_use_case(self, utterance_id):
      """ Adds a use case of a phrase being said in response to utterance_id phrase. 
      Updates DATA_CONVO_PAIRS and DATA_STATS
      """
      
      if (self.last_msg != None and (self.last_msg != '1' 
                                     or self.last_msg != '2'
                                     or self.last_msg != '3'
                                     or self.last_msg != '4'
                                     or self.last_msg != '5')):
         update_query = ("INSERT INTO DATA_CONVO_PAIRS ( utterance_id, response_id )"
                         "VALUES (%s, %s);" % (self.last_msg, utterance_id))
         try:
            self.db_conn.query(update_query, True)
         except sqlite3.IntegrityError:
            pass

   def add_msg(self, filtered_msg, unfiltered_msg, utterance_id):
      """Adds a new message to the db and pairs it with the utterance_id"""

      print unfiltered_msg
      #insert into DATA_Phrases
      insert_statement1 = ('INSERT INTO DATA_PHRASES (orig_utterance, sani_utterance) VALUES ("%s", "%s");'
                           % (unfiltered_msg, filtered_msg))
      self.db_conn.query(insert_statement1, True)

      #get id
      response_id = self.find_id(filtered_msg)

      if response_id != None:
         #insert into DATA_Convo_pairs
         insert_statement2 = ('INSERT INTO DATA_CONVO_PAIRS (utterance_id, response_id) ' + 
                              'VALUES (%s, %s);' %  (utterance_id, response_id))
         self.db_conn.query(insert_statement2, True)
      #insert into DATA_stats
         insert_statement3 = ('INSERT INTO DATA_PHRASE_STATS (id, user_use, gust_use)' +
                              'VALUES (%s, %s, %s);' % (response_id, "1", "0"))
         self.db_conn.query(insert_statement3, True)


def main():
   ccie = CCInferenceEngine()
   print "How are you?"
   ccie.lookup_response(['how', 'are', 'you'], '1')
   ccie.lookup_response(['heya'], '2')
