from django.db import models
from django.contrib.auth.models import User
import datetime

class avatar(models.Model):
	user = models.OneToOneField(User)
	image = models.ImageField(upload_to = 'images/', default = 'images/None/no-img.jpg')

class Profile(models.Model):
	user = models.OneToOneField(User)
	profile = models.CharField(max_length=100000)
	def __str__(self):
			return self.profile

class Reiting(models.Model):
	user = models.OneToOneField(User)
	reiting = models.CharField(max_length=1000)
	howmany = models.CharField(max_length=1000)


class Celebr(models.Model):
	user = models.ForeignKey(User)
	index = models.CharField(max_length=100000)
	name = models.CharField(max_length=100000)
	descript = models.TextField()
	thing = models.CharField(max_length=100000)
	kategory = models.CharField(max_length=10000)
	adress = models.CharField(max_length=100000)
	incoords = models.CharField(max_length=100000)
	count = models.CharField(max_length=100000)
	maybecount = models.CharField(max_length=100000)
	last = models.CharField(max_length=10000)
	date = models.DateTimeField(default=datetime.datetime.now())
	quantity = models.CharField(max_length=1000000)
	can = models.CharField(max_length=100)
	def __str__(self):
			return self.name

class Your(models.Model):
	user = models.ForeignKey(User)
	yourcelebrinfo = models.ForeignKey(Celebr)
	date = models.DateTimeField(default=datetime.datetime.now())
	yourcelebr = models.CharField(max_length=10000)
	def __str__(self):
			return self.yourcelebr

class MaybeYour(models.Model):
	user = models.ForeignKey(User)
	yourcelebr = models.CharField(max_length=10000)
	def __str__(self):
			return self.yourcelebr

class Favourites(models.Model):
	user = models.ForeignKey(User)
	favourite = models.CharField(max_length=10000)
	def __str__(self):
			return self.favourite

class Members(models.Model):
	cele = models.ForeignKey(Celebr)
	member = models.ForeignKey(User)
	ochenen = models.CharField(max_length=1000)
class MaybeMembers(models.Model):
	cele = models.ForeignKey(Celebr)
	member = models.ForeignKey(User)

class Mybuh(models.Model):
	user = models.OneToOneField(User)
	mybuh = models.CharField(max_length=100000)
	def __str__(self):
			return self.mybuh

class Yetbuh(models.Model):
	user = models.OneToOneField(User)
	yetbuh = models.CharField(max_length=100000)
	def __str__(self):
			return self.yetbuh


class Friend(models.Model):
	user = models.ForeignKey(User, related_name="user")
	friend = models.ForeignKey(User, related_name="friend")

class MaybeFriend(models.Model):
	user = models.ForeignKey(User, related_name="muser")
	friend = models.ForeignKey(User, related_name="mfriend")

class Messages(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=10000000)
	mestype = models.CharField(max_length=100000)
	ahref = models.CharField(max_length=10000000)
	profilename = models.CharField(max_length=1000000)
	date = models.DateTimeField()

class HaveMessages(models.Model):
	user = models.OneToOneField(User)
	havemes = models.CharField(max_length=100000)

class OnlineMes(models.Model):
	user = models.ForeignKey(User, related_name="mesuser")
	message = models.TextField()
	readed = models.CharField(max_length=1000)
	message_id = models.CharField(max_length=100000)
	to = models.ForeignKey(User, related_name="to")

