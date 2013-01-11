from state import State
from gossip import Gossip

class UserResponse(Gossip):
    @staticmethod
    def recognize(msg):
      affirmative_words = ['yes', 'ya', 'sure', 'maybe', 'always', 'yeah']
      negative_words = ['no', 'nope', 'never']
      isAffirmative = False   
   
      for (w, tag) in msg:
         if w.lower() in affirmative_words:
            isAffirmative = True
            return (1, {'isAffirmative': isAffirmative, 'specific' : False})

      for (w, tag) in msg:
         if w.lower() in negative_words:
            isAffirmative = False
            return (1, {'isAffirmative': isAffirmative, 'specific' : False})

      return (0, {})

State.register(UserResponse)
