from jamfAuth import * ## <-- Import jamfAuth
import xmltodict

apiToken = startAuth() ## <-- This is the variable that is used to capture the API Token

jamfHostName = 'mooncheese.jamfcloud.com'

if apiToken:
    headers = {'accept': 'application/xml', 'Authorization': f'Bearer {apiToken}'} ## <-- apiToken being used to authenticate the API Call

    print('### >> Example 1: Search for Computers that contain *admin*')
    apiURL1 = f'https://{jamfHostName}/JSSResource/computers/match/*admin*'
    example1 = requests.get(apiURL1, headers=headers)

    print(f'Status Code: {example1.status_code}')

    example1XML = xmltodict.parse(example1.text)

    print(json.dumps(example1XML))


    print(f'\n### >> Example 2: List all Packages')
    apiURL2 = f'https://{jamfHostName}/JSSResource/packages'
    example2 = requests.get(apiURL2, headers=headers)

    print(f'Status Code: {example2.status_code}')
    
    example2XML = xmltodict.parse(example2.text)

    print(json.dumps(example2XML))

