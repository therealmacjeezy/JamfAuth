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

### Get the Last Known IP Address for the system
lastknownIP=$(curl -s "https://benderisgreat.jamfcloud.com/api/v1/computers-inventory?section=GENERAL&filter=hardware.serialNumber==$serialNumber" -H "accept: application/json" -H "Authorization: Bearer $apiToken" | jq '.results[0].general|.lastReportedIp'| tr -d '"')

if [[ "$lastknownIP" != 'null' ]]; then
    echo "This is the last known IP Address for the system with serial number $serialNumber:" 
    echo "$lastknownIP"
else
    echo "Unable to find the last known IP Address for the system with serial number $serialNumber"
fi