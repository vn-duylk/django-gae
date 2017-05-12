# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	'''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
	return ndb.Key('GuestBook', guestbook_name)


class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
	date_update = ndb.DateTimeProperty(auto_now=True)
	updated_by = ndb.UserProperty()

	@classmethod
	def get_greeting(self, guestbook_name):
		greeting_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(
			-Greeting.date)
		greetings = greeting_query.fetch(10)
		return greetings

	@classmethod
	def get_guestbook_by_id(self, guestbook_id, guestbook_name):
		entity = Greeting.get_by_id(guestbook_id, guestbook_key(guestbook_name))
		return entity

	def to_resource_dict(self, guestbook_name):
		context = {
			'content': self.content,
			'guestbook_id': self.key.id(),
			'url': 'api/v1/' + guestbook_name + '/' + str(self.key.id()),
			'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
		}
		if self.author:
			context['author'] = self.author.email()
		if self.updated_by:
			context['updated_by'] = self.updated_by.email()
			context['date_update'] = self.date_update.strftime("%Y-%m-%d %H:%M:%S")
		return context
