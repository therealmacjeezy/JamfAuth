from jamfAuth import *

### This is the variable that is used to capture the API Token
apiToken = startAuth()

jamfHostName = 'benderthegreat.jamfcloud.com'
# apiURL = 'https://{jamfHostName}/JSSResource/computers/match/*admin*'

if apiToken:
    headers = {'accept': 'application/xml', 'Authorization': f'Bearer {apiToken}'}
    print('You can now set the API Token to a variable and use it in the header to authenticate with your Jamf Pro server.')

    print('### >> Example 1: Search for Computers that contain *admin*')
    apiURL1 = f'https://{jamfHostName}/JSSResource/computers/match/*admin*'
    # apiURL1 = 'https://mooncheese.jamfcloud.com/JSSResource/computers/match/*admin*'
    print(f'API URL: {apiURL1}')
    example1 = requests.get(apiURL1, headers=headers)
    search1Results = example1.text

    print(search1Results)
    # try:
    #     if example1.status_code == 200:
    #         example1.json()
    # except Exception as errorMessage:
    #     print('uh...'+errorMessage)

    print(f'\n### >> Example 2: List all Packages')
    apiURL2 = f'https://{jamfHostName}/JSSResource/packages'
    print(f'API URL: {apiURL2}\n')
    example2 = requests.get(apiURL2, headers=headers)
    print(example2.text)