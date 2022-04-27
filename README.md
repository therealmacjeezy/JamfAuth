# JamfAuth

A python script to authenticate with the Jamf Pro API.

## To-Do List
 - [x] Save API Token in the keychain and remove it from the JSON config file
 - [x] Add usage examples
 - [ ] Add additional error handling (if a 401 occurs.. etc..)
 - [x] Create pip install
 - [ ] Add option to delete the keychain entry (currently manual delete)

---

## Overview
This python script handles the API Authentication to your Jamf Pro Server. Once you have a valid API Token, you can store it as a variable and use it when performing API calls later in the script.

Here is how `jamfAuth.py` works:
 - Checks to see if the JSON Config file exists. 
   - **✅ JSON Config Found:** Attempts to load the `apiUserName` and `jamfHostName` variables
   - **⚠️ JSON Config Not Found:** Creates an empty JSON Config file and prompts you for the following things: `Jamf Pro Host Name`, `API Username`
 - Once the above information is entered/loaded, it will check the local keychain for an API Token.
   - **✅ API Token Found:** Checks to see if the API Token stored is valid
     - **✅ Valid Token:** Returns the API Token for use
     - **⚠️ Invalid Token:** Attempts to renew the API Token (using `keep-alive`). If the API Token is unable to be renewed, it will check the local keychain for the **API Password**
       - **✅ API Password Keychain Found:** Uses the `API Password` to get a new API Token then saves it to the local keychain then returns it for use
       - **⚠️ API Password Keychain Not Found:** Prompts for the API Password, stores it in the local keychain and gets a new API Token then returns it for use
   - **⚠️ API Token Not Found:** Checks the local keychain for the `API Password`
       - **✅API Password Keychain Found:** Uses the `API Password` to get a new API Token then saves it to the local keychain then returns it for use
       - **⚠️ API Password Keychain Not Found:** Prompts for the API Password, stores it in the local keychain and gets a new API Token then returns it for use



