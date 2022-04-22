import requests
import csv
import time

startTime = time.time()

# =========== =========== ===========#
# ===== Set your Variables here ======
# =========== =========== ===========#

domain = "DOMAIN.okta.com"  # <------------------------ Replace DOMAIN with your Okta Domain
apikey = "APIKEY"           # <------------------------ Replace APIKEY with your Okta API Key
filename = "out.csv"        # <------------------------ Name the file what you want.

url = "https://{}/api/v1/users?filter=status eq \"ACTIVE\"".format(domain)
payload={}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'SSWS ' + str(apikey)
}

response = requests.get(url, headers=headers)
users = response.json()
links = response.links

while 'next' in links:
  url=links['next']['url']
  response = requests.get(url, headers=headers)
  next_users = response.json()
  users += next_users
  links = response.links

uidList = []
loginList = []

for s in range(len(users)):
  if users[s]["id"]:
    uid = users[s]["id"]
    uidList.append(uid)

for s in range(len(users)):
  if users[s]["profile"]["login"]:
    login = users[s]["profile"]["login"]
    loginList.append(login)

fields = ['Username', 'UserId', 'Factors']
c = 0

with open(filename, 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(fields)
  for uid in uidList:
    url = "https://{}/api/v1/users/{}/factors".format(domain, uid)
    payload={}
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': 'SSWS ' + str(apikey)
    }

    response = requests.get(url, headers=headers)
    factors_out = response.json()
    factorList = []

    for s in range(len(factors_out)):
      if factors_out[s]["factorType"]:
        factorList.append(factors_out[s]["factorType"])
    row = loginList[c],uidList[c],factorList
    csvwriter.writerow(row)
    c += 1
    #time.sleep(0.5)    # <------------------------ This is an optional delay (in seconds). Not needed unless rate limits hit

executionTime = (time.time() - startTime)
print('Execution time (seconds): ' + str(executionTime))
