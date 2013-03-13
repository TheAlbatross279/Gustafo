from db.psql import HelpConnection
from processor.nlp.filter.normalTokFilter import NormalTokFilter
import re

class HInferenceEngine():
   def __init__(self):
      self.dbConnection = HelpConnection()
      self.filt = NormalTokFilter()
      self.title_weight = 0.1
      self.tag_weight = 0.1
      self.rating_weight = 0.1
      self.body_weight = 0.1
      self.stop_words = ['i', 'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on',
                         'are', 'with', 'as', 'I', 'his', 'they', 'be', 'at', 'one', 'have', 'this', 'from', 'or', 
                         'had', 'by', 'hot', 'word', 'but', 'what', 'some', 'we', 'can', 'out', 'other', 'were',
                         'all', 'there', 'when', 'up', 'use', 'your', 'how', 'said', 'an', 'each', 'she', 'which',
                         'do', 'their', 'time', 'if', 'will', 'way', 'about', 'many', 'then', 'them', 'write',
                         'would', 'like', 'so', 'these', 'her', 'long', 'make', 'thing', 'see', 'him', 'two',
                         'has', 'look', 'more', 'day', 'could', 'go', 'come', 'did', 'number', 'sound', 'no',
                         'most', 'people', 'my', 'over', 'know', 'water', 'than', 'call', 'first', 'who', 'may',
                         'down', 'side', 'been', 'now', 'find', 'any', 'new', 'work', 'part', 'take', 'get',
                         'place', 'made', 'live', 'where', 'after', 'back', 'little', 'only', 'round', 'man',
                         'year', 'came', 'show', 'every', 'good', 'me', 'give', 'our', 'under', 'name',
                         'very', 'through', 'just', 'form', 'sentence', 'great', 'think', 'say',
                         'help', 'low', 'line', 'differ', 'turn', 'cause', 'much', 'mean', 'before',
                         'move', 'right', 'boy', 'old', 'too', 'same', 'tell', 'does', 'set', 'three',
                         'want', 'air', 'well', 'also', 'play', 'small', 'end', 'put', 'home']

   """
   takes list of strings as input, returns string
   """
   def infer(self, msg):
      # qid = self.findBestQuestion(msg)
      qid = self.find_best_answer(msg)
      response = self.findAnswer(qid)
      return response

   def find_best_answer(self, msg):
      # Find first 100 question/answer pairs that contain
      # the specified keywords in either question title/test or
      # answer text
      stripped = list(set(msg).difference(self.stop_words))
      qDict = dict()
      q = 'select q.qid, q.creator, q.editor, q.title, q.text, ' \
          'q.rating, q.num_views, q.favorited, q.created, q.edited from question q where %s order by q.rating desc'
      q = q % ' or '.join(["q.title ilike '%%%s%%'" % k for k in stripped])
      qs = self.dbConnection.query(q)
      for qu in qs:
         (qid, creator, editor, answer, title, body, rating, num_views, favorited, created, edited) = qu
         rank = self.rankQuestion(qu, msg)
         qDict[qu] = (rank, qid)
      best = max(qDict.values(), key=lambda x: x[0])
      return best[1]
   
   def get_body_score(self, body, keywords):
       body_set = set(self.filt.filter(keywords).split()).difference(self.stop_words)
       keyword_set = set(keywords).difference(self.stop_words)
       return len(body_set.intersection(keyword_set))/float(len(body_set))

   def findBestQuestion(self, msg):
      qDict = {}

      # Iterate over all user entered words
      for keyword in msg:
         # This will be replaced with the index query
         qs = self.dbConnection.query(
               ("SELECT * FROM question" \
                "WHERE question.title ILIKE %s", ['%'+keyword+'%'])
              )

         for q in qs:
            qDict[q] = 0

      for q in qDict.keys():
         (qid, _, _, title, body, rating, num_views, favorited, _, _) = q
         rank = self.rankQuestion(q, msg)
         qDict[q] = (rank, qid)
       
      best = max(qDict.values(), key=lambda x: x[0])
      return best[1]

   def rankQuestion(self, question, msg):
      (qid, creator, editor, title, body, rating, num_views, favorited, created, edited) = question
      title = self.filt.filter(title)
      titleScore = self.title_weight * self.calcDist(title, msg)
      viewScore = self.
      body_score = self.get_body_score(body, msg) * self.body_weight
      tag_score = None
      rating_score = None
      rank = titleScore
      return rank

   def calcDist(self, title, message):
      title_features = set([])
      title_features = title_features.union(title).union(message)
      titleVector = [0]*len(title_features)
      messageVector = [0]*len(title_features)

      for i, word in enumerate(title_features):
         if word in title:
            titleVector[i] = 1
         if word in message:
            messageVector[i] = 1

      return (len(title_features) -
              sum([(x - y)**2 for x, y in zip(titleVector, messageVector)]))


   #Finds the most likely answer in a very basic way
   def findAnswer(self, qid):
      '''
      qidDict = {}
      
      #Iterate over all keywords
      for keyword in msg:
         #Save all qids associated with the specified keyword
         qids = self.dbConnection.query(("SELECT question.qid FROM question WHERE question.title ILIKE %s", ['%'+keyword+'%']))
         for qid in qids:
            try:
               qidDict[qid]
            except:
               qidDict[qid] = 0
            #For every qid found, increment its value in a dictionary
            qidDict[qid] = qidDict[qid] + 1

      bestqid = 0
      high = 0
      #Iterate over the dictionary results, the highest valued qid is most likely
      for val in qidDict:
         if qidDict[val] > high:
            high = qidDict[val]
            bestqid = val[0]
      '''
      # Find the answer associated with the best qid
      answers = self.dbConnection.query(
            ("SELECT answer.text " \
             "FROM answer " \
             "WHERE answer.qid = %s " \
             "ORDER BY answer.rating DESC", [str(qid)]))

      try:
         return answers[0]
      except:
         return "I could not find an answer"

