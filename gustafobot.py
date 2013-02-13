from bot import Bot
from adapters.ircadapter import *
from bot.state.state import State
from bot.state.outreach import InitialOutreach
from bot.state.solicitresponse import SolicitResponse
from bot.state.giveupstate import GiveUpState
from bot.state.factfinding import FindGossip
from bot.state.solicituser import SolicitUser
from db.dbsetup import Database
from threading import Timer
import random
import time

class GustafoBot(Bot):
   CHAT = 0
   TIMEOUT = 30.0

   def __init__(self, adapter):
      Bot.__init__(self, adapter) 

      self.idle = {}
      self.resume_state = {}

   def forget(self):
      for timer in self.idle.values():
         timer.cancel()

      self.idle = {}
      self.resume_state = {}
      State.forget()

      db = Database()
      db.drop_tables()
      db.close_conn()

      self.on_join()

   def die(self):
      State.die()
      for timer in self.idle.values():
         timer.cancel()

   def send_message(self, nick, msg):
      to_send = nick + ": " + msg

      self.adapter.send_message(to_send)

   def on_event(self, event, data={}):
      if event is USER_JOIN:
         self.on_user_join(data['nick'], time.time())
      elif event is USER_EXIT:
         self.on_user_exit(data['nick'], time.time())
      elif event is JOIN:
         self.on_join()
      elif event is DIE:
         self.die()

   def on_user_join(self, nick, timestamp):
      print "##### JOIN #####"

      knowers = self.adapter.get_users()
      knowers.remove(self.adapter.nickname)

      timestamp = time.strftime("%X", time.localtime())

      msg = "joined at " + timestamp

      context = {'author': nick,
                 'recipient': "",
                 'msg': msg,
                 'knowers': knowers}

      State.force_state(FindGossip, context)

   def on_user_exit(self, nick, timestamp):
      print "##### EXIT #####"

      knowers = self.adapter.get_users()
      knowers.remove(self.adapter.nickname)

      timestamp = time.strftime("%X", time.localtime())

      msg = "left at " + timestamp

      context = {'author': nick,
                 'recipient': "",
                 'msg': msg,
                 'knowers': knowers}

      State.force_state(FindGossip, context)

   def on_join(self):
      self.idle[GustafoBot.CHAT] = Timer(GustafoBot.TIMEOUT, self.on_chat_inactive)
      self.idle[GustafoBot.CHAT].start()

   def on_chat_inactive(self):
      State.users = self.adapter.get_users()

      users = self.adapter.get_users()
      users.remove(self.adapter.nickname)

      if "foaad" in users:
         user = "foaad"
      elif len(users) > 0:
         random.shuffle(users)
         user = users[0]
      else:
         self.idle[GustafoBot.CHAT] = Timer(GustafoBot.TIMEOUT, self.on_chat_inactive)

      res = State.force_state(InitialOutreach, {'_nick': user})
      if res is not None:
         self.send_message(user, res)

      self.idle[user] = Timer(GustafoBot.TIMEOUT, self.on_user_inactive, [user])
      self.idle[user].start()

   def on_user_inactive(self, nick):
      State.users = self.adapter.get_users()

      if State.user_state[nick] is not SolicitResponse:
         self.resume_state[nick] = State.user_state[nick]
         res = State.force_state(SolicitResponse, {'_nick': nick})
         #res = State.force_state(SolicitUser,{'_nick': nick})
         self.idle[nick] = Timer(GustafoBot.TIMEOUT, self.on_user_inactive, [nick])
         self.idle[nick].start()
      else:
         res = State.force_state(GiveUpState, {'_nick': nick})
         del(State.user_state[nick])
         del(self.idle[nick])
         if len(State.user_state) == 0:
            self.idle[GustafoBot.CHAT] = Timer(10.0, self.on_chat_inactive)
            self.idle[GustafoBot.CHAT].start()
      if res is not None:
         self.send_message(nick, res) 

   def on_message(self, user, msg):
      timestamp = time.time()
      self.idle[GustafoBot.CHAT].cancel()
      if self.idle.get(user, None) is not None:
         self.idle[user].cancel()
         if State.user_state[user] is SolicitResponse:
            State.user_state[user] = self.resume_state[user]

      it = time.time()

      print self.adapter.get_users()
      State.users = self.adapter.get_users()
      res = State.query(user, msg)

      rt = time.time()

      if rt - it < 3.0:
         print "Sleep:", 3.0 - (rt - it)
         time.sleep(3.0 - (rt - it))

      if res is not None:
         self.send_message(user, res)

      print user

      self.idle[user] = Timer(GustafoBot.TIMEOUT, self.on_user_inactive, [user])
      self.idle[user].start()

   def on_chat(self, t, f, msg):
      knowers = self.adapter.get_users()
      knowers.remove(self.adapter.nickname)
      context = {'author': f,
                 'recipient': t,
                 'msg': msg,
                 'knowers': knowers}

      State.force_state(FindGossip, context)
