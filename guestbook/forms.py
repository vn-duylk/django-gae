# -*- coding: utf-8 -*-
from django import forms


class SignForm(forms.Form):
	name = forms.CharField(label='Name', max_length=100)
	message = forms.CharField(widget=forms.Textarea, max_length=1000, required=True)


class UpdateForm(forms.Form):
	guestbook_id = forms.CharField(widget=forms.HiddenInput())
	name = forms.CharField(label='Name', max_length=100)
	message = forms.CharField(widget=forms.Textarea, max_length=1000, required=True)
