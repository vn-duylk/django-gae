from _greeting import Greeting
from google.appengine.ext import ndb


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	'''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
	return ndb.Key('GuestBook', guestbook_name)
