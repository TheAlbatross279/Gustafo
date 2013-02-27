from db.psql import HelpConnection
from processor.nlp.filter.normalTokFilter import NormalTokFilter
"""

"""

class HInferenceEngine():
   def __init__(self):
      self.dbConnection = HelpConnection()
      self.filt = NormalTokFilter()
      self.title_weight = 0.1
      self.tag_weight = 0.1
      self.rating_weight = 0.1
      self.body_weight = 0.1

   """
   takes list of strings as input, returns string
   """
   def infer(self, msg):

      qid = self.findBestQuestion(msg)

      response = self.findAnswer(qid)

      return response

   
   def findBestQuestion(self, msg):
      qDict = {}

      #Iterate over all user entered words
      for keyword in msg:
         #This will be replaced with the index query
         qs = self.dbConnection.query(("SELECT * FROM question WHERE question.title ILIKE %s", ['%'+keyword+'%']))

         for q in qs:
            qDict[q] = 0

      for q in qDict.keys():
         (qid, _, _, title, body, rating, num_views, favorited, _, _) = q

         rank = self.rankQuestion(q, msg)

         qDict[q] = (rank, qid)
       
      best = max(qDict.values(), key=lambda x: x[0])

      return best[1]

   def rankQuestion(self, question, msg):
      (_, _, _, title, body, rating, num_views, favorited, _, _) = question
      
      title = self.filt.filter(title)
      
      titleScore = self.title_weight * self.calcDist(title, msg)

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

      return len(title_features) - sum([(x - y)**2 for x, y in zip(titleVector, messageVector)])


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
      #Find the answer associated with the best qid
      answers = self.dbConnection.query(("SELECT answer.text FROM answer WHERE answer.qid = %s", [str(qid)]))

      try:
         return answers[0]
      except:
         return "I could not find an answer"
