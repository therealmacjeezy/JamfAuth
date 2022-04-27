import json, getpass, requests, keyring

def check_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig):
    if apiToken:
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {apiToken}'}
        apiResponse = requests.get(theURL, headers=headers)

        print(f'status code: {apiResponse.status_code}')

        if apiResponse.status_code != 200:
            if apiResponse.status_code == 401:
                print('[>jamfAuth] Your token is invalid :(, attempting to renew it.. hold tight..\n')
                keep_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)
        else:
            print('[Jamf Pro API Token Status]: Valid')
            return apiToken
    else:
        get_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)


def keep_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig):
    theURL = baseAPIURL+'auth/keep-alive'
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {apiToken}'}
    apiResponse = requests.post(theURL, headers=headers)
    if apiResponse.status_code != 200:
        if apiResponse.status_code == 401:
            print('[>jamfAuth] Your token is invalid and cannot be renewed. Why dont we get a new one..\n')
            keyring.delete_password(baseAPIURL, apiUser+'API')
            get_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)
            return apiToken
    else:
        print('[>jamfAuth] Renewed the API token successfully.')
        return apiToken

def get_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig):
    ## check for stored creds first
    try:
        apiPassword = keyring.get_password(baseAPIURL, apiUser)
        if not apiPassword:
            print('[>jamfAuth] Unable to find keychain entry. lets make one shall we?')
            apiPassword = getpass.getpass(f'What is the password for {apiUser}: ')
            keyring.set_password(baseAPIURL, apiUser, apiPassword)
    except Exception as errorMessage:
        print(f'get_token: error doing keychain things..\n{errorMessage}')
    theURL = baseAPIURL+'auth/token'
    headers = {'accept': 'application/json'}

    apiResponse = requests.post(theURL,auth=(apiUser,apiPassword), headers=headers)

    try:
        apiResponseJSON = apiResponse.json()
        try:
            apiToken = apiResponseJSON['token']

            apiTokenKeychain = keyring.get_password(baseAPIURL, apiUser+'API')

            if not apiTokenKeychain:
                keyring.set_password(baseAPIURL, apiUser+'API', apiToken)
                print('[>jamfAuth] API Token saved to keychain.')

            return apiToken
        except Exception as errorMessage:
            validToken = False
            print(f'ERROR [get_token(apiToken)]: {errorMessage}')
        else:
            print(f'[get_token]: Saved API Token..\n')
    except Exception as errorMessage:
        print(f'ERROR [get_token(apiResponseJSON)]: {errorMessage}\n')
