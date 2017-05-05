from google.appengine.ext import ndb


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
