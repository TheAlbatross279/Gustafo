from state import *

JOIN = 0x1
DIE = 0x2
USER_JOIN = 0x3
USER_EXIT = 0x4

class Bot(object):
   '''
   The Bot class holds all the pieces together and is in charge of passing messages between the
   states and adapter.   
   '''

   def __init__(self, adapter):
      '''
      Initialize the bot with a given adapter. All subclasses must super this method.
      '''
      self.adapter = adapter

   def die(self):
      '''
      Kill the bot. Any necessary cleanup should be done here.
      '''
      pass

   def start(self):
      '''
      Start the bot. This will call through and start the adapter. All subclasses must super this
      method AFTER they do their own processing. This is a blocking operation.
      '''
      self.adapter.start(self)

   def send_message(self, nick, msg):
      '''
      Sends a message through to the adapter.
      '''
      self.adapter.send_message(nick, msg)

   def on_event(self, event, data={}):
      '''
      Called by the adapter. This method may chose to respond to any adapter specific events.
      Event codes and their data are to be outlined by the adapter itself.
      '''
      pass

   def on_message(self, user, msg):
      '''
      Called by the adapter when a message directed at the bot is received. It will query all the
      states for a response and send it back to the adapter.
      '''
      res = state.State.query(user, msg)

      if res is not None:
         self.send_message(user, res)
