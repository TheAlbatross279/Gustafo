#!/usr/bin/env python

import pkgutil

from twisted.application import internet, service
from twisted.web import server, resource

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
   def __init__(self, adapter):
      resource.Resource.__init__(self)
      self._adapter = adapter

   def render_GET(self, request):
      request.setHeader('Content-Type', 'text/html; charset=utf-8')
      return """<!DOCTYPE html>
<html>
<head>
   <title>Gustafo</title>
</head>
<body>
   <div id="chatRecord">&nbsp;</div>
   <div id="inputLine">
      <form action="/" method="POST">
         &gt; <input type="text" name="m">
         <input type="submit" value="Send">
      </form>
   </div>
</body>
</html>
"""

   def render_POST(self, request):
      line = request.args["m"][0]
      self._adapter.bot.on_message("user", line)
      return """<!DOCTYPE html>
<html>
<head>
   <title>Gustafo</title>
</head>
<body>
   <div id="chatRecord">&nbsp;</div>
   <div id="inputLine">
      <form action="/" method="POST">
         &gt; <input type="text" name="m">
         <input type="submit" value="Send">
      </form>
   </div>
</body>
</html>
"""

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

      self.bot.on_event(JOIN)
      # TODO(ross): We should be taking in user info
      #self.bot.on_event(USER_JOIN, {'nick': 'user'})

      root = resource.Resource()
      root.putChild("", _Resource(self))
      root.putChild('jquery-1.9.1.js', _StaticResource('jquery-1.9.1.js', 'text/javascript'))
      site = server.Site(root)

      from twisted.internet import reactor
      reactor.listenTCP(self.port, site)
      reactor.run()

   def send_message(self, msg):
      print msg

   def get_users(self):
      return ['user', 'gustafo']

# vim: ft=python et ts=8 sts=3 sw=3 tw=100
