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
            try:
                apiToken = keyring.get_password(baseAPIURL, apiUser+'API')
                print(f'[>jamfAuth] Loaded API Token')
            except Exception as errorMessage:
                print(f'[ERROR>jamfAuth] {errorMessage}')
            theURL = baseAPIURL+'auth'
    except Exception as errorMessage:
        print(f'ERROR load_config: Load Config] - {errorMessage}')

def header(instance=""):
    pwd = os.getcwd()
    global jamfSearchConfig
    if instance == "dev":
        jamfSearchConfig = pwd+f'/support/.jamfauth.json'
    else:
        jamfSearchConfig = pwd+f'/support/.jamfauth-dev.json'

    authHeader = '''   _                  __   _         _   _     
  (_) __ _ _ __ ___  / _| /_\  _   _| |_| |__  
  | |/ _` | '_ ` _ \| |_ //_\\\| | | | __| '_ \ 
  | | (_| | | | | | |  _/  _  \ |_| | |_| | | |
 _/ |\__,_|_| |_| |_|_| \_/ \_/\__,_|\__|_| |_|
|__/ ------ jamfAuth.py (v0.3.4) [github]
----------- josh.harvey@jamf.com
----------- Created: 04/25/22
----------- Modified: 06/16/22              
 '''

    print(authHeader)
    print(f'> jamfAuth Config Path: \n{jamfSearchConfig}\n')  


def startAuth(instance=""):
    header(instance)
    pwd = os.getcwd()
    global jamfSearchConfig
    ## Adding support for a development server
    if instance == "dev":
        jamfSearchConfig = pwd+f'/support/.jamfauth.json'
    else:
        jamfSearchConfig = pwd+f'/support/.jamfauth-dev.json'

    #start config check
    check_config(jamfSearchConfig)
    start_config_check(jamfSearchConfig)
    load_config(jamfSearchConfig)
    check_token(apiUser, apiToken, theURL, baseAPIURL, jamfSearchConfig)
    load_config(jamfSearchConfig)
    return apiToken

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            print('[>jamfAuth]: Resetting Settings for Production..')
            reset_config()
        if sys.argv[1] == 'reset-dev':
            print('[>jamfAuth]: Resetting Settings for Dev..')
            reset_config("dev")
        if sys.argv[1] == 'setup':
            print('[>jamfAuth]: Setting up Config for Production..')
            startAuth()
        if sys.argv[1] == 'setup-dev':
            print('[>jamfAuth]: Setting up Config for Dev..')
            startAuth("dev")
    else:
        print('no arg')
        startAuth()

if __name__ == '__main__':
    main()
