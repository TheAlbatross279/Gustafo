from state import State
from solicituser import SolicitUser
import random

class InquiryState(State):
   responce_type = 0

   @staticmethod
   def recognize(msg):
      well_being = ['how', 'are', 'is', '\'s', 'you', 'it', 'going', 'things', '?']
      activity = ['what', 'is', '\'s', 'up', 'sup', '?']

      tot_being, tot_activ = 0.0, 0.0
   
      for (w, tag) in msg:
         if w in well_being:
            tot_being += 1
         if w in activity:
            tot_activ += 1

      if tot_being / len(msg) > tot_activ / len(msg):
         return (tot_being / len(msg), {'type': 'well_being'})
      else: 
         return (tot_activ / len(msg), {'type': 'activity'})

   @staticmethod
   def respond(context):
      if context['type'] == 'well_being':
         InquiryState.responce_type = 1
         State.forceState(SolicitUser,{'_nick': context['_nick']})
         solicitations = ["Do you want to hear some gossip?",
                          "Would you like me to tell you some gossip?",
                          "I know something really interesting. Would you like to hear about it?",
                          "I have some gossip, would you like me to share it with you?"]
         rand_ndx = random.randint(0, len(solicitations) - 1)


         responses = ["I\'m doing awful. Thanks for asking. But maybe you could help. ",
                      "I am doing great, I keep hearing all these interesting rumors. ",
                      "Not bad, Could be better "]

         rand_ndy = random.randint(0, len(responses) - 1)

         return responses[rand_ndy] + solicitations[rand_ndx]
      else:
         InquiryState.responce_type = 0
         return 'Not much, what\'s up with you?'

   @staticmethod
   def nextStates():
   #if InquiryState.responce_type:
      return tuple([SolicitUser])

State.register(InquiryState)
