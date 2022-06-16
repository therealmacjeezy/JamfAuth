# jamfAuth Examples

## Usage Examples
Below are four examples of how to use jamfAuth with your script. For complete example scripts, see the **Script Examples** section below. 

### python [production server]
```python
from jamfAuth import *

### Use jamfAuth to start and handle the API Authentication then save it as the variable "apiToken"
apiToken=startAuth()

#[...continue with script...]
```

### python [development server]
```python
from jamfAuth import *

### Use jamfAuth to start and handle the API Authentication then save it as the variable "apiToken"
apiToken=startAuth("dev")

#[...continue with script...]
```

### bash [production server]
```shell
#!/bin/bash

### This function kicks off jamfAuth and captures the API Token saved in the keychain
startAuth() {
    ### Use jamfAuth to start and handle the API Authentication
    python3 -c 'from jamfAuth import *; startAuth()'

    jamfHostname=$(grep -o '"jamfHostName": "[^"]*' /path/to/jamfAuth/support/.jamfauth.json | grep -o '[^"]*$')

    apiUsername=$(grep -o '"apiUserName": "[^"]*' /path/to/jamfAuth/support/.jamfauth.json | grep -o '[^"]*$')

    ### Use python3's keyring to get the API Token from the keychain
    apiToken=$(python3 -c 'import keyring; print(keyring.get_password("https://'$jamfHostname'/api/v1/", "'${apiUsername}API'"))')
}

### Call the function
startAuth

#[...continue with script...]
```

### bash [development server]
```shell
#!/bin/bash

### This function kicks off jamfAuth and captures the API Token saved in the keychain
startAuth() {
    ### Use jamfAuth to start and handle the API Authentication
    python3 -c 'from jamfAuth import *; startAuth("dev")'

    jamfHostname=$(grep -o '"jamfHostName": "[^"]*' /path/to/jamfAuth/support/.jamfauth.json | grep -o '[^"]*$')

    apiUsername=$(grep -o '"apiUserName": "[^"]*' /path/to/jamfAuth/support/.jamfauth.json | grep -o '[^"]*$')

    ### Use python3's keyring to get the API Token from the keychain
    apiToken=$(python3 -c 'import keyring; print(keyring.get_password("https://'$jamfHostname'/api/v1/", "'${apiUsername}API'"))')
}

### Call the function
startAuth

#[...continue with script...]
```

---
## Script Examples
I put together a few example scripts to show how jamfAuth can be used from start to finish. Each example script has been written in both bash and python.

### Get Last Known IP Address
Uses the system's serial number to get the last known IP Address for that system.

**Script Type** | **Name**
--- | ---
**python** | [`getLastKnownIP.py`](GetLastKnownIP/getLastKnownIP.py)
**BASH** | [`getLastKnownIP.sh`](GetLastKnownIP/getLastKnownIP.sh)

----
### Redeploy MDM Profile
Uses the system's serial number to get the Jamf Computer ID then uses that to redeploy the MDM Profile.

**Script Type** | **Name**
--- | ---
**python** | [`redeployMDM.py`](RedeployMDM/redeployMDM.py)
**BASH** | [`redeployMDM.sh`](RedeployMDM/redeployMDM.sh)


