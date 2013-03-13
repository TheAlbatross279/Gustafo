from state import State
import helpanswer


class HelpResponse(State):
    @staticmethod
    def recognize(msg):
      affirmative_words = ['yes', 'ya', 'sure', 'maybe', 'always', 'yeah']
      negative_words = ['no', 'nope', 'never']
      isAffirmative = False   
   
      for w in msg:
         if w.lower() in affirmative_words:
            isAffirmative = True
            return (1, {'isAffirmative': isAffirmative, 'specific' : False})

      return (1, {'isAffirmative': isAffirmative, 'specific' : False})

    @staticmethod
    def respond(context):
       #print context 
       if context['isAffirmative']:
          return "Great. What else can I tell you?"
       else:
          State.user_state[context['_nick']] = None
          return "Okay. I hope I answered your question!"

    @staticmethod
    def next_states():
       return tuple([helpanswer.HelpAnswer])

State.register(HelpResponse)
