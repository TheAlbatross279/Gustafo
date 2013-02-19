"""
Filter subclass that contains method for normailizing and returns 
full parse tokenized as a default action.
@author Kim Paterson
"""
from processor.nlp.filter.filter import Filter
import re

class NormalTokFilter(Filter):
   def filter(self, msg):
      return self.full_parse(msg)

   def full_parse(self, msg):
       return self.split_parse(self.normalize(msg))
