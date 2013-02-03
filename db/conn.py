class Connection(object):
   '''
   Represents a connection to a database. Any subclasses must implement the following methods.
   '''

   def __init__(self):
      '''
      This is where the connection should be initialized. Add any parameters necessary.
      '''
      pass

   def query(self, query):
      '''
      Query the database.
      '''
      pass

   def close(self):
      '''
      Do any cleanup necessary and close the connection. The Bot can call this method at any time.
      '''
      pass
