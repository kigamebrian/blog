# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import Post,Comment,Friend,SystemErrorLog

class PostAdmin(admin.ModelAdmin):
    exclude = ('author',)
    list_display=('title','updated','timestamp','author','date')
    prepopulated_fields = { 'slug': ['title'] }
    

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PostAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return Entry.objects.all()
        return Entry.objects.filter(author=request.user)    


    def queryset(self, request):
        if request.user.is_superuser:
            return Entry.objects.all()
        return Entry.objects.filter(author=request.user)
	


	
admin.site.register(Post,PostAdmin)
admin.site.register(Friend)

admin.site.register(Comment)

class SystemErrorLogAdmin(admin.ModelAdmin):
    ordering = ('-timestamp',)
    list_display = ('level', 'message', 'timestamp',)
    list_filter = ('level',)
    search_fields = ('level','message',)

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('level', 'message', 'timestamp')
admin.site.register(SystemErrorLog, SystemErrorLogAdmin)