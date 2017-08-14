# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.template import Context,loader
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from.forms import PostForm,CommentForm
from django.shortcuts import render,get_object_or_404,redirect
from.models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User
from notifications.signals import notify
from.models import Friend
import datetime


@user_passes_test(lambda u: u.is_superuser)
def post_create(request):
	#if not  request.user.is_authenticated():
		#aise Http404

	form=PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.author = request.user
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
		messages.success(request,"Successfully Created")
		notify.send(user, recipient=user, verb='new post')

	else:
		messages.error(request,"there is an error")
	context={
	"form":form,

	}
	return render(request,"blog/post_form.html",context)

def post_detail(request,slug):
	instance =get_object_or_404(Post,slug=slug)
	initial_data={
			"content_type":instance.get_content_type,
			"object_id":instance.id

	}

	form=CommentForm(request.POST or None,initial=initial_data)
	if form.is_valid():
		c_type=form.cleaned_data.get("content_type")
		content_type =ContentType.objects.get(model=c_type)
		obj_id=form.cleaned_data.get("object_id")
		content_data= form.cleaned_data.get("content")
		parent_obj= None
		try: 
			parent_id =int(request.POST.get("parent_id"))
		except:
			parent_id= None 

		if parent_id:
			parent_qs= Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj=parent_qs.first()


		new_comment,created =Comment.objects.get_or_create(
									user=request.user,
									content_type=content_type,
									object_id=obj_id,
									content=content_data,
									parent=parent_obj,)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	comments=Comment.objects.filter_by_instance(instance)
    
	context={
	"title":instance.title,
	"instance":instance,
	"comments":comments,
	"comment_form":form,
	}
	return render(request,"blog/detail.html",context)

def post_list(request):
	if request.user.is_authenticated():
		queryset_list= Post.objects.all().order_by("-timestamp")
		users= User.objects.all()
		try:
			friend=Friend.objects.get(current_user=request.user)
			friends=friend.users.all()
		except Friend.DoesNotExist:
			friends=None
		query =request.GET.get("q")
		if query:
			queryset_list=queryset_list.filter(
				Q(title__icontains=query)|
				Q(author__first_name__icontains=query)|
				Q(content__icontains=query)
				)

		paginator=Paginator(queryset_list,5)
		page_request_var="page"
		page =request.GET.get(page_request_var )
		try:
			queryset= paginator.page(page)
		except PageNotAnInteger:
			queryset=paginator.page(1)
		except EmptyPage:
			queryset=paginator.page(paginator.num_pages)

		context={
			"objects_list":queryset,
			"title":"Recent posts",
			"page_request_var":page_request_var,
			"users":users,
			"friends":friends,
			}
		return render(request,"blog/index.html", context)
	else:
		queryset_list= Post.objects.all().order_by("-timestamp")
		users= User.objects.all()
		query =request.GET.get("q")
		if query:
			queryset_list=queryset_list.filter(
				Q(title__icontains=query)|
				Q(author__first_name__icontains=query)|
				Q(content__icontains=query)
				)

		paginator=Paginator(queryset_list,5)
		page_request_var="page"
		page =request.GET.get(page_request_var )
		try:
			queryset= paginator.page(page)
		except PageNotAnInteger:
			queryset=paginator.page(1)
		except EmptyPage:
			queryset=paginator.page(paginator.num_pages)

		context={
			"objects_list":queryset,
			"title":"Recent posts",
			"page_request_var":page_request_var,
			"users":users,
			}
 		return render(request,"blog/index2.html",context)


def post_update(request,slug=None):
	instance =get_object_or_404(Post,slug=slug)
	form=PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Saved",extra_tags='some-tag')
		return HttpResponseRedirect(instance.get_absolute_url())

	context={
		"title":instance.title,
		"instance":instance,
		"form":form,

		}
	return render(request,"blog/post_form.html",context)

	


def post_delete(request,id ):
	instance =get_object_or_404(Post,pk=id)
	instance.delete()
	messages.success(request,"Successfully deleted",extra_tags='some-tag')
	return redirect("blog:list")
	
def change_friends(request, operation, pk):
	friend =User.objects.get(pk=pk)
	if operation =='add':
		Friend.make_friend(request.user, friend)

	elif operation == 'lose':
		Friend.lose_friend(request.user, friend)
	return redirect ('/blog/')
def archives(request):
	posts=Post.objects.filter().order_by("-date")
	now=datetime.datetime.now()


	post_dict ={}
	for i in range (posts[0].date.year,posts[len(posts)-1].date.year-1,-1):
		post_dict[i]={}
		for month in range(1,13):
			post_dict[i][month]=[]
	for post in posts:
		post_dict[post.date.year][post.date.month].append(post)

	post_sorted_keys =list(reversed(sorted(post_dict.keys())))
	list_posts=[]

	for key in post_sorted_keys:
		adict={key:post_dict[key]}
		list_posts.append(adict)
	
	context={
		'now':now,
		"list_posts":list_posts,
		}
	return render(request,"blog/archives.html",context)






