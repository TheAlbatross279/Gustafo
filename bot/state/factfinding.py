from state import State
from db.fact import Fact
from db.dbsetup import Database

class FindGossip(State):

    @staticmethod
    def respond(context):
        f = Fact(context['author'], context['msg'], context['recipient'], context['knowers'])
        tup = f.to_list()

        db = Database()
        db.add_row(tup)
        db.close_conn()

State.register(FindGossip)
