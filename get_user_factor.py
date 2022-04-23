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
nameList = []

for s in range(len(users)):
  if users[s]["id"]:
    uid = users[s]["id"]
    uidList.append(uid)

for s in range(len(users)):
  if users[s]["profile"]["login"]:
    login = users[s]["profile"]["login"]
    loginList.append(login)

for s in range(len(users)):
  if users[s]["profile"]["firstName"]:
    first = users[s]["profile"]["firstName"]
  if users[s]["profile"]["lastName"]:
    last = users[s]["profile"]["lastName"]
  name = first + ' ' + last
  nameList.append(name)

fields = ['Name', 'Username', 'UserId', 'Factors']
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

    if len(factors_out) == 0:
      factorList.append("None")
    else:
      for s in range(len(factors_out)):
        if factors_out[s]["factorType"]:
          if factors_out[s]["provider"] == 'OKTA':
            if factors_out[s]["factorType"] == 'push':
              factorList.append("Okta Verify Push")
            elif factors_out[s]["factorType"] == 'token:software:totp':
              factorList.append("Okta Verify")
            elif factors_out[s]["factorType"] == 'email':
              factorList.append("Email")
            elif factors_out[s]["factorType"] == 'sms':
              factorList.append("SMS")
            elif factors_out[s]["factorType"] == 'call':
              factorList.append("Call")
            elif factors_out[s]["factorType"] == 'question':
              factorList.append("Security Question")
          elif factors_out[s]["provider"] == 'GOOGLE' and factors_out[s]["factorType"] == 'token:software:totp':
            factorList.append("Google Authenticator")
          elif factors_out[s]["provider"] == 'DUO' and factors_out[s]["factorType"] == 'web':
            factorList.append("DUO")
          elif factors_out[s]["provider"] == 'FIDO' and factors_out[s]["factorType"] == 'webauthn':
            factorList.append("WebAuthn")
          elif factors_out[s]["provider"] == 'RSA' and factors_out[s]["factorType"] == 'token':
            factorList.append("RSA Token")
          elif factors_out[s]["provider"] == 'SYMANTEC' and factors_out[s]["factorType"] == 'token':
            factorList.append("Symantec Token")
          elif factors_out[s]["provider"] == 'YUBICO' and factors_out[s]["factorType"] == 'token:hardware':
            factorList.append("Yubikey")
          else:
            factorList.append(factors_out[s]["factorType"])
    row = nameList[c],loginList[c],uidList[c],factorList
    csvwriter.writerow(row)
    c += 1
    #time.sleep(0.5)    # <------------------------ This is an optional delay (in seconds). Not needed unless rate limits hit

executionTime = (time.time() - startTime)
print('Execution time (seconds): ' + str(executionTime))
