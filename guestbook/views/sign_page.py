from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from google.appengine.api import users
from google.appengine.ext import ndb
from guestbook.forms import SignForm
from guestbook.models import Greeting
from guestbook.models import guestbook_key

class SignView(FormView):
	template_name = "guestbook/sign_page.html"
	form_class = SignForm
	success_url = reverse_lazy('indexview')

	def get_context_data(self, **kwargs):
		context = super(SignView, self).get_context_data(**kwargs)
		context['guestbook_name'] = self.get_guestbook_name()
		return context

	def get_initial(self):
		initial = super(SignView, self).get_initial()
		initial['name'] = self.get_guestbook_name()
		return initial

	def get_success_url(self):
		url = reverse_lazy('indexview')
		return '%s?guestbook_name=%s' % (url, self.get_guestbook_name())

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name')
		return guestbook_name

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form, **kwargs):
		name = form.cleaned_data['name']
		message = form.cleaned_data['message']
		greeting = Greeting(parent=guestbook_key(name))
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.guestbook_name = name
		greeting.content = message

		@ndb.transactional(retries=4)
		def put_greeting():
			greeting.put()
		put_greeting()
		return super(SignView, self).form_valid(form, **kwargs)
