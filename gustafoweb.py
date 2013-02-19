#!/usr/bin/env python

import sys

#import bot
from bot import Bot
from adapters.webadapter import WebAdapter

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

   bot = Bot(WebAdapter(port))
   bot.start()

if __name__ == "__main__":
   main()
