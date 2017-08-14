from django.conf.urls import url,include
from django.contrib import admin
from.import views


urlpatterns=[
	url(r'^$',views.post_list,name='list'),
	url(r'^create/$',views.post_create,name='create'),
	url(r'^delete/(?P<pk>\d+)/$',views.post_delete,name='delete'),
	url(r'^archives/$',views.archives,name='archives'),
	url(r'^edit/(?P<slug>[-\W]+)$',views.post_update,name='update'),
	url(r'^detail/(?P<slug>[-\w]+)$',views.post_detail,name='detail'),
	url(r'^connect/(?P<operation>.+)(?P<pk>\d+)/$',views.change_friends, name='change_friends'),
	

	
	
]