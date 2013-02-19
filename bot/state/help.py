from state import State
from .helpanswer import HelpAnswer
from processor.nlp.helpProcessor import HelpChatProcessor
from processor.nlp.filter.filter import Filter

class Help(State):
   @staticmethod
   def init():
      pass
   
   @staticmethod
   def recognize(msg):
      #help_keywords = ['help', 'java', 'programming', 'abstract', 'continue',
      #                 'for', 'new', 'switch',
      #                 'assert', 'default', 'goto', 'package', 'synchronized',
      #                 'boolean', 'do', 'if', 'private', 'this',
      #                 'break', 'double', 'implements', 'protected', 'throw',
      #                 'byte', 'else', 'import', 'public', 'throws',
      #                 'case', 'enum', 'instanceof', 'return', 'transient',
      #                 'catch', 'extends', 'int', 'short', 'try',
      #                 'char', 'final', 'interface', 'static', 'void',
      #                 'class', 'finally', 'long', 'strictfp', 'volatile',
      #                 'const', 'float', 'native', 'super', 'while', 'null']
      help_keywords = ['help']
   
      # Check msg for key phrases
      for w in msg:
         if w.lower() in help_keywords:
            return (1.0, {})
      return (0.0, {})
   
   @staticmethod
   def respond(context):
      return "It seems you need help... Ask me a question."
   
   @staticmethod
   def next_states():
      return tuple([HelpAnswer])

State.register(Help, True)
        
