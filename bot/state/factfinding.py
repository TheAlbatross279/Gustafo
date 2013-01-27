from state import State
from db.fact import Fact
from db import SQLiteConn

class FindGossip(State):
    db = SQLiteConn('db/gossip.db')

    @staticmethod
    def respond(context):
        f = Fact(context['author'], context['msg'], context['recipient'], context['knowers'])
        tup = f.to_list()

        prefix = "INSERT INTO facts VALUES (" 
        suffix = ")"
        #build query
        query = prefix + "'"+ '\', \''.join(tup) +"'"+ suffix
 
        FindGossip.db.query(query, True)

State.register(FindGossip)
