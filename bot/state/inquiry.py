from state import State
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

         responses = ["I\'m doing awful. Thanks for asking.",
                      "I am doing great!",
                      "Not bad, Could be better."]

         rand_ndy = random.randint(0, len(responses) - 1)

         return responses[rand_ndy]
      else:
         InquiryState.responce_type = 0
         return 'Not much, what\'s up with you?'

#State.register(InquiryState)