The `API Password` and `API Token` will be stored in the local keychain (using the [keyring](https://pypi.org/project/keyring/) python library) with the following naming convention:

**Variable** | **Keychain Naming Convention**
---------------- | --------------
**API Password** | service = **JamfProHostName**, username = **API Username**, password = **API Password**
**API Token** | service = **JamfProHostName**, username = **API Username**+API, password = **API Token**


The `jamfAuth.py` JSON Configuration file is located in the `support` directory:
 - **Github Install Method:** `/path/to/jamfAuth/support/.jamfauth.json`
 - **pip Install Method:** `/path/to/pip/site-packages/jamfAuth/support/.jamfauth.json`

---
### `jamfAuth.py` Options
The `jamfAuth.py` script also has two options available for use to help make setup easier, these are `reset` and `setup`. Depending on how you installed `jamfAuth` will depend on how these two options can be called.

#### Reset Option
**Github Install Method**
`python3 /path/to/jamfAuth.py reset`


**pip Install Method**
`python3 -c 'from jamfAuth import *; reset_config()'`

The `reset` option allows you to reset the JSON Configuration file that `jamfAuth.py` uses. The following items in the JSON Config file will be reset:
 - apiUserName
 - jamfHostName
 - jamfAPIURL

After the `reset` option is ran, you will be prompted to enter the `Jamf Pro Host Name` and `API Username` on the next run.

#### Setup Option
**Github Install Method**
```
11:35:32 ➜ JamfAuth git:(main!) python3 jamfAuth.py setup
Setting up Config..
   _                  __   _         _   _
  (_) __ _ _ __ ___  / _| /_\  _   _| |_| |__
  | |/ _` | '_ ` _ \| |_ //_\\| | | | __| '_ \
  | | (_| | | | | | |  _/  _  \ |_| | |_| | | |
 _/ |\__,_|_| |_| |_|_| \_/ \_/\__,_|\__|_| |_|
|__/ ------ jamfAuth.py (v0.2.1)
----------- josh.harvey@jamf.com
----------- Created: 04/25/22
----------- Modified: 04/26/22

Enter the Jamf Pro URL (without https://):
	=> mooncheese.jamfcloud.com
Enter the Username for API Access:
	=> mcapi
[>jamfAuth] Unable to find keychain entry. lets make one shall we?
What is the password for mcapi:
[>jamfAuth] API Token saved to keychain.
```

**pip Install Method**

`python3 -c 'from jamfAuth import *; startAuth()'`

The `setup` option allows you to setup the JSON Configuration file that `jamfAuth.py` uses. You can use this option if you would like to avoid being prompted to enter information. 

---
## Installation
There are two ways to install `jamfAuth`, **Github** or **pip**.

### pip Method *[Recommended]*
This method will install `jamfAuth` **and** all of the required packages. Using this method will allow you to import and use `jamfAuth` without having to copy the `jamfAuth` directory into the project your going to use it with. 
 - `pip3 install jamfAuth`
   - [PyPi URL](https://test.pypi.org/project/jamfAuth/)

### Github Method
This method will clone the `jamfAuth` code to your system. When using this method, you will need to install the required Python3 packages manually.
 - `git clone https://github.com/therealmacjeezy/JamfAuth.git`

---
## Requirements
### Jamf Pro
 - A Jamf Pro account that has API Access

### Python
**Python Version** | **Supported**
------------------ | -------------
3.8.9 | ✅ *(Supported)*
3.9.x | ⚠️ *(Not Tested)*
3.10.x | ✅ *(Supported)*

**Required Python Packages:**
 - `pip3 install requests`
 - `pip3 install keyring`

---
### Usage
To use `jamfAuth.py` with your script, import `jamfAuth` and set the `startAuth()` function to a variable to store the API Token. See the example below

**Note:** If you used the **Github** method to install `jamfAuth`, you will need to copy the `jamfAuth` directory into the root directory of the script you are going to be using it with. If you used the `pip` method, you can just import `jamfAuth` as normal.

```
from jamfAuth import *

apiPassword = startAuth()

if apiPassword:
    print('You can now use the apiToken variable to authenticate with your Jamf Pro API.')
    print(f'apiToken: \n{apiPassword}')
```

#### Examples
Below is an example script that shows how to use `jamfAuth.py` and the API Token it gets. 

The first example performs a search for all computers that contain the word **admin** in it and returns the results via XML.

The second example performs a search for all packages in Jamf Pro and returns the results via XML.

**example.py**
```
## example.py
from jamfAuth import * ## <-- Import jamfAuth
import xmltodict

apiToken = startAuth() ## <-- This is the variable that is used to capture the API Token

jamfHostName = 'benderisgreat.jamfcloud.com'

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
```

**example.py Output**
```10:43:37 ➜ JamfAuth git:(main!?) python3 example.py
   _                  __   _         _   _
  (_) __ _ _ __ ___  / _| /_\  _   _| |_| |__
  | |/ _` | '_ ` _ \| |_ //_\\| | | | __| '_ \
  | | (_| | | | | | |  _/  _  \ |_| | |_| | | |
 _/ |\__,_|_| |_| |_|_| \_/ \_/\__,_|\__|_| |_|
|__/ ------ jamfAuth.py
----------- josh.harvey@jamf.com
----------- Created: 04/25/22
----------- Modified: N/A

[Jamf Pro Host Name]: benderisgreat.jamfcloud.com
[Jamf Pro API URL]: https://benderisgreat.jamfcloud.com/api/v1/
[Jamf Pro API Username]: mcapi
[>jamfAuth] Loaded API Token
[Jamf Pro API Token Status]: Valid
### >> Example 1: Search for Computers that contain *admin*
Status Code: 200
{"computers": {"size": "1", "computer": {"id": "1", "name": "ladmin\u2019s MacBook Pro", "udid": "B71D8D21-AFF8-5ED3-B7F1-BB1488CBC8D1", "serial_number": "C02T39SEGTFM", "mac_address": "78:4F:43:64:17:E8", "alt_mac_address": "82:49:6E:C3:E0:01", "asset_tag": null, "bar_code_1": null, "bar_code_2": null, "username": "josh.harvey", "realname": "Josh Harvey", "email": "josh.harvey@jamf.com", "email_address": "josh.harvey@jamf.com", "room": null, "position": null, "building": null, "building_name": null, "department": null, "department_name": null}}}

### >> Example 2: List all Packages
Status Code: 200
{"packages": {"size": "2", "package": [{"id": "1", "name": "Jamf Connect [2.11]"}, {"id": "2", "name": "JamfProtect-3.1.6+469.pkg"}]}}
```
