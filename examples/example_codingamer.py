import codingame

client = codingame.Client()

# get a codingamer from their pseudo or public handle
codingamer = client.get_codingamer("a pseudo or public handle here")
print(codingamer)
print(codingamer.pseudo)
print(codingamer.public_handle)
print(codingamer.avatar_url)
