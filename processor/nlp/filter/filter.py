"""
Filter superclass that contains method for normailizing and returns 
full parse as a default action.
"""

import re

class Filter(object):
   def filter(self, msg):
      return self.fullParse(msg)

   def normalize(self, msg):
       splitMsg = msg.lower()
       splitMsg = re.sub("[^A-Za-z0-9 ]", "", splitMsg)
       splitMsg = re.sub("[ ]+", " ", splitMsg)
       return splitMsg
        
   def splitParse(self, msg):
       splitMsg = self.normalize(msg)
       splitMsg = splitMsg.split(" ")
       print splitMsg

       return splitMsg

   def fullParse(self, msg):
       return self.normalize(msg)

   def main():
       fil = Filter()
       msg = fil.filter("Hello, ?!@#$%^&**$#@#$&*(^&, how?\"")
       print msg
        
   if __name__ == "__main__":
       main()
