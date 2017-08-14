from django.conf.urls import url,include
from. import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.views import login,logout,password_reset, password_reset_done, password_reset_confirm, password_reset_complete

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.




urlpatterns=[

	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^login/$',login,{'template_name':'accounts/login.html'},name='login'),
	url(r'^logout/$',logout,{'template_name':'accounts/logout.html'},name='logout'),
	url(r'^register/$',views.register,name='register'),
	url(r'^profile/$',views.profile,name='profile'),
	url(r'^contact/$',views.Contact,name='contact'),
	url(r'^profile/(?P<pk>\d+)/$',views.profile,name='profile_with_pk'),
	url(r'^profile/edit/$',views.edit_profile,name='edit'),
	url(r'^change-password/$',views.change_password,name='change_password'),
	url(r'^about/$',views.about,name='about'),
	url(r'^password_reset/$',password_reset, {'template_name':'/accounts/password_reset_email.html'     
		}, name='password_reset'),
    url(r'^password-reset/done/$',password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$',password_reset_complete, name='password_reset_complete'),
	

	
]
