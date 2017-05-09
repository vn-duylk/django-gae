from google.appengine.api import taskqueue
from guestbook.views import send_mail
import webapp2
import logging


def add_task_queue(sender, content):
	task = taskqueue.add(
		url='/task_queue_handler',
		params={'sender': sender, 'subject': 'New greeting has been signed',
				'content': content})


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
