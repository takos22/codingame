import codingame

client = codingame.Client()

# get a codingamer from his public handle
me = client.get_codingamer("your handle here")
print(me)
print(me.pseudo)
print(me.public_handle)
print(me.avatar_url)
