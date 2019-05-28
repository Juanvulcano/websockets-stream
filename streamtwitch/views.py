from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from Levenshtein import distance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from social_core.backends.twitch import TwitchOAuth2
from twitch import TwitchClient


# Create your views here.
def index(request):
    return render(request, 'index.html')

@permission_classes((IsAuthenticated,))
def home(request):
    user = request.user
    social = user.social_auth.get(provider='twitch')
    client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token=social.extra_data['access_token'])
    return render(request, 'home.html')

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search(request):
    """
    This function returns a json list with up to 100 users by relevance using Levenshtein distance
    """
    user = request.user
    social = user.social_auth.get(provider='twitch')
    client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token=social.extra_data['access_token'])
    search_query = request.GET.get('search_box', None)
    if search_query:
        channels = client.search.channels(search_query, limit=100)
        print(channels)
        sorting_dict = {}
        for channel in channels:
    	    levenshtein_distance = distance(search_query, channel.display_name)
    	    if levenshtein_distance in sorting_dict:
    		    sorting_dict[levenshtein_distance] =  sorting_dict[levenshtein_distance] + [channel.display_name]#.append(channel.display_name)
    	    else:
    		    sorting_dict[levenshtein_distance] = [channel.display_name]
        users_list = []
        for key in sorted(sorting_dict.keys()):
    	    for user in sorting_dict[key]:
                users_list.append(user)
        return JsonResponse({'users':users_list})



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_followers(request):
    """
    This function returns a json with the ids of all the followers of our user
    """
    user = request.user
    social = user.social_auth.get(provider='twitch')
    client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token=social.extra_data['access_token'])

def logout(request):
    """This function logs out an authenticated user"""
    auth_logout(request)
    return render(request, 'home.html')

#def follow_user(request, username):
	# Will follow user
