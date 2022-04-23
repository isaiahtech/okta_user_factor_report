# okta_user_factor_report
This script performs similar operations to the built-in Okta MFA Usage report.
It produces a CSV file with the Name, Username, UserID, and Factors (in single cell)
Output will look similar to the following in raw form:

```
Name,Username,UserId,Factors
Day Sun,daysun@oktaice.local,00u10eskk0LQ2svth5d7,"['Okta Verify Push', 'Okta Verify']"
bari creed,bari.creed@experiment.app,00u10m6nf2z8nlfZs5d7,"['SMS', 'Okta Verify Push', 'Okta Verify']"
Cat Neko,cat.neko@daysun.org,00u11w52kcLiPIpSB5d7,['None']
```

The script is built to support pagination/multiple calls to enumerate all users.

Execution time for listing 100 users was around 20-22 seconds.
This will result in about 300 requests-per-minute, half of the maximum rate limit okta has by default for the endpoints used (600).
This should leave plenty of room for normal/other operations without encountering rate limit issues.
