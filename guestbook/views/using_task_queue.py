from google.appengine.api import taskqueue
import webapp2
import logging
from google.appengine.api import users
from guestbook.views import send_mail
from guestbook.models import Greeting


def add_task_queue():
	greeting = Greeting()
	task = taskqueue.add(
		url='/task_queue_handler',
		params={'sender': users.get_current_user(), 'subject': 'New greeting has been signed',
				'content': greeting.content})


class TaskQueueHandler(webapp2.RequestHandler):

	def post(self):

		logging.info('task_handle')
		sender = self.request.get('sender')
		subject = self.request.get('subject')
		content = self.request.get('content')
		logging.info(sender)
		send_mail.send_mail(sender, subject, content)

app = webapp2.WSGIApplication([
	('/task_queue_handler', TaskQueueHandler)
], debug=True)
