from twitch import TwitchClient

client = TwitchClient(client_id='ktzzjqubnpvb95qw4146ssdjl3zwz5')
channel = client.channels.get_by_id('Juanvulcano')

print(channel.id)
print(channel.name)
print(channel.display_name)
