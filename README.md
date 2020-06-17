# figgy.python-reference
An example Flask application demonstrating how you can leverage Figgy for application config management.

To run the DEMO from top to bottom, these are the requirements:

- FiggyCLI must be installed: [Install instructions](https://www.figgy.dev/docs/getting-started/install.html)
- You'll need python 3.7+ installed [Install instructions](https://www.python.org/downloads/)

### First: Pick a service name:
Open `src/config.py`

Change
```python
    TWIG: str = "/app/demo-service"
```
To:

```python
    TWIG: str = "/app/YOUR_CUSTOM_NAME_HERE"
```

maybe something like `/app/YOUR_NAME-playground`? :)

Many people could be playing in this sandbox so this will reduce the liklihood you'll get a name collision with someone
playing right now. 

### Second: Add our secret configs
Take notice of the `figgy.json` file in your root directory.

1. Log-in to the figgy sandbox: [More Instructions](https://www.figgy.dev/docs/getting-started/sandbox.html)

You will want to select the DBA role. 
 
```console
    figgy login sandbox
```

Right now you're impersonating the DBA, since you're the Secret Owner, lets store the secrets your app needs:
```console
    figgy config sync --config figgy-dba.json --env dev --replication-only
```
Follow the prompts, you'll be asked to add a username / password. You can put anything and encrypt it with whatever
encryption key you want ;). 

Booya, bet you just stored some UBER secret credentials AND you shared them with our application! Woo woo!

### Third: Add our application configs
Next, lets impersonate a developer, so lets re-login to the sandbox and select `dev` for the ROLE.

```console
    figgy login sandbox
```

Then after login run sync:
```console
    figgy config sync --config figgy.json --env dev
```

You'll be prompted to add the required configurations that are missing.

If you `re-run` `figgy config sync --config figgy.json --env dev` you should see `Sync completed with no errors!` 

### Fourth: Run our app!

Set local run ENV variable:
```console
    export LOCAL_RUN=true
```

Install requirements
```console
    pip3 install -r src/requirements.txt
```

Run it!
```
    python3 src/app.py
```

Check check to see who the secret admirer is: http://localhost:5000/

### Fifth: Add a new config

In src/config.py add a new `AppFig`
```python
    # Custom Figs specific to my application (app figs)
    SECRET_ADMIRER = AppFig("secret-admirer")
    ADMIRED_PERSON = AppFig("admired-person")
    SQL_DB_NAME = AppFig("db-name", default="SecretAdmirerDB")
    YOUR_FIG_HERE = AppFig("new-configuration")    <--- Add this - or something like it
```

Re run the app:
```console
    python3 src/app.py
```

Look at your figgy.json - notice how it's updated and now shows your configuration in the `app_figs` section?

Rerun sync
```console
    figgy config sync --env dev --config figgy.json
```

You'll be prompted to add the missing config.

Other paths to experiment with:
    - Delete the config, then rerun sync (this will prompt you to run cleanup)
    - Try enabling lazy_load=True in `src/app.py`
        - This will enable you to run the app to generate the figgy.json, run sync, then use the app and have it 
            dynamically pull the new config without a restart.