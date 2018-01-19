from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
	noti_from = models.IntegerField(blank=False)
	overview = models.CharField(max_length=100,blank=False,default='')
	link = models.URLField(blank=True,default='')
	post_time = models.DateTimeField()

	def __str__(self):
		return str(self.overview)

class Journal(models.Model):
	category = models.IntegerField(blank=False)
	user_id = models.IntegerField(blank=False)
	post_time = models.DateTimeField(auto_now=True)
	content = models.TextField(blank=False)
	title = models.CharField(max_length=30,blank=False)

	def __str__(self):
		return str(self.title)

class Book(models.Model):
	title = models.CharField(max_length=30,blank=False,unique=True)
	author = models.CharField(max_length=30,blank=False)
	rate = models.FloatField(null=True,blank=True)
	comment = models.TextField(blank=True,default='')
	post_time = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(upload_to='book_images',blank=True,null=True)

	def __str__(self):
		return str(self.title)
class UserProfile(models.Model):
	user = models.OneToOneField(User,unique=True)


