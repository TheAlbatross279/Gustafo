from state import *

class Bot(object):
   def __init__(self):
      pass

   def forget(self):
      pass

   def die(self):
      pass

   def send_message(self, nick, msg):
      pass

   def get_users(self):
      pass

   def on_join(self):
      pass

   def on_user_join(self, user, timestamp):
      pass

   def on_user_exit(self, user, timestamp):
      pass

   def on_chat(self, f, t, msg):
      pass

   def on_message(self, user, timestamp, msg):
      res = state.State.query(user, msg)

      if res is not None:
         self.send_message(user, res)
