### Sing up
Actions such as deployment will require that zeit has been authenticated for the current machine, it can be done with
```bash
now login
```

This process will ask the user to introduce their registered email and the to click on a verify email that they'll get



### Deploying
To deply a new version simply run the command
```bash
now
```

### Secrets
New secrets can be created with
```bash
now secret add acme-api-key my-value-here
```

With this a new secret will be created and can now be referenced in the now.json file to add it to the deployment

```json
{
    "version": 2,
    "name": "single_user_2fa",
    "env": {
        "api-key": "@acme-api-key"
    },
    "builds": [
        { "src": "*.py", "use": "@now/python" }
    ]
}

```

The secret may also be deleted with
```bash
now secret rm acme-api-key
```

For further reading **https://zeit.co/docs/v2/deployments/environment-variables-and-secrets/#securing-environment-variables-using-secrets**