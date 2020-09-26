import codingame

client = codingame.Client()

# get a pending public clash of code
coc = client.get_pending_clash_of_code()
# or get a clash of code from its public handle
coc = client.get_clash_of_code("clash of code handle here")

print(coc)
print(coc.join_url)
print(coc.modes)
print(coc.programming_languages)
print(coc.public_handle)
print(coc.players)
