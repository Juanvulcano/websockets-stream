from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from social_core.backends.twitch import TwitchOAuth2

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    user = request.user
    social = user.social_auth.get(provider='twitch')
    print(social.extra_data['access_token'])
    return render(request, 'home.html')


def get_followers(request):
    """
    This function returns a json with the ids of all the followers of our user
    """
    user = request.user
    social = user.social_auth.get(provider='twitch')
    print(social.extra_data['access_token'])
    print(social)
    print(social_extra_data)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render(request, 'home.html')

#def follow_user(request, username):
	# Will follow user
