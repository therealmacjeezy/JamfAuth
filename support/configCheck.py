import json, os

def check_config(jamfSearchConfig):
    if os.path.exists(jamfSearchConfig) == False:
        print('..why no config? Lets make you one..')
        data = {
            'apiUserName' : '',
            'jamfHostName' : '',
            'jamfAPIURL' : ''
            # 'apiToken' : ''
        }

        with open(jamfSearchConfig, 'w') as output:
            json.dump(data, output)


def reset_config():
    pwd = os.getcwd()
    jamfSearchConfig = pwd+f'/support/.jamfauth.json'
    data = {
        'apiUserName' : '',
        'jamfHostName' : '',
        'jamfAPIURL' : ''
        # 'apiToken' : ''
    }

    with open(jamfSearchConfig, 'w') as output:
        json.dump(data, output)


def start_config_check(jamfSearchConfig):
    with open(jamfSearchConfig, 'r') as f:
        data = json.load(f)

    host_check(data['jamfHostName'], jamfSearchConfig, data['jamfAPIURL'])
    user_check(data['apiUserName'], jamfSearchConfig, data['jamfAPIURL'])

def host_check(jamfHost, jamfSearchConfig, baseAPIURL):
    if jamfHost:
        print(f'[Jamf Pro Host Name]: {jamfHost}')
    else:
        jamfHost = input(f'Enter the Jamf Pro URL (without https://): \n\t=> ')
        try:
            with open(jamfSearchConfig, 'r') as f:
                data = json.load(f)

            with open(jamfSearchConfig, 'w') as d:
                data['jamfHostName'] = jamfHost
                data['jamfAPIURL'] = f"https://{jamfHost}/api/v1/"
                json.dump(data, d)
                
        except Exception as errorMessage:
            print(f'Unable to save Jamf Pro HostName to Local Config File..\n')

    if baseAPIURL:
        print(f'[Jamf Pro API URL]: {baseAPIURL}')
    else:
        try:
            with open(jamfSearchConfig, 'r') as f:
                data = json.load(f)

            with open(jamfSearchConfig, 'w') as d:
                data['jamfAPIURL'] = f"https://{jamfHost}/api/v1/"
                json.dump(data, d)
                
        except Exception as errorMessage:
            print(f'Unable to save Jamf Pro API URL to Local Config File..\n')

def user_check(apiUser, jamfSearchConfig, baseAPIURL):
    if apiUser:
        print(f'[Jamf Pro API Username]: {apiUser}')
    else:
        apiUser = input(f'Enter the Username for API Access: \n\t=> ')
    
        try:
            with open(jamfSearchConfig, 'r') as f:
                data = json.load(f)

            with open(jamfSearchConfig, 'w') as d:
                data['apiUserName'] = apiUser
                json.dump(data, d)
                
        except Exception as errorMessage:
            print(f'Unable to save Jamf Pro API Username to Local Config File..\n')
