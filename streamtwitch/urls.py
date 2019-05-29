from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('login', views.index, name='index'),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    path('search', views.search, name="search"),
    path('get_followers', views.get_followers, name='get_followers'),
    path('unfollow_user/<user_id>/', views.unfollow_user, name='unfollow_user'),
    path('follow_user/<user_id>/', views.follow_user, name="follow_user"),

    #url('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
    # ex: /polls/5/
]