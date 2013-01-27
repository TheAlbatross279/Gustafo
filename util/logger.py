import os
import time

class Logger(object):
   debug_file = None
   error_file = None
   log_file = None

   @staticmethod
   def debug(msg):
      if Logger.debug_file is None:
         Logger.debug_file = open(os.path.join('log', 'debug_'+str(int(time.time() * 100))+'.log'), 'w')

      Logger.debug_file.write(msg + '\n\n')

   @staticmethod
   def error(msg):
      if Logger.error_file is None:
         Logger.error_file = open(os.path.join('log', 'error_'+str(int(time.time() * 100))+'.log'), 'w')

      Logger.error_file.write(msg + '\n\n')

   @staticmethod
   def log(msg):
      if Logger.log_file is None:
         Logger.log_file = open(os.path.join('log', 'log_'+str(int(time.time() * 100))+'.log'), 'w')

      Logger.log_file.write(msg + '\n\n')
