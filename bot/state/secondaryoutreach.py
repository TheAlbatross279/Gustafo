from state import State
import random

class SecondaryOutreach(State):
    @staticmethod
    def recognize(msg):
      greeting_words = ['hi', 'hello', 'hey', 'hola', 'yo']

      for (w, tag) in msg:
         if w.lower() in greeting_words:
            return (1, {})

      return (0, {})

    @staticmethod
    def respond(context):
        
        #randomly choose how are your/
        inquiries = [ "How are you?", 
                      "How's it going?",
                      "How are things?",
                      "How's it hanging?",
                      "What are you up to?", 
                      "What's up?",
                      "Sup?",
                      "What's crackin?" ]

        rand_ndx = random.randint(0, len(inquiries) - 1)

        return inquiries[rand_ndx]

State.register(SecondaryOutreach)
