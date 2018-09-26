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
reply = requests.get("http://127.0.0.1:5000/user")
userDict = reply.json() #Change the list recieved into a dictionary
userString = userDict['users'][0]['link'] #Drill into the user
fullAddress = "http://127.0.0.1:5000" + userString #get the user-specific address
user_name = requests.get(fullAddress) #Request the user information

#Objective 2
names = {"first" : "Benedict", "last" : "Cumberbatch"} #New user's first and last name
new_user = requests.post("http://127.0.0.1:5000/user",json=names) #Send the information created above to the server
newUserLocation = new_user.headers['Location'] #Get the http adress of the user


#Objective 3
message = {"text": "The Imitation Game", "recipient": fullAddress} #Create the dictionary that contains the message
answer = requests.post(newUserLocation + "/message", json=message ) #Send the information to the server
updated= requests.get(newUserLocation+"/message")
print(updated.text)




