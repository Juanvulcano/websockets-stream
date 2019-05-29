from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from Levenshtein import distance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from social_core.backends.twitch import TwitchOAuth2
from twitch import TwitchClient
from .models import Event


# Create your views here.
def index(request):
    return render(request, 'index.html')

@permission_classes((IsAuthenticated,))
def home(request):
    user = request.user
    social = user.social_auth.get(provider='twitch')
    client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token=social.extra_data['access_token'])
    get_followers(request)
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
        sorting_dict = {}
        for channel in channels:
    	    levenshtein_distance = distance(search_query, channel.display_name)
    	    if levenshtein_distance in sorting_dict:
    		    sorting_dict[levenshtein_distance] =  sorting_dict[levenshtein_distance] + [channel.display_name]
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
    This function creates an event for all the followed channels of our user
    It returns a json with the information of all the followers of our user
    """
    user = request.user
    social = user.social_auth.get(provider='twitch')
    client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token=social.extra_data['access_token'])
    follows = client.users.get_follows(social.uid)
    for follower in follows:
        previously_followed = Event.objects.filter(user=user, streamer_id=follower['channel'].id, event_type="Followed user")
        if not previously_followed:
            Event.objects.create(user=user, streamer_id=follower['channel'].id, event_type="Followed user")
    return JsonResponse({'follows': follows})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def follow_user(request, user_id):
    """
    This function follows a streamer as long as the last follow event is older
    than the last unfollow event.
    """
    user = request.user
    social = user.social_auth.get(provider='twitch')
    client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token=social.extra_data['access_token'])
    last_follow = Event.objects.filter(user=user, streamer_id=user_id, event_type="Followed user").order_by('-id').first()
    last_unfollow = Event.objects.filter(user=user, streamer_id=user_id, event_type="Unfollowed user").order_by('-id').first()


    if last_follow:
        if last_unfollow:
            time1 = last_follow._meta.get_field('created_at').value_from_object(last_follow)
            time2 = last_unfollow._meta.get_field('created_at').value_from_object(last_unfollow)
            if (time1-time2).total_seconds() > 0:
            	return(JsonResponse({"follows": "User was already following this channel"}))
            else:
                Event.objects.create(user=user, streamer_id=user_id, event_type="Followed user")
                return(JsonResponse({'follows': client.users.follow_channel(social.uid, user_id)}))
        return(JsonResponse({"follows": "User was already following this channel"}))
    Event.objects.create(user=user, streamer_id=user_id, event_type="Followed user")
    return(JsonResponse({'follows': client.users.follow_channel(social.uid, user_id)}))

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def unfollow_user(request, user_id):
    """
    This function unfollows a user as long as the last follow event is more recent than the last
    unfollow event.
    """
    user = request.user
    social = user.social_auth.get(provider='twitch')
    client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token=social.extra_data['access_token'])
    last_follow = Event.objects.filter(user=user, streamer_id=user_id, event_type="Followed user").order_by('-id').first()
    last_unfollow = Event.objects.filter(user=user, streamer_id=user_id, event_type="Unfollowed user").order_by('-id').first()

    if not last_follow:
        return(JsonResponse({"response:" "User was not following this channel"}))

    if last_follow:
        if last_unfollow:
            time1 = last_follow._meta.get_field('created_at').value_from_object(last_follow)
            time2 = last_unfollow._meta.get_field('created_at').value_from_object(last_unfollow)
            if (time1-time2).total_seconds() > 0:
                Event.objects.create(user=user, streamer_id=user_id, event_type="Unfollowed user")
                client.users.unfollow_channel(social.uid, user_id)
                return(JsonResponse({"response": "User succesfully unfollowed"}))
            else:
                return(JsonResponse({"response": "User was not following this channel"}))
        Event.objects.create(user=user, streamer_id=user_id, event_type="Unfollowed user")
        client.users.unfollow_channel(social.uid, user_id)
        return JsonResponse({'response': "User succesfully unfollowed"})  

def logout(request):
    """This function logs out an authenticated user"""
    auth_logout(request)
    return render(request, 'home.html')
