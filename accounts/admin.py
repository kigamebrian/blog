# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from accounts.models import UserProfile,About



class UserProfileAdmin(admin.ModelAdmin):
	list_display=('user','user_infor','city','website','phone')


	def user_infor(self,obj):
		return obj.description

	def get_queryset(self,request):

		queryset=super(UserProfileAdmin,self).get_queryset(request)
		queryset=queryset.order_by('phone')
		return queryset


	user_infor.short_description ='infor'
class AboutAdmin(admin.ModelAdmin):
	list_display=('mission',)

admin.site.register(UserProfile,UserProfileAdmin)


admin.site.register(About,AboutAdmin)




 