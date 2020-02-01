from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	"""
		username, password, email, firstname, surname
	"""
	number = models.IntegerField()

	def __str__(self):
		return self.user.username

class Ailment(models.Model):
	ailments = models.CharField(max_length=100)

	def __str__(self):
		return self.ailments

class Analysis(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	BG_CHOICES = (('A', 'a'), ('B', 'b'), ('AB', 'ab'), ('O', 'o'))
	GENDER_CHOICES = (('Male', 'M'), ('Female', 'F'))
	blood_group = models.CharField(max_length=50, choices=BG_CHOICES)
	height = models.IntegerField()
	weight = models.IntegerField()
	gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
	ailments = models.ManyToManyField(Ailment)

	def get_ailments(self):
		return ",\n".join([a.ailments for a in self.ailments.all()])

	def __str__(self):
		post = "'s analysis"
		return self.user.username + post

	class Meta:
		verbose_name_plural = "Analysis"