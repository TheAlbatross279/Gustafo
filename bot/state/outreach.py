from state import State
from inquiry import InquiryState
from secondaryoutreach import SecondaryOutreach

class OutreachState(State):
   @staticmethod
   def recognize(msg):
      greeting_words = ['hi', 'hello', 'hey', 'hola', 'yo']

      for (w, tag) in msg:
         if w.lower() in greeting_words:
            return (1, {})

      return (0, {})

   @staticmethod
   def respond(context):
      return "Hello, " + context['_nick'] + "."

class InitialOutreach(OutreachState):
   @staticmethod
   def nextStates():
      return tuple([SecondaryOutreach])

State.register(InitialOutreach)

class OutreachResponse(OutreachState):
   @staticmethod
   def nextStates():
      return tuple([InquiryState])

State.register(OutreachResponse, True)
