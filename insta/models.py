from django.contrib.auth.hashers import make_password
from django.db import models

class BaseLoginModel(models.Model):
	last_login = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)


	class Meta:
		abstract = True


class BaseTimeModel(models.Model):
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now=True)


	class Meta:
		abstract = True


# Create your models here.
class Insta(BaseLoginModel):
	name = models.CharField(
		max_length=120,
		null=True,
		blank=True,
		unique=True
		)


	password = models.TextField(
		null=True,
		blank=True,
	)

	IP = models.GenericIPAddressField()

