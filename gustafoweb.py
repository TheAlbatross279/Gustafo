#!/usr/bin/env python

import sys

#import bot
from bot import Bot
from adapters.webadapter import WebAdapter
from random import randint

class Beemo(Bot):
   def on_event(self, event, data={}):
      if event is USER_JOIN:
         if randint(0, 1) is 1:
            self.adapter.send_message(data['nick'], "Hello")

def main():
   if len(sys.argv) != 2:
       print "Usage: gustafoweb <server[:port]>"
       sys.exit(1)

   s = sys.argv[1].split(":", 1)
   server = s[0]
   if len(s) == 2:
      try:
         port = int(s[1])
      except ValueError:
         print "Error: Erroneous port."
         sys.exit(1)
   else:
      port = 8080

   bot = Beemo(WebAdapter(port))
   bot.start()

if __name__ == "__main__":
   main()
