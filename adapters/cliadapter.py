import readline
from adapter import *

class CLIAdapter(Adapter):
   def __init__(self):
      super(CLIAdapter, self).__init__()

   def start(self, bot):
      super(CLIAdapter, self).start(bot)

      while True:
         line = raw_input("> ")
         if line == "quit":
            return
         self.bot.on_message("user", line)

   def send_message(self, nick, msg):
      print msg
