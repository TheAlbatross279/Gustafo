class Adapter(object):
   def __init__(self):
      self.bot = None

   def start(self, bot):
      self.bot = bot

   def send_message(self, nick, msg):
      pass

   def get_users(self):
      return []

   def get_name(self):
      return "Gustafo"
