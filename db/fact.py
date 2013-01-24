"""
Data structure to hold gossip
"""
import re
class Fact(object):
    
    def __init__(self, author, msg, recipient, knowers):
        self.author = author
        self.msg = re.sub("'", "", msg)
        self.recipient = recipient
        self.knowers = knowers
    
    def to_list(self):
        return [self.author, self.msg, self.recipient, "; ".join(self.knowers)]

    
    




#f = fact("Gustafo", "Hello, Gustapen", "Kim", ["Kim", "Gustafo", "Bob"])
#print f.to_list()
