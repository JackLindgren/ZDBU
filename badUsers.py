import requests
import json
import getpass

# get the username and password securely so it's not sitting in the code here:
email = raw_input('Enter your Zendesk username: ')
pwd  = getpass.getpass('Enter your Zendesk password: ')
org  = raw_input('Enter your organization: ')

# only interested in end users
url = "https://{0}.zendesk.com/api/v2/users.json?role=end-user".format(org)

userIDs = []

while url:
	response = requests.get(url, auth=(email, pwd))
	data = response.json()
	for user in data['users']:
		userIDs.append(user['id'])
	url = data['next_page']

badUsers = {}

for userID in userIDs[:1]:
	url = "https://{0}.zendesk.com/api/v2/users/{1}/identities.json".format(org, userID)
	response = requests.get(url, auth=(email, pwd))
	data = response.json()
	for identity in data['identities']:
		if identity['type'] == "email":
			idURL = "https://{0}.zendesk.com/api/v2/users/{1}/identities/{2}.json".format(org, userID, identity['id'])
			response = requests.get(url, auth=(email, pwd))
			data = response.json()
			for identity in data['identities']:
				if identity['deliverable_state'] != 'deliverable':
					badUsers[identity['value']] = int(identity['undeliverable_count'])
					# badUsers.append({identity['value]']: int(identity['undeliverable_count'])})

f = open('badUsers.csv', 'w')
for entry in badUsers.keys():
	f.write("{0},{1}\n".format(entry, badUsers[entry]))

f.close()