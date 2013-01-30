"""

"""

class CCInferenceEngine():
   def __init__(self):
      self.dbConnection = None

   """
   takes list of strings as input, returns string
   """
   def infer(self, msg):
      msgID = self.findID(msg)
      response = ""
      
      #if msg does not exist in db
      if msgID is None: 
          response = self.genResponse(msg)
      #if exists, find response
      else:
          response = self.lookupResponse(msg)

      return response

   #find ID of phrase in db
   def findID(msg):
       pass

   #finds response based on ID
   def lookupResponse(msg, msgID):
       pass

   #generates a response based on msg
   def genResponse(msg):
       pass
   
