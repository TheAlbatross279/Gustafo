from state import State
from helpresponse import HelpResponse
from processor.nlp.helpProcessor import HelpChatProcessor
from processor.nlp.filter.filter import Filter

class HelpAnswer(State):
   @staticmethod
   def init():
      HelpAnswer.processor = HelpChatProcessor(Filter())

   @staticmethod
   def recognize(msg):
      return (1.0, {'msg': ' '.join([x[0] for x in msg])})

   @staticmethod
   def respond(context):
       return "Here is the answer to your question:\n%s\nCan I help you with anything else?" % HelpAnswer.processor.respond(context['msg'])

   @staticmethod
   def next_states():
      return tuple([HelpResponse])

State.register(HelpAnswer)
        
