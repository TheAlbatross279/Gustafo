import sqlite3 

class Database(object):
    def __init__(self):
        self.connection = sqlite3.connect('database/gossip.db')
        self.c = self.connection.cursor()

    def add_row(self, values):
        prefix = "INSERT INTO facts VALUES (" 
        suffix = ")"
        #build query
        query = prefix + "'"+ '\', \''.join(values) +"'"+ suffix
        self.c.execute(query)
        #(commit) the changes
        self.connection.commit()

    def close_conn(self):
        self.connection.close()
     
    def query(self, query):
        self.c.execute(query)
        results = []
        for row in self.c:
            results.append(row)

        return results

    def update(self, update_statement):
        self.c.execute(update_statement)
        self.connection.commit()

    def drop_tables(self):
        self.c.execute("DROP TABLE facts")
        self.c.execute('''CREATE TABLE facts
             (author text, msg text, recipient text, knowers text)''')

    def build_tables(self):
        self.c.execute('''CREATE TABLE facts
             (author text, msg text, recipient text, knowers text)''')



if __name__ == '__main__':
   db = Database()
   db.build_tables()
