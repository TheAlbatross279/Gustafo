import os
import time

class Logger(object):
   '''
   Logger is a logging module for Gustafo. Logger allows you to log messages to one of three files in
   the log/ directory.
   '''

   debug_file = None
   '''The debug file reference'''

   error_file = None
   '''The error file reference'''

   log_file = None
   '''The log file reference'''

   @staticmethod
   def debug(msg):
      '''
      Log a debug message. These messages should include information that is useful for testing, but
      should not be shown on a typical run.
      '''
      if Logger.debug_file is None:
         Logger.debug_file = open(os.path.join('log', 'debug_'+str(int(time.time() * 100))+'.log'), 'w')

      Logger.debug_file.write(msg + '\n\n')

   @staticmethod
   def error(msg):
      '''
      Log an error message. These messages should document any unexpected behavior that occurs during
      runtime.
      '''
      if Logger.error_file is None:
         Logger.error_file = open(os.path.join('log', 'error_'+str(int(time.time() * 100))+'.log'), 'w')

      Logger.error_file.write(msg + '\n\n')

   @staticmethod
   def log(msg):
      '''
      Log a log message. These messages should include expected output that provides useful
      information about the current run.
      '''
      if Logger.log_file is None:
         Logger.log_file = open(os.path.join('log', 'log_'+str(int(time.time() * 100))+'.log'), 'w')

      Logger.log_file.write(msg + '\n\n')
