from state import State
from solicituser import SolicitUser
import random

class RedditState(State):
   @staticmethod
   def recognize(msg):
      phrase = ("when", "does", "the", "narwhal", "bacon")

      if len(msg) < len(phrase):
         return (0.0, {})

      for idx, w in enumerate(phrase):
         if msg[idx][0].lower() != w:
            return (0.0, {})

      return (1.0, {})

   @staticmethod
   def respond(context):
      State.forceState(SolicitUser,{'_nick': context['_nick']})

      solicitations = ["Do you want to hear some gossip?",
                       "Would you like me to tell you some gossip?",
                       "I know something really interesting. Would you like to hear about it?",
                       "I have some gossip, would you like me to share it with you?"]

      rand_ndx = random.randint(0, len(solicitations) - 1)
      return "Midnight. " + solicitations[rand_ndx]

   @staticmethod
   def nextStates():
       return tuple([SolicitUser])

State.register(RedditState, True)
