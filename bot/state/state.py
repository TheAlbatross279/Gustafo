from multiprocessing import Pool, cpu_count
from nltk import pos_tag, word_tokenize
from processor.nlp.filter.normalTokFilter import NormalTokFilter

def state_test((msg, state)):
   return (state.recognize(msg), state)

class State:
   '''
   Represents a state of conversation which the user can be in. All user-defined states must
   subclass this class.
   '''

   users = []
   '''
   Current users present in the room.
   '''

   states = []
   '''
   List of all known states
   '''

   initial_states = []
   '''
   List of all states the user could possibly start in.
   '''

   user_state = {}
   '''
   Keeps track of what state each user is currently in. This allows the bot to hold a
   conversation with multiple users.
   '''

   @staticmethod
   def forget():
      '''
      Forget all user states.
      '''
      State.user_state = {}

   @staticmethod
   def register(state, isInitial=False):
      '''
      Register a state. This makes a user-defined state known to the bot. It can also be specified
      that this state should be considered an initial state. This method will also call the given
      state's init() method.
      '''
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
      '''
      Force a user into a specific state.
      '''
      if context.get('_nick', None) is not None:
         State.user_state[context['_nick']] = state

      return state.respond(context)

   @staticmethod
   def query(nick, msg):
      '''
      Query the valid states. This method will take in a message from the user and return the
      bot's response.
      '''

#      msg_tag = pos_tag(word_tokenize(msg))
      msg_filter = NormalTokFilter()
      msg_tag = msg_filter.filter(msg)
      current_state = State.user_state.get(nick, None)
      if current_state is None:
         valid_states = State.initial_states
      else:
         # Unclean method to make help states work correctly
         if current_state.next_states():
            valid_states = current_state.next_states()
         else:
            valid_states = State.initial_states

      #print current_state
      #print 'valid',valid_states
      #print 'current',current_state
      if not valid_states:
          return None
      else:
          confidence = map(state_test, [(msg_tag, state) for state in State.states if State.validate_state(state, valid_states)])

      #print confidence

      ((conf, context), state) = reduce(lambda x, y: x if x[0][0] > y[0][0] else y, confidence)
      #print 'state', state

      if conf < 0.1:
         State.user_state[nick] = None
         return None
         #if not nick in State.user_state or State.user_state[nick] != State:
         #   State.user_state[nick] = State
         #   return State.query(nick, msg)
         #else:
         #   return None

      State.user_state[nick] = state

      context['_nick'] = nick
      return state.respond(context)

   @staticmethod
   def init():
      '''
      Do any setup needed by the state. This will likely include creating a connection to a
      database. This method is called when the state is registered.
      '''
      pass

   
   @staticmethod
   def die():
      '''
      Called when the Bot is told to die. Allows states to do any necessary cleanup. This will
      typically entail closing a database connection.
      '''
      pass

   @staticmethod
   def recognize(msg):
     return (0, {})

   @staticmethod
   def respond(context):
      pass

   @staticmethod
   def next_states():
      return None
