from db.psql import HelpConnection
from processor.nlp.filter.normalTokFilter import NormalTokFilter
import re

class HInferenceEngine():
   def __init__(self):
      self.dbConnection = HelpConnection()
      self.filt = NormalTokFilter()
      self.title_weight = 1
      self.tag_weight = 1
      self.rating_weight = 1
      self.view_weight = 1
      self.body_weight = 1
      self.max_views = 1
      self.max_rating = 1
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
      #qid = self.findBestQuestion(list(set(msg).difference(self.stop_words)))
      qid = self.find_best_answer(msg)
      response = self.findAnswer(qid)
      return response

   def find_best_answer(self, msg):
      # Find first 100 question/answer pairs that contain
      # the specified keywords in either question title/test or
      # answer text
      stripped = list(set(msg).difference(self.stop_words))
      qDict = dict()
      q = 'select q.qid, q.creator, q.editor, q.title, q.text, q.rating, q.num_views, q.favorited, q.created, q.edited from question q where %s order by q.rating desc'
      q = q % ' or '.join(["q.title ilike '%%%s%%'" % k for k in stripped])
      qs = self.dbConnection.query(q)

      self.max_views = float(max(qs, key=lambda x: x[6])[6])
      self.max_rating = float(qs[0][5])

      for qu in qs:
         (qid, _, _, title, body, rating, num_views, favorited, _, _) = qu
         rank = self.rankQuestion(qu, msg)
         qDict[qu] = (rank, qid)


      best = max(qDict.values(), key=lambda x: x[0])
      return best[1]
   
   def rankQuestion(self, question, msg):
      (_, _, _, title, body, rating, num_views, favorited, _, _) = question
      title = self.filt.filter(title)
      #Title score
      titleScore = self.getTitleScore(title, msg)
      #Views score
      viewScore = self.getViewScore(num_views)
      #Rank score
      ratingScore = self.getRatingScore(rating)

      #Sum the weights here
      rank = titleScore + viewScore + ratingScore
      
      return rank

   def getRatingScore(self, rating):
      return  self.rating_weight * (rating / self.max_rating)

   def getViewScore(self, num_views):
      return self.view_weight * (num_views / self.max_views)

   def getTitleScore(self, title, msg):
      return self.title_weight * self.calcDist(title, msg)

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

      return ((len(title_features) -
              sum([(x - y)**2 for x, y in zip(titleVector, messageVector)]))) / float(len(title_features))


   #Finds the most likely answer in a very basic way
   def findAnswer(self, qid):
      # Find the answer associated with the best qid
      answers = self.dbConnection.query(
            ("SELECT answer.text " \
             "FROM answer " \
             "WHERE answer.qid = %s " \
             "ORDER BY answer.rating DESC", [str(qid)]))

      print qid
      try:
         return answers[0]
      except:
         return "I could not find an answer"
