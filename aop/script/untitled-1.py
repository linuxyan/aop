from gevent import monkey; monkey.patch_all()

def read_url(url):
    response = urllib2.urlopen(url)
    body = response.read()
a = gevent.spawn(read_url, 'http://gevent.org')
b = gevent.spawn(read_url, 'http://python.org')
gevent.joinall([a, b])