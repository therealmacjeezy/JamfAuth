from jamfAuth import *
import json, requests, subprocess

def getSerialNumber():
    system_profile_data = subprocess.Popen(['system_profiler', '-json', 'SPHardwareDataType'], stdout=subprocess.PIPE)
    data = json.loads(system_profile_data.stdout.read())
    global serial_number
    serial_number = data.get('SPHardwareDataType', {})[0].get('serial_number')

### Use jamfAuth to start and handle the API Authentication and save it as the variable apiToken
apiToken=startAuth()

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
        lastReportedIP = apiResultsJSON['results'][0]['general']['lastReportedIp']
        print(f'\nThis is the last known IP Address for the system with serial number {serial_number}:\n{lastReportedIP}')
    except:
        print(f'\nUnable to find the last known IP Address for the system with serial number {serial_number}')
else:
    print('\noops.. something broke\n\t[apiResults.status_code]: {apiResults.status_code}')