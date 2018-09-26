#!/usr/bin/python3
import requests
import json

def printContent(request):
  print(json.dumps(r.json(), indent=3))

r = requests.get("http://127.0.0.1:5000/")
r.status_code           # Should be 200
r.json()                # The json body of the request as a Python dictionary
printContent(r)         # Prints the json body of the request
r.headers               # A dictionary of the provided headers

## Write your code in what follows. You can include comments describing what you are doing.

#Objective 1
user_name = requests.get("http://127.0.0.1:5000/user")
random_user = user_name.text[27:32]
address = "http://127.0.0.1:5000/"
user_name = requests.get(address + "user/" + random_user)
print(user_name.text)

#Objective 2
names = {"first" : "Benedict", "last" : "Cumberbatch"} 
new_user = requests.post("http://127.0.0.1:5000/user",json=names)
newUserLocation = new_user.headers['Location']

