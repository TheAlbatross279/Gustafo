"""
Filter superclass that contains method for normailizing and returns 
full parse as a default action.
@author Kim Paterson
"""

import re

class Filter(object):
   def filter(self, msg):
      return self.full_parse(msg)

   def normalize(self, msg):
       split_msg = msg.lower()
       split_msg = re.sub("[^A-Za-z0-9 ]", "", split_msg)
       split_msg = re.sub("[ ]+", " ", split_msg)
       return split_msg
        
   def split_parse(self, msg):
       split_msg = self.normalize(msg)
       split_msg = split_msg.split(" ")

       return split_msg

   def full_parse(self, msg):
       return self.normalize(msg)

def main():
   fil = Filter()
   msg = fil.filter("Hello, ?!@#$%^&**$#@#$&*(^&, how?\"")
   print msg
        
if __name__ == "__main__":
   main()
