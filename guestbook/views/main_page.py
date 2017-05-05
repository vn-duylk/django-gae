from django.views.generic import TemplateView
from google.appengine.api import users
from guestbook.models import Greeting, DEFAULT_GUESTBOOK_NAME
from guestbook.models import guestbook_key

class IndexView(TemplateView):

	template_name = "guestbook/index_page.html"
	model = Greeting

	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greeting_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(
			-Greeting.date)
		greetings = greeting_query.fetch(10)
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'

		context = super(IndexView, self).get_context_data(**kwargs)
		context['greetings'] = greetings
		context['guestbook_name'] = guestbook_name
		context['url_linktext'] = url_linktext
		context['url'] = url
		return context
