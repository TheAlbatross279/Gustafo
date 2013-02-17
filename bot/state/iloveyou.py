from state import State
import random

class ILoveYouState(State):
   @staticmethod
   def recognize(msg):
      iloveyou =  ["i", "love", "you"]
      
      if len(msg) < len(iloveyou):
         return (0.0, {})

      for idx, w in enumerate(iloveyou):
         if msg[idx][0].lower() != w:
               return (0.0, {})
               
      return (1.0, {})

   @staticmethod
   def respond(context):
      return "I love you too, " + context['_nick'] + "!"

#State.register(ILoveYouState, True)
