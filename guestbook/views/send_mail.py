# -*- coding: utf-8 -*-
from google.appengine.api import  mail


def send_mail(sender, subject, content):
	message = mail.EmailMessage(
		sender=sender,
		subject=subject,
		body=content
	)
	message.to = "admin <admin@example.com>"
	message.send()
