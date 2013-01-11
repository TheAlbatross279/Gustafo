from multiprocessing import Pool, cpu_count
from nltk import pos_tag, word_tokenize

def stateTest((msg, state)):
   return (state.recognize(msg), state)

class State:
   users = []
   states = []
   initial_states = []
   userState = {}

   @staticmethod
   def forget():
      State.userState = {}
   
   @staticmethod
   def die():
      pass

   @staticmethod
   def register(state, isInitial=False):
      State.states.append(state)
      if isInitial:
         State.initial_states.append(state)

   @staticmethod
   def validateState(state, validStates):
      for e in validStates:
         if issubclass(state, e):
            return True

      return False

   @staticmethod
   def forceState(state, context={}):
      if context.get('_nick', None) is not None:
         State.userState[context['_nick']] = state

      return state.respond(context)

   @staticmethod
   def monitor(t, f, msg):
      pass

   @staticmethod
   def query(nick, msg):
      print msg

      msg_tag = pos_tag(word_tokenize(msg))

      currentState = State.userState.get(nick, None)
      if currentState is None:
         validStates = State.initial_states
      else:
         validStates = currentState.nextStates()

      print currentState


      confidence = map(stateTest, [(msg_tag, state) for state in State.states if State.validateState(state, validStates)])

      print confidence

      ((conf, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)

      if conf < 0.1:
         if not nick in State.userState or State.userState[nick] != State:
            State.userState[nick] = State
            return State.query(nick, msg)
         else:
            return None

      State.userState[nick] = state

      context['_nick'] = nick
      return state.respond(context)

   @staticmethod
   def userJoin(user, timestamp):
      print user + " joined the channel!"
      for state in State.states:
         state.onUserJoin(user, timestamp)

   @staticmethod
   def userLeave(user, timestamp):
      print user + " left the channel...." 
      for state in State.states:
         state.onUserLeave(user, timestamp)

   @staticmethod
   def recognize(msg):
      return (0, {})

   @staticmethod
   def respond(context):
      pass

   @staticmethod
   def nextStates():
      return tuple([State])

   @staticmethod
   def onUserJoin(user, timestamp):
      pass

   @staticmethod
   def onUserLeave(user, timestamp):
      pass
