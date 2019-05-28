from twitch import TwitchClient

#client = TwitchClient(client_id='ktzzjqubnpvb95qw4146ssdjl3zwz5')
client = TwitchClient(client_id='9hfygng7md3x7maw2g4uko0ednm3hk', oauth_token='x9bdmjt1cmwrac4glcim49yygwuf4w')
resp = client.users.follow_channel(437701321, 129454141)
print(resp)
#channel = client.channels.get_by_id('')

#print(channel.id)
#print(channel.name)
#print(channel.display_name)
