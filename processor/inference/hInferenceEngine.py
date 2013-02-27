from db.psql import HelpConnection
"""

"""

class HInferenceEngine():
   def __init__(self):
      self.dbConnection = HelpConnection()

   """
   takes list of strings as input, returns string
   """
   def infer(self, msg):

      response = self.findAnswer(msg)

      return response

   #Finds the most likely answer in a very basic way
   def findAnswer(self, msg):
      qidDict = {}
      
      #Iterate over all keywords
      for keyword in msg:
         #Save all qids associated with the specified keyword
         qids = self.dbConnection.query(("SELECT question.qid FROM question WHERE question.title SIMILAR TO %s", ['%'+keyword+'%']))
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

      #Find the answer associated with the best qid
      answers = self.dbConnection.query(("SELECT answer.text FROM answer WHERE answer.qid = %s", [str(bestqid)]))

      try:
         return answers[0]
      except:
         return "I could not find an answer"
