#!/usr/bin/env python

from cgi import escape as htmlescape
import json
import pkgutil
import random

from twisted.application import internet, service
from twisted.web import server, resource, error

from adapter import *

__all__ = ['WebAdapter']

# TODO(ross): Refactor event codes into bot/bot.py interface.
#             Currently, GustafoBot is tightly coupled to IRCAdapter.
JOIN = 0x1
DIE = 0x2
USER_JOIN = 0x3
USER_EXIT = 0x4
# END

class _Resource(resource.Resource):
   def __init__(self, adapter, log):
      resource.Resource.__init__(self)
      self._adapter = adapter
      self._log = log

   def render_GET(self, request):
      new_username = 'user' + str(random.randint(10000, 99999))
      self._log.new_box(new_username)
      request.setHeader('Content-Type', 'text/html; charset=utf-8')
      return """<!DOCTYPE html>
<html>
<head>
   <title>Gustafo</title>
   <link rel="stylesheet" type="text/css" href="/style.css">
</head>
<body>
   <div id="column">
      <h1>Gustafo</h1>
      <div id="chatRecord"></div>
      <div id="inputLine">
         <form action="/" method="POST">
            <input type="hidden" name="user" value="%s" size="10">
            &gt; <span id="userName">%s</span>:
            <input type="text" name="m" size="30" x-webkit-speech>
            <input type="submit" value="Send">
         </form>
      </div>
   </div>
   <script type="text/javascript" src="/jquery-1.9.1.js"></script>
   <script type="text/javascript" src="/chat.js"></script>
</body>
</html>
""" % (htmlescape(new_username), htmlescape(new_username))

   def render_POST(self, request):
      if request.args.get("join"):
         join_user = request.args["join"][0]
         self._log.new_box(join_user)
         self._adapter.bot.on_event(USER_JOIN, {'nick': join_user})
         return ""
      else:
         user = request.args["user"][0]
         line = request.args["m"][0]
         self._log.add_message(user + ': ' + line)
         self._adapter.bot.on_message(user, line)
         request.setResponseCode(204)
         return ""

class _LogResource(resource.Resource):
   def __init__(self):
      resource.Resource.__init__(self)
      self._boxes = {}

   def add_message(self, msg):
      """Add a message to everyone's box."""
      for box in self._boxes.itervalues():
         box.append(msg)

   def new_box(self, user):
      """Create a message box for a new user."""
      self._boxes.setdefault(user, [])

   def fetch_messages(self, user):
      """Get and clear the message box for a user."""
      box = self._boxes.setdefault(user, [])
      boxCopy = list(box)
      del box[:]
      return boxCopy

   def render_POST(self, request):
      user_arg = request.args.get("user", [])
      if not user_arg:
         return error.NoResource()
      request.setHeader('Content-Type', 'application/json; charset=utf-8')
      return json.dumps(self.fetch_messages(user_arg[0]))

class _StaticResource(resource.Resource):
   def __init__(self, name, mime_type):
      resource.Resource.__init__(self)
      self._data = pkgutil.get_data(__name__, name)
      self._mime_type = mime_type
   
   def render_GET(self, request):
      request.setHeader('Content-Type', self._mime_type)
      return self._data

class WebAdapter(Adapter):
   # TODO(ross): Again, GustafoBot requires this undocumented field
   nickname = 'gustafo'

   def __init__(self, port=8080):
      super(WebAdapter, self).__init__()
      self.port = port

   def start(self, bot):
      super(WebAdapter, self).start(bot)

      self.logResource = _LogResource()

      # TODO(ross): stubbing
      #self.bot.on_event(JOIN)

      root = resource.Resource()
      root.putChild("", _Resource(self, self.logResource))
      root.putChild("log", self.logResource)
      for name in ['jquery-1.9.1.js', 'chat.js']:
         root.putChild(name, _StaticResource(name, 'text/javascript'))
      for name in ['style.css']:
         root.putChild(name, _StaticResource(name, 'text/css'))
      site = server.Site(root)

      from twisted.internet import reactor
      reactor.listenTCP(self.port, site)
      reactor.run()

   def send_message(self, nick, msg):
      print msg
      self.logResource.add_message(msg)

   def get_users(self):
      return ['user', 'gustafo']

# vim: ft=python et ts=8 sts=3 sw=3 tw=100
