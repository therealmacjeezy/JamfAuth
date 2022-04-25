import json, getpass, requests, keyring

def check_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig):
    if apiToken:
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {apiToken}'}
        apiResponse = requests.get(theURL, headers=headers)

        if apiResponse.status_code != 200:
            if apiResponse.status_code == 401:
                print('Your token is invalid :(, attempting to renew it.. hold tight..\n')
                keep_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)
        else:
            # print('[Jamf Pro API Token Status]: Valid')
            return apiToken
    else:
        get_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)

def keep_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig):
    theURL = baseAPIURL+'auth/keep-alive'
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {apiToken}'}
    apiResponse = requests.post(theURL, headers=headers)
    if apiResponse.status_code != 200:
        if apiResponse.status_code == 401:
            print('Your token is invalid and cannot be renewed. Why dont we get a new one..\n')
            get_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)
            return apiToken
    else:
        print('Renewed the token successfully.')
        return apiToken

def get_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig):
    ## check for stored creds first
    try:
        print('get_token: looking for local creds..')
        apiPassword = keyring.get_password(apiUser, apiUser)
        if not apiPassword:
            print('get_token: unable to find keychain entry. lets make one shall we?')
            apiPassword = getpass.getpass(f'What is the password for {apiUser}: ')
            keyring.set_password(apiUser, apiUser, apiPassword)
    except Exception as errorMessage:
        print(f'get_token: error doing keychain things..\n{errorMessage}')
    theURL = baseAPIURL+'auth/token'
    headers = {'accept': 'application/json'}

    apiResponse = requests.post(theURL,auth=(apiUser,apiPassword), headers=headers)

    try:
        apiResponseJSON = apiResponse.json()
        try:
            apiToken = apiResponseJSON['token']

            with open(jamfSearchConfig, 'r') as f:
                data = json.load(f)

            with open(jamfSearchConfig, 'w') as d:
                data['apiToken'] = apiToken
                json.dump(data, d)

            validToken = True
            return apiToken
        except Exception as errorMessage:
            validToken = False
            print(f'ERROR [get_token(apiToken)]: {errorMessage}')
        else:
            print(f'[get_token]: Saved API Token..\n')
            validToken = True
    except Exception as errorMessage:
        print(f'ERROR [get_token(apiResponseJSON)]: {errorMessage}\n')
        validToken = False
