"""
Filter that tagges and tokenizes a given string using NLTK word_tokenize() 
and pos_tag() filtering and returns a list of tuple tokens as the message 
"""

from filter import Filter
from nltk import pos_tag, word_tokenize

class TagAndTokFilter(Filter):
   def filter(self, msg):
      #normailze
      msgNormalized = self.normalize(msg)

      #tag and tokenize
      msgTagged = pos_tag(word_tokenize(msgNormalized))
      return msgTagged

def main():
   f = TagAndTokFilter()
   msg = f.filter("Hello, ?!@#$%^&**$#@#$&*(^&, how?\" are you?")
   print msg
     
if __name__ == '__main__':
   main()
