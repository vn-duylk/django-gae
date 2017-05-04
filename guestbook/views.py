from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from guestbook import models
from django.core.urlresolvers import reverse_lazy
from guestbook.forms import SignForm
from google.appengine.api import users
from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME
import urllib
import logging

# def main_page(request):
# 	guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
#
# 	# Ancestor Queries, as shown here, are strongly consistent with the High
# 	# Replication Datastore. Queries that span entity groups are eventually
# 	# consistent. If we omitted the ancestor from this query there would be
# 	# a slight chance that Greeting that had just been written would not
# 	# show up in a query.
#
# 	greeting_query = Greeting.query(ancestor = guestbook_key(guestbook_name)).order(-Greeting.date)
# 	greetings = greeting_query.fetch(10)
#
# 	if users.get_current_user():
# 		url = users.create_logout_url(request.get_full_path())
# 		url_linktext = 'Logout'
# 	else:
# 		url = users.create_login_url(request.get_full_path())
# 		url_linktext = 'Login'
#
# 	template_values = {
# 		'greetings': greetings,
# 		'guestbook_name': guestbook_name,
# 		'url': url,
# 		'url_linktext': url_linktext,
# 	}
# 	return render(request, 'guestbook/main_page.html', template_values)
#
# def sign_post(request):
# 	if request.method == 'POST':
# 		guestbook_name = request.POST.get('guestbook_name')
# 		greeting = Greeting(parent=guestbook_key(guestbook_name))
#
# 		if users.get_current_user():
# 			greeting.author = users.get_current_user()
#
# 		greeting.content = request.POST.get('content')
# 		greeting.put()
# 		return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
# 	return HttpResponseRedirect('/')

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
		logging.info(self.get_guestbook_name())
		return initial

	def get_success_url(self):
		url = reverse_lazy('indexview')
		logging.info('get_success_url')
		logging.info(self.get_guestbook_name())
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
		greeting.put()
		return super(SignView, self).form_valid(form, **kwargs)










