## jamfAuth.py
## version: 0.2
## Josh Harvey - josh.harvey@jamf.com
## github.com/therealmacjeezy
## created: April 2022

from support.getToken import *
from support.configCheck import *
import sys

def load_config(jamfSearchConfig):
    global data
    global apiUser
    global apiToken
    global baseAPIURL
    global theURL
    try:
        with open(jamfSearchConfig, 'r') as f:
            data = json.load(f)
            apiUser = data['apiUserName']
            baseAPIURL = data['jamfAPIURL']
            # apiToken = data['apiToken']
            try:
                # apiToken = keyring.get_password(apiUser+'API', apiUser)
                apiToken = keyring.get_password(baseAPIURL, apiUser+'API')
                print(f'[>jamfAuth] Loaded API Token')
            except Exception as errorMessage:
                print(f'[ERROR>jamfAuth] {errorMessage}')
            theURL = baseAPIURL+'auth'
    except Exception as errorMessage:
        print(f'ERROR load_config: Load Config] - {errorMessage}')



def startAuth():
    pwd = os.getcwd()
    global jamfSearchConfig
    jamfSearchConfig = pwd+f'/support/.jamfauth.json'
    authHeader = '''   _                  __   _         _   _     
  (_) __ _ _ __ ___  / _| /_\  _   _| |_| |__  
  | |/ _` | '_ ` _ \| |_ //_\\\| | | | __| '_ \ 
  | | (_| | | | | | |  _/  _  \ |_| | |_| | | |
 _/ |\__,_|_| |_| |_|_| \_/ \_/\__,_|\__|_| |_|
|__/ ------ jamfAuth.py (v0.2)
----------- josh.harvey@jamf.com
----------- Created: 04/25/22
----------- Modified: 04/26/22              
 '''

    print(authHeader)
    # print('-----------------------------------------------------------------')

    #start config check
    check_config(jamfSearchConfig)
    start_config_check(jamfSearchConfig)
    load_config(jamfSearchConfig)
    check_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)
    return apiToken
    # print('-----------------------------------------------------------------')

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            print('Resetting Settings..')
            reset_config()
        if sys.argv[1] == 'setup':
            print('Setting up Config..')
            startAuth()
    else:
        print('no arg')
        startAuth()
        # print(f'Your API token can be used with the variable apiToken.')

if __name__ == '__main__':
    main()
