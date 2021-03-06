from db.psql import HelpConnection
from processor.nlp.filter.normalTokFilter import NormalTokFilter
import re

class HInferenceEngine():
   def __init__(self):
      self.MIN_SCORE = .1
      self.dbConnection = HelpConnection()
      self.filt = NormalTokFilter()
      self.title_weight = 1
      self.tag_weight = .5
      self.rating_weight = .3 
      self.view_weight = .1 
      self.body_weight = 1
      self.max_views = 1
      self.max_rating = 1
      self.stop_words = ['i', 'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on',
                         'are', 'with', 'as', 'I', 'his', 'they', 'be', 'at', 'one', 'have', 'this', 'from', 'or', 
                         'had', 'by', 'hot', 'but', 'some', 'we', 'can', 'out', 'other', 'were',
                         'all', 'there', 'when', 'up', 'use', 'your', 'said', 'an', 'each', 'she', 'which',
                         'do', 'their', 'will', 'way', 'about', 'many', 'then', 'them',
                         'would', 'like', 'so', 'these', 'her', 'thing', 'see', 'him',
                         'has', 'look', 'more', 'day', 'could', 'go', 'come', 'did', 'no',
                         'most', 'people', 'my', 'over', 'know', 'water', 'who', 'may',
                         'down', 'object', 'side', 'been', 'now', 'any', 'work', 'part', 'take', 
                         'place', 'made', 'live', 'back', 'little', 'only', 'round', 'man']

   """
   takes list of strings as input, returns string
   """
   def infer(self, msg):
      qid = self.find_best_answer(msg)
      response = self.findAnswer(qid)
      return response

   def find_best_answer(self, msg):
      # Find first 100 question/answer pairs that contain
      # the specified keywords in either question title/test or
      # answer text
      tmp = list(set(msg).difference(self.stop_words))
      stripped = tmp if tmp else list(set(msg))
      qDict = dict()
      q = 'select q.qid, q.creator, q.editor, q.title, q.text, ' \
          'q.rating, q.num_views, q.favorited, q.created, q.edited from question q where %s order by q.rating desc'
      q = q % ' or '.join(["q.title ilike '%%%s%%'" % k for k in stripped])
      qs = self.dbConnection.query(q)

      if not qs:
         return None

      self.max_views = float(max(qs, key=lambda x: x[6])[6])
      self.max_rating = float(qs[0][5])

      for qu in qs:
         (qid, creator, editor, title, body, rating, num_views, favorited, created, edited) = qu
         rank = self.rankQuestion(qu, msg)
         qDict[qu] = (rank, qid)


      best = max(qDict.values(), key=lambda x: x[0])
      return best[1] if best[0] >= self.MIN_SCORE else None
   
   def get_body_score(self, body, keywords):
      temp1 = set(self.filt.filter(body)).difference(self.stop_words)
      temp2 = set(keywords).difference(self.stop_words)
      body_set = temp1 if temp1 else set(self.filt.filter(body))
      keyword_set = temp2 if temp2 else set(keywords)
      return (len(body_set.intersection(keyword_set))/float(len(body_set))) * self.body_weight

   def get_tag_score(self, tags, keywords):
      temp = set(keywords).difference(self.stop_words)
      keyword_set = temp if temp else set(keywords)
      tag_set = set(tags)
      return (len(tag_set.intersection(keyword_set))/float(len(tag_set))) * self.tag_weight


   def rankQuestion(self, question, msg):
      (qid, creator, editor, title, body, rating, num_views, favorited, created, edited) = question
      tags = map(lambda x: x[0], self.dbConnection.query(('select distinct tag from tag_question where qid = %s', [qid])))

      title = self.filt.filter(title)

      # Tag score
      tag_score = self.get_tag_score(tags, msg)

      # Body score
      body_score = self.get_body_score(body, msg)

      #Title score
      titleScore = self.getTitleScore(title, msg)

      #Views score
      viewScore = self.getViewScore(num_views)

      #Rank score
      ratingScore = self.getRatingScore(rating)

      #Sum the weights here
      rank = titleScore + viewScore + ratingScore + body_score + tag_score
      
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
      try:
         answers = self.dbConnection.query(
               ("SELECT answer.text " \
                "FROM answer " \
                "WHERE answer.qid = %s " \
                "ORDER BY answer.rating DESC", [str(qid)]))

         print qid
         return answers[0]
      except:
         self.dbConnection.connection.commit()
         return "I could not find an answer"

