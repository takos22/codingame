import codingame

client = codingame.Client()

# get a codingamer from his public handle
me = client.get_codingamer("your handle here")
print(me)
print(me.pseudo)
print(me.public_handle)
print(me.avatar_url)

# get a clash of code from its public handle
coc = client.get_clash_of_code("clash of code handle here")
print(coc)
print(coc.join_url)
print(coc.modes)
print(coc.programming_languages)
print(coc.public_handle)
print(coc.players)
