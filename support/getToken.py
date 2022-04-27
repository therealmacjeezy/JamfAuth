import json, getpass, requests, keyring, sys

def check_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig):
    if apiToken:
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {apiToken}'}
        apiResponse = requests.get(theURL, headers=headers)

        # print(f'status code: {apiResponse.status_code}')

        if apiResponse.status_code != 200:
            if apiResponse.status_code == 401:
                print('[>jamfAuth] Your token is invalid :(, attempting to renew it.. hold tight..')
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
            print('[>jamfAuth] Your token is invalid and cannot be renewed. Why dont we get a new one..')
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

    if apiResponse.status_code != 200:
        # Bad Request.. what were you thinking?!
        if apiResponse.status_code == 400:
            print(f'[>jamfAuth] Bad Request. Check the header and try again]')
            sys.exit('Bad Request.. oops.')

        # Unauthorized :(
        if apiResponse.status_code == 401:
            print('[>jamfAuth] Unauthorized. Lets try entering the password again.')
            # delete the keychain entry and create it again..
            keyring.delete_password(baseAPIURL, apiUser)
            apiPassword = getpass.getpass(f'What is the password for {apiUser}: ')
            keyring.set_password(baseAPIURL, apiUser, apiPassword)
            try:
                print('[>jamfAuth] Trying to get an API Token again..')
                apiResponse = requests.post(theURL,auth=(apiUser,apiPassword), headers=headers)
            except Exception as errorMessage:
                print(f'ERROR [>jamfAuth] Unable to get an API Token for {apiUser}. Make sure the password and permissions are correct for {apiUser}, then try again.')
                sys.exit(f'Unable to get API Token for {apiUser}')

        # Forbidden 0_o ..oops
        if apiResponse.status_code == 403:
            print(f'[>jamfAuth] Forbidden. Make sure the user {apiUser} has the correct access to perform API Authentication calls.')
            sys.exit(f'Forbidden. Double check the permissions for {apiUser}.')

        # Not Found ..yup.. totally lost right now.
        if apiResponse.status_code == 404:
            print('[>jamfAuth] Not Found. Check the Jamf Pro Hostname and try again.')
            sys.exit('Not Found.. 1000 percent lost.')

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
            print(f'ERROR [get_token(apiToken)]: {errorMessage}')
        else:
            print(f'[get_token]: Saved API Token..\n')
    except Exception as errorMessage:
        print(f'ERROR [get_token(apiResponseJSON)]: {errorMessage}\n')
