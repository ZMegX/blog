from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from users.models import Profile

for user in User.objects.all():
    Profile.objects.get_or_create(user=user)