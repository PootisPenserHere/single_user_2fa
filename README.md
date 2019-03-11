# Single user 2fa
A serverless aproach to managing the two-factor authentication (2fa) tokens for a single account and deliver them by sms.

## Setting up the work environment

### Prerequisites
A zeit account will be needed to perform the deployments, if you're not registere a free account can be created [here.](https://zeit.co)

To send the sms messages a Twilio account with its corresponding sid and auth token credentials [for further reading](https://www.twilio.com/sms)

**NOTE:** Although Twilio offers a free trial, after said period there will be chargers for the service in the form of a set price for each sms based on the destination country as well as the monthly rent of a phone number.

### Installing now
```bash
# yarn
yarn global add now

# npm
npm install -g now
```

### Sing up in zeit
Actions such as deployment will require that zeit has been authenticated for the current machine, it can be done with:
```bash
now login
```

This process will ask the user to introduce their registered email and the to click on a verify email that they'll get.


### Deploying
To deply a new version simply run the command:
```bash
now
```

## Personalizing
Once the environment has been set up it's time to set our credentials and authentication secrets. By the fault there are 5 secrets that must be set and they can be found in the now.json file at the "env" key.

```text
{
    "version": 2,
    "name": "single_user_2fa",
    "env": {
        "SECRET": "@2fa_secret",
        "TWILLIO_ACCOUND_SID": "@twillio_account_sid",
        "TWILLIO_AUTH_TOKEN": "@twillio_auth_token",
        "TO_NUMBER": "@twillio_to_number",
        "FROM_NUMBER": "@twillio_from_number"
    },
    "builds": [
        { "src": "*.py", "use": "@now/python" }
    ]
}

```

Setting up the new secrets
```bash
now secret add 2fa_secret 2fa_secret_here
now secret add twillio_account_sid twillio_api_sid_here
now secret add twillio_auth_token twillio_api_auth_here
now secret add twillio_to_number destination_phone_here
now secret add twillio_from_number yout_twillio_number_here

```

**Note:** If the secrets are changed a new version of the code must be deployed for the changes to take effect.

## Credit
Credit goes to **Patrick Mylund Nielsen** for his [python implementation of the 2fa ](https://patrickmn.com/security/you-can-be-a-twofactor-hero/)
## TODO
* Leading 0s in codes are omited by the algorithm
    * Likely happens with any number of continues leading zeros
