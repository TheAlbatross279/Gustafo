from state import *

class Bot(object):
   def __init__(self, adapter):
      self.adapter = adapter

   def die(self):
      pass

   def start(self):
      self.adapter.start(self)

   def send_message(self, nick, msg):
      self.adapter.send_message(nick, msg)

   def on_event(self, event, data={}):
      pass

   def on_message(self, user, msg):
      res = state.State.query(user, msg)

      if res is not None:
         self.send_message(user, res)
