from jamfAuth import *

apiPassword = startAuth()

if apiPassword:
    print('You can now use the apiToken variable to authenticate with your Jamf Pro API.')
    print(f'apiToken: \n{apiPassword}')