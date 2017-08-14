# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.cache import cache 
import datetime
from brian import settings


class UserProfile(models.Model):
	user =models.OneToOneField(User)
	username=models.CharField(max_length=120,default='')
	first_name=models.CharField(max_length=200,default='')
	last_name=models.CharField(max_length=200,default='')
	email=models.EmailField(default='')
	description =models.TextField()
	city =models.CharField(default='',max_length=100)
	phone = models.IntegerField(default=07000000)
	website=models.URLField(default='',blank=True)
	image =models.ImageField(upload_to='profile_image',blank=True)
	

	def  create_profile(sender,**kwargs):
		if kwargs['created']:
			user_profile= UserProfile.objects.create(user= kwargs['instance'])

	post_save.connect(create_profile,sender=User)

	def last_seen(self):
		return cache.get('seen_%s' % self.user.username)

	def online(self):
		if self.last_seen():
			now = datetime.datetime.now()
			if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
				return False
			else:
				return True
		else:
			return False


class About(models.Model):

	
	about=models.TextField()
	mission=models.CharField(max_length=100,default="") 


	def __unicode__(self):
		return self.mission 

	def __str__(self):
		return self.mission