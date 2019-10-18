from twisted.internet import reactor
from twisted.web import proxy, server

site = server.Site(proxy.ReverseProxyResource('127.0.0.1', 8080, b''))
reactor.listenTCP(8666, site)
reactor.run()
