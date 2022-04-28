from jamfAuth import *
import json, requests, subprocess

def getSerialNumber():
    system_profile_data = subprocess.Popen(['system_profiler', '-json', 'SPHardwareDataType'], stdout=subprocess.PIPE)
    data = json.loads(system_profile_data.stdout.read())
    global serial_number
    serial_number = data.get('SPHardwareDataType', {})[0].get('serial_number')

### Use jamfAuth to start and handle the API Authentication and save it as the variable apiToken
apiToken=startAuth()

### Call the function to get the system's Serial Number
getSerialNumber()

### Base API URL for your Jamf Pro Server
apiURL = 'https://benderisgreat.jamfcloud.com/api/v1/'

### Searches the GENERAL section of the computers-inventory and filters the results by Serial Number
apiSearchFilter = f'computers-inventory?section=GENERAL&filter=hardware.serialNumber=={serial_number}'

### API Call Header.. This contains the API Token 
headers = {'accept': 'application/json', 'Authorization': f'Bearer {apiToken}'}

apiResults = requests.get(apiURL+apiSearchFilter, headers=headers)

if apiResults.status_code == 200:
    apiResultsJSON = apiResults.json()
    try:
        ### Get the Last Reported IP Address from the API Results
        jamfComputerID = apiResultsJSON['results'][0]['id']
        ### This kicks off the API Call to redeploy the MDM Profile
        mdmDeploy = requests.post(f'{apiURL}jamf-management-framework/redeploy/{jamfComputerID}', headers=headers)
        if mdmDeploy.status_code == 202:
            print(f'\nThe MDM Profile has been successfully deployed to the system with serial number {serial_number}.')
        if mdmDeploy.status_code == 404:
            print(f'\nUnable to find a computer with the Jamf Computer ID of {jamfComputerID}.')
    except:
        print(f'\nUnable to find the Jamf Computer ID for the system with serial number {serial_number}')
else:
    print('\noops.. something broke\n\t[apiResults.status_code]: {apiResults.status_code}')