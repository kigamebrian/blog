from __future__ import unicode_literals
from django.shortcuts import render,redirect
from accounts.forms import (
	RegistrationForm,
	EditProfileForm,About,
	

	
	)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from forms import ContactForm
from blog.models import Post
from django.contrib import messages




def register(request):
	
	if request.method=='POST':
		form =RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form=RegistrationForm()
		args ={'form':form,}
		return render(request,'accounts/reg_form.html',args)

@login_required(login_url='/account/login/')
def profile(request, pk=None):
	user =request.user
	user_posts = Post.objects.filter(author=request.user).order_by("-timestamp")
	if pk:
		user = User.objects.get(pk=pk)
		
	else:
		user= request.user
	args={'user':user,'user_posts':user_posts}
	return render(request,'accounts/profile.html',args)

def edit_profile(request,pk=None):
	user =request.user
	user_profile =user.userprofile
	if request.method =='POST':

		form=EditProfileForm(request.POST,instance=request.user)

		if form.is_valid():
			user_profile.city =request.POST['city']
			user_profile.first_name =request.POST['first_name']
			user_profile.last_name =request.POST['last_name']
			user_profile.username =request.POST['username']
			user_profile.user = user
			user_profile.email = request.POST['email']
			user_profile.description = request.POST['description']
			user_profile.phone = request.POST['phone']
			user_profile.website = request.POST['website']
			user_profile.save()
			messages.success(request,('Your profile was successfully updated!'))

			return redirect('/account/profile')


	else:

		form =EditProfileForm(instance=request.user)
		args={'form':form}

		return render(request,'accounts/edit_profile.html',args)



def change_password(request):
	if request.method=='POST':
		form=PasswordChangeForm(data=request.POST,user=request.user_profile)

		if form.is_valid():
			form.save()

			update_session_auth_hash(request,form.user)
			return redirect('/account/profile')

	else:
		form=PasswordChangeForm(user=request.user)
		args={'form':form}

		return render(request,'accounts/changepassword.html',args ) 

def about(request):
	form=About()
	return render(request,'accounts/about.html',{'form':form})

def Contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			topic = form.cleaned_data['topic']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			send_mail('Feedback from your site, topic: %s' % topic,message, sender,
				['b.kigame@yahoo.com'])
			return HttpResponseRedirect('/blog/')
	else:
		form = ContactForm()
	return render(request,'accounts/contact.html', {'form': form})