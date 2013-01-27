from conn import Connection

import sqlite3

class SQLiteConn(Connection):
   def __init__(self, filepath):
      self.connection = sqlite3.connect(filepath)
      self.cursor = self.connection.cursor()

   def query(self, query, commit=False):
      self.cursor.execute(query)
      if commit:
         self.connection.commit()

      return [result for result in self.cursor]

   def close(self):
      self.connection.close()
