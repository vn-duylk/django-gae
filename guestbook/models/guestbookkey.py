from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

class GuestBookKey(ndb.Model):

	@staticmethod
	def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
		'''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
		return ndb.Key('Guestbook', guestbook_name)
