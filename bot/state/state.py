from multiprocessing import Pool, cpu_count
from nltk import pos_tag, word_tokenize

def state_test((msg, state)):
   return (state.recognize(msg), state)

class State:
   users = []
   states = []
   initial_states = []
   user_state = {}

   @staticmethod
   def forget():
      State.user_state = {}
   
   @staticmethod
   def register(state, isInitial=False):
      State.states.append(state)
      if isInitial:
         State.initial_states.append(state)

      state.init()

   @staticmethod
   def validate_state(state, valid_states):
      for e in valid_states:
         if issubclass(state, e):
            return True

      return False

   @staticmethod
   def force_state(state, context={}):
      if context.get('_nick', None) is not None:
         State.user_state[context['_nick']] = state

      return state.respond(context)

   @staticmethod
   def query(nick, msg):
      #print msg

      msg_tag = pos_tag(word_tokenize(msg))

      current_state = State.user_state.get(nick, None)
      if current_state is None:
         valid_states = State.initial_states
      else:
         valid_states = current_state.next_states()

      #print current_state


      confidence = map(state_test, [(msg_tag, state) for state in State.states if State.validate_state(state, valid_states)])

      #print confidence

      ((conf, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)

      if conf < 0.1:
         if not nick in State.user_state or State.user_state[nick] != State:
            State.user_state[nick] = State
            return State.query(nick, msg)
         else:
            return None

      State.user_state[nick] = state

      context['_nick'] = nick
      return state.respond(context)

   @staticmethod
   def init():
      pass

   @staticmethod
   def die():
      pass
 
   @staticmethod
   def recognize(msg):
      return (0, {})

   @staticmethod
   def respond(context):
      pass

   @staticmethod
   def next_states():
      return tuple([State])
