from google.appengine.ext import ndb
#
#
# DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
#
#
# def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
# 	'''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
# 	return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
