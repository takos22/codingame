import codingame

client = codingame.Client()
client.login("email", "password")
# or
client = codingame.Client("email", "password")

# then you can access the logged in codingamer like this
print(client.logged_in)
print(client.codingamer)
print(client.codingamer.pseudo)
print(client.codingamer.public_handle)
print(client.codingamer.avatar_url)
