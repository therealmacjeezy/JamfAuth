# JamfAuth

A python script to authenticate with the Jamf Pro API.

----
## About
This python script will authenticate you with your Jamf Pro server and get you an API Token (valid for 30 minutes) for Jamf Pro. 

The script uses a JSON file (`support/.jamfsearch.json`) to store the following data:
 - apiUserName
 - jamfHostName
 - jamfAPIURL
 - apiToken

Here is how `jamfAuth.py` works:
 - The script will first check to see if the JSON file exists or not. 
   - If not, it will prompt you to enter the above information
   - Once the information is entered, it will check the local keychain for the API Password and attempt to get an API Token.
     - If the API Password isn't found in the local keychain, it will prompt you to enter the password then start the process of getting an API token.
 - Next if an apiToken is found, it will check if it's valid or not
   - If it's not valid, it will attempt to renew it using `keep-alive`
   - If the renew fails, it will check the local keychain for the API Password and attempt to get a new API Token.
     - If the API Password isn't found in the local keychain, it will prompt you to enter the password
   - If the renew is successful, the API Token will be saved to the JSON file

Once you have a valid API Token, you can store it as a variable and use it when performing API calls later in the script.

---
### Importing into a script
```
from jamfAuth import *

apiPassword = startAuth()

if apiPassword:
    print('You can now use the apiToken variable to authenticate with your Jamf Pro API.')
    print(f'apiToken: \n{apiPassword}')
```