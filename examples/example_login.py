import codingame

client = codingame.Client()
# see https://codingame.readthedocs.io/en/1.2.x/user_guide/quickstart.html#login
client.login(remember_me_cookie="your cookie here")

# then you can access the logged in codingamer like this
print(client.logged_in)
print(client.codingamer)
print(client.codingamer.pseudo)
print(client.codingamer.public_handle)
print(client.codingamer.avatar_url)
