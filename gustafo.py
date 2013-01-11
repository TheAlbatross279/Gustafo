import sys

#import bot
from gustafobot import GustafoBot

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

   GustafoBot(channel, nickname, server, port)

if __name__ == "__main__":
   main()
