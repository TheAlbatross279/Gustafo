from conn import Connection
import psycopg2

class HelpConnection(Connection):
   '''
   Represents a connection to the postgres database.
   '''

   def __init__(self):
      '''
      This is where the connection is initialized.
      '''
      self.connection = psycopg2.connect(database='mydb', user='postgres', password='password')
      self.cursor = self.connection.cursor()

   def query(self, query, commit=False):
      '''
      Query the database.
      '''
      rtn = None
      if isinstance(query, tuple):
         self.cursor.execute(query[0], query[1])
      else:
         self.cursor.execute(query)
      
      if commit:
         self.connection.commit()
      else:
         rtn = self.cursor.fetchmany(1000);

      return rtn


   def close(self):
      '''
      Do any cleanup necessary and close the connection. The Bot can call this method at any time.
      '''
      self.connection.close()
