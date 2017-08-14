# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import datetime



def upload_location(instance,filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	author=models.ForeignKey(User)
	title=models.CharField(max_length=100)
	slug=models.SlugField(unique=True)
	image =models.ImageField(blank=True,null=True,width_field="width_field",height_field="height_field",upload_to='images')
	height_field=models.IntegerField(default=0)
	width_field=models.IntegerField(default=0)
	content =models.TextField()
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	date=models.DateField(auto_now_add=True, blank=True)
	
	class Meta:
		permissions = (

			("can_add_pose", "can add post"),
			("can_change_post", "can change post"),
			("can_delete_post", "can delete post"),




			)
	

	def __unicode__(self):
		return self.title 

	def __str__(self):
		return self.title

	@property
	def get_content_type(self):
		instance=self
		content_type=ContentType.objects.get_for_model(instance.__class__)
		return content_type


	def get_absolute_url(self):
		return reverse("blog:detail",kwargs={"slug":self.slug})

def create_slug(instance, new_slug=None):
	slug= slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists= qs.exists()
	if exists:
		new_slug= "%s-%s" %(slug, qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug
	


def pre_save_post_reciever(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug= create_slug(instance)
		
			
pre_save.connect(pre_save_post_reciever,sender=Post) 

class CommentManager(models.Manager):
	def all(self):
		qs= super(CommentManager,self).filter(parent=None)
		return qs

	def filter_by_instance(self,instance):
		content_type=ContentType.objects.get_for_model(instance.__class__)
		obj_id=instance.id
		qs=super(CommentManager, self).filter(content_type=content_type,object_id= obj_id).filter(parent=None)
		return qs

class Comment(models.Model):
	user= models.ForeignKey(settings.AUTH_USER_MODEL,default=1)

	content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id= models.PositiveIntegerField(null=True)
	content_object= GenericForeignKey('content_type','object_id')
	parent =models.ForeignKey("self",null=True,blank=True)

	content =models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)

	objects=CommentManager()
	class Meta:
		ordering =['timestamp']


	def __unicode__(self):
		return str(self.user.username)

	def __str__(self):
		return str(self.user.username)
	def children(self):
		return Comment.objects.filter(parent=self)
	
	@property
	def is_parent(self):
		if self.parent is not None:
			return False
			
		return True
class Friend(models.Model):
	users = models.ManyToManyField(User)
	current_user=models.ForeignKey(User, related_name= 'owner', null= True)


	@classmethod

	def make_friend(cls,current_user, new_friend):
		friend, created= cls.objects.get_or_create(
			current_user= current_user
			)
		friend.users.add(new_friend)

	@classmethod

	def lose_friend(cls,current_user, new_friend):
		friend, created= cls.objects.get_or_create(
			current_user= current_user
			)
		friend.users.remove(new_friend)

class SystemErrorLog(models.Model):
    level = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField('timestamp', null=True, blank=True)
