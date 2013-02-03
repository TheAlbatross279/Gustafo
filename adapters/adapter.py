class Adapter(object):
   '''
   An adapter represents a connection to some sort of user-interface which can send and receive
   messages.
   '''

   def __init__(self):
      '''
      Initialization of the adapter. This should NEVER initiate a connection. All subclasses must
      super this method.
      '''
      self.bot = None

   def start(self, bot):
      '''
      Start the adapter. This is where the connection will be initialized. All subclasses must
      super this method.
      '''
      self.bot = bot

   def send_message(self, nick, msg):
      '''
      This is the method the Bot will call to send a message to the user. Takes in the nickname of
      the receiving user and the message to be sent.
      '''
      pass

   def get_users(self):
      '''
      Return all users currently present in the room. If the interface has no concept of users,
      return an empty list.
      '''
      return []

   def get_name(self):
      '''
      Return the name which has been assigned to the bot by the adapter.
      '''
      return "Gustafo"
