#!/usr/bin/env python

import pkgutil

from twisted.application import internet, service
from twisted.web import server, resource

from adapter import *

__all__ = ['WebAdapter']

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
      print line
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
   def __init__(self, port=8080):
      super(WebAdapter, self).__init__()
      self.port = port

   def start(self, bot):
      super(WebAdapter, self).start(bot)

      root = resource.Resource()
      root.putChild("", _Resource(self))
      site = server.Site(root)

      from twisted.internet import reactor
      reactor.listenTCP(self.port, site)
      reactor.run()

   def send_message(self, nick, msg):
      print msg

# vim: ft=python et ts=8 sts=3 sw=3 tw=100
