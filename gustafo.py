import sys

#import bot
from gustafobot import GustafoBot
from adapters.ircadapter import IRCAdapter

def main():
   if len(sys.argv) != 4:
       print "Usage: testbot <server[:port]> <channel> <nickname>"
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
      port = 6667
   channel = sys.argv[2]
   nickname = sys.argv[3]

   bot = GustafoBot(IRCAdapter(channel, nickname, server, port))
   bot.start()

if __name__ == "__main__":
   main()
