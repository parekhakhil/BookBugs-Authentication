from django.urls import re_path,path

from . import views
app_name='authapp'
urlpatterns = [
    path('accounts/profile/',views.profile_redirector,name='user_profile'),
    path('accounts/profile/update/',views.UserProfileUpdateView.as_view(),name='user_profile_update'),
    re_path(r'^@(?P<username>[\w-]+)/$', views.UserProfileView.as_view(), name='profile'),
]