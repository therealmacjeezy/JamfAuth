### v0.3.3 (2022/04/29)
**New Features**
 - Added support for the following Operating Systems:
  - Ubuntu Server 20.04.4 LTS
  - Red Hat Enterprise Linux 9 (Beta)
**Minor Changes**
 - [pip] Added minimum required versions to setup.cfg
 - [pip] Added `keychains.alt` to **install_requires** for any Linux system in setup.cfg

### v0.3.2 (2022/04/28)
**Minor Changes**
 - Changed python classifier from **beta** to **production/stable**
 - Updated README.md with example scripts

### v0.3.1 (2022/04/27)
**New Features**
 - Added error handling to `getToken.py` to better manage the HTTP status codes inside the `getToken()` function.
 - Added a section inside the **401** check to handle incorrect passwords. It will now delete the keychain item containing the API Password and prompt you to enter a new one. It will then try to get an API Token with the new credentials
**Minor Changes**
 - Adjusted the formatting for how the jamfAuth Config Path appears in the header

### v0.3 (2022/04/26)
 - apiToken is now stored in the local keychain
 - added **setup** and **reset** options for `jamfAuth.py`
