### v0.3.1 (2022/04/27)
**New Features**
 - Added error handling to `getToken.py` to better manage the HTTP status codes inside the `getToken()` function.
 - Added a section inside the **401** check to handle incorrect passwords. It will now delete the keychain item containing the API Password and prompt you to enter a new one. It will then try to get an API Token with the new credentials
**Minor Changes**
 - Adjusted the formatting for how the jamfAuth Config Path appears in the header

### v0.3 (2022/04/26)
 - apiToken is now stored in the local keychain
 - added **setup** and **reset** options for `jamfAuth.py`
