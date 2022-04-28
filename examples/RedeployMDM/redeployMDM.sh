#!/bin/bash

### Get the Serial Number of the System
serialNumber=$(system_profiler SPHardwareDataType | grep Serial | awk '{print $4}')

### This function kicks off jamfAuth and captures the API Token saved in the keychain
startAuth() {
    ### Use jamfAuth to start and handle the API Authentication
    python3 -c 'from jamfAuth import *; startAuth()'

    ### Use python3's keyring to get the API Token from the keychain
    apiToken=$(python3 -c 'import keyring; print(keyring.get_password("https://benderisgreat.jamfcloud.com/api/v1/", "mcfryAPI"))')
}

### Call the function
startAuth

### Get the Jamf Computer ID for this system using the serial number
computerID=$(curl -s "https://benderisgreat.jamfcloud.com/api/v1/computers-inventory?section=HARDWARE&filter=hardware.serialNumber==$serialNumber" -H "accept: application/json" -H "Authorization: Bearer $apiToken" | jq '.results[0].id'| tr -d '"')

if [[ ! -z "$computerID" ]]; then
    ### Redeploy the MDM Profile using the Jamf Computer ID
    redeployMDM=$(curl -s "https://benderisgreat.jamfcloud.com/api/v1/jamf-management-framework/redeploy/$computerID" -H "accept: application/json" -H "Authorization: Bearer $apiToken" -X POST)
    if [[ "$?" == "0" ]]; then
        echo "MDM Profile has been redeployed successfully to the system with serial number $serialNumber."
    fi
else
    echo "Unable to get the Jamf Computer ID for system with serial number $serialNumber"
fi