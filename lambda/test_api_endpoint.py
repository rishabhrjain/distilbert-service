import requests

url = 'YOUR API GATEWAY URL'

event = {"context":"some context", "text":"i love the movie. It was really good"}

x = requests.post(url, json = event)

print(x.json())