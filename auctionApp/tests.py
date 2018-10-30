from django.test import TestCase, RequestFactory
from django.core import mail
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from datetime import datetime
from .views import email_view

# Create your tests here.
class SimpleTest(TestCase):
    fixtures = ['db_data.json',]

    def setUp(self):
        pass