from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('twitchsocial', views.index, name='index'),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout")
    # ex: /polls/5/
]