from state import State
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
      return "Midnight."

#State.register(RedditState, True)
