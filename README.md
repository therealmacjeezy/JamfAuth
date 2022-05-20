# JamfAuth

A python script to authenticate with the Jamf Pro API.

[jamfAuth Examples](examples/README.md)

**Current Version:** v0.3.3

### Supported Operating Systems
**Operating System** | **Version** | **Status** | **Notes**
-------------------- | ---------- | --------- | ----------
**macOS Monterey** | macOS 12.x | ✅ *(Supported)* | None
**RedHat Enterprise Linux (RHEL)** | 9 (Beta) | ✅ *(Supported in 0.3.3+)* | *Requires keychains.alt package*
**RedHat Enterprise Linux (RHEL)** | 8 | ⚠️ *(Needs Testing)* | None
**CentOS Stream** | 8 | ⚠️ *(Needs Testing)* | None
**Oracle Linux** | 8 | ⚠️ *(Needs Testing)* | None
**Ubuntu Server** | 20.04.4 LTS | ✅ *(Supported in 0.3.3+)* | *Requires keychains.alt package*

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


The `jamfAuth` JSON Configuration file is located in the `support` directory:

**Install Method** | **Configuration File Location**
------------------ | ------------------------------
**Github** | `/path/to/jamfAuth/support/.jamfauth.json`
**pip** | `/path/to/pip/site-packages/jamfAuth/support/.jamfauth.json`

---
### jamfAuth Options
The `jamfAuth` script also has two options available for use to help make setup easier, these are `reset` and `setup`. Depending on how you installed `jamfAuth` will depend on how these two options can be called.

#### Reset Option

**Install Method** | **Command**
------------------ | ------------------------------
**Github** | `python3 /path/to/jamfAuth.py reset`
**pip** | `python3 -c 'from jamfAuth import *; reset_config()'`

The `reset` option allows you to reset the JSON Configuration file that `jamfAuth` uses. The following items in the JSON Config file will be reset:
 - apiUserName
 - jamfHostName
 - jamfAPIURL

After the `reset` option is ran, you will be prompted to enter the `Jamf Pro Host Name` and `API Username` on the next run.

#### Setup Option

**Install Method** | **Command**
------------------ | ------------------------------
**Github** | `python3 /path/to/jamfAuth.py setup`
**pip** | `python3 -c 'from jamfAuth import *; startAuth()'`

The `setup` option allows you to setup the JSON Configuration file that `jamfAuth.py` uses. You can use this option if you would like to avoid being prompted to enter information. 

----
## To-Do List
 - [x] Save API Token in the keychain and remove it from the JSON config file
 - [x] Add usage examples
 - [x] Add additional error handling (if a 401 occurs.. etc..)
 - [x] Create pip install
 - [ ] Add option to delete the keychain entry (currently manual delete)
 - [ ] Add additional OS support (linux, windows)

---
## Installation
There are two ways to install `jamfAuth`: **Github** or **pip**.

### pip Method *[Recommended]*
This method will install `jamfAuth` **and** all of the required packages. Using this method will allow you to import and use `jamfAuth` without having to copy the `jamfAuth` directory into the project your going to use it with. 

 - `pip3 install jamfAuth`
   - [PyPi URL](https://pypi.org/project/jamfAuth/)

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

To install all of the required Python packages at once, use the `requirements.txt` file to install them using the command below:

`pip3 install -r requirements.txt`

**Individual Packages**
 - **requests**
   - `pip3 install requests`
 - **keyring**
   - `pip3 install keyring`
 - **keyrings.alt** *(Linux ONLY)*
   - `pip3 install keyrings.alt`

---
### Usage
Once installed, you'll need to configure `jamfAuth` by using the **setup** option (see **Setup Option** section above). This will create the jamfAuth configuration file and the keychain entries. Once it's setup, you're ready to start playing with API Calls!

To use `jamfAuth` with your script, import `jamfAuth` and set the `startAuth()` function to a variable to store the API Token. See the example below

**Note:** 
> If you used the **Github** method to install `jamfAuth`, you will need to copy the `jamfAuth` directory into the root directory of the script you are going to be using it with. If you used the `pip` method, you can just import `jamfAuth` as normal.

```
from jamfAuth import *

apiPassword = startAuth()

if apiPassword:
    print('You can now use the apiToken variable to authenticate with your Jamf Pro API.')
    print(f'apiToken: \n{apiPassword}')
```
#### Examples
I created a few example scripts in both `python` and `bash` to show how easy it is to use jamfAuth in your script. Check out the **examples** directory or view the [examples README.md](examples/README.md) to see them.