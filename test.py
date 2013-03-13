from bot import *
from adapters.cliadapter import CLIAdapter
from random import randint

class Beemo(Bot):
   def on_event(self, event, data={}):
      if event is USER_JOIN:
         if randint(0, 1) is 1:
            self.adapter.send_message(data['nick'], "Hello. How are you?")


beemo = Beemo(CLIAdapter())

beemo.start()
