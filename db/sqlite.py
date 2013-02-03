from conn import Connection

import sqlite3

class SQLiteConn(Connection):
   '''
   Represents a connection to a SQLite3 database.
   '''

   def __init__(self, filepath):
      '''
      Initialize a connection to the database given a filepath.
      '''
      self.connection = sqlite3.connect(filepath)
      self.cursor = self.connection.cursor()

   def query(self, query, commit=False):
      '''
      Send a SQL query to the database. By default, results are NOT commited. Returns a list of
      results as tuples
      '''
      self.cursor.execute(query)
      if commit:
         self.connection.commit()

      return [result for result in self.cursor]

   def close(self):
      '''
      Close the connection to the database.
      '''
      self.connection.close()
