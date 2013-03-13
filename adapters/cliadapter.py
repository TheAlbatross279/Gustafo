import readline
from adapter import *

class CLIAdapter(Adapter):
   def __init__(self):
      super(CLIAdapter, self).__init__()

   def start(self, bot):
      super(CLIAdapter, self).start(bot)
      self.bot.on_event(USER_JOIN, {'nick': 'User'})

      while True:
         try:
            line = raw_input("> ")
         except (EOFError, KeyboardInterrupt):
            # print newline
            print
            return

         if line == "quit":
            return
         self.bot.on_message("User", line)

   def send_message(self, nick, msg):
      print msg
