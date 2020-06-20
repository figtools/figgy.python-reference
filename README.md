# figgy.python-reference 
An example Flask application demonstrating how you can leverage Figgy for application config management.

To run the DEMO from top to bottom, these are the requirements:

- FiggyCLI must be installed: [Install instructions](https://www.figgy.dev/docs/getting-started/install.html)

### First: Pick a service name:
Open `src/config.py`

Change
```python
11    SERVICE_NAME: str = "demo-service"
```
To:

```python
11    SERVICE_NAME: str = "YOUR_CUSTOM_NAME_HERE"
```

maybe something like `YOUR_NAME-playground`? :)

Many people could be playing in this sandbox so this will reduce the likelihood you'll get a name collision with someone
playing right now. 

### Second: Add our secret configs
Take notice of the `figgy-secrets.json` in your `figgy/` directory.

1. Open `figgy-secrets.json` and replace `YOUR_SERVICE` with the service name you just selected. There are 4 places to update in this file.

In this case, lets pretend you're a DBA and you're creating a definition of all secrets you manage for `YOUR_SERVICE`,
this is the definition of what they are, where they're stored, and what application is using them. 
Now we just need to add the secrets and share it with the service.

1. Log-in to the figgy sandbox:

You will want to select the **DBA** role. The other options are whatever you want.
 
```console
    $   figgy login sandbox

    Please select a role to impersonate:
    Options: ['dev', 'devops', 'sre', 'data', 'dba']
-----> dba <------
```

Great, you're now impersonating the DBA, since you're the *secret owner*, lets store the secrets your app needs:
```console
    figgy config sync --config figgy/figgy-secrets.json --env dev --replication-only
```

Follow the prompts, you'll be asked to add a username / password. You can put anything and encrypt it with whatever
encryption key you want ;). 

Booya, you just stored some UBER secret credentials AND you shared them with our application! Woo woo! :sunglasses:

### Third: Add our application configs
Next, lets impersonate a developer, so lets re-login to the sandbox and select `dev` for the ROLE.

```console
    $   figgy login sandbox

    Please select a role to impersonate:
    Options: ['dev', 'devops', 'sre', 'data', 'dba']
-----> dev <------
```

### Fourth: Run our app!
Export temporary credentials so our app has permissions to access ParameterStore. This will write temporary credentials 
to your `~/.aws/credentials` file under the `[default]` profile. If you use `[default]`, backup your existing credentials file. 

1. Backup your credentials file
```console
    $   cp ~/.aws/credentials ~/.aws/credentials.backup
```

1. Export new credentials
```
    $   figgy iam export --env dev
```

1. Run it! 
```
    $   ./run_docker.sh
```

Go to `http://localhost:5000`

Oh no! Your app is missing some configurations! No worries, look in the `figgy/` directory. You'll see your application
auto-generated a definition of the configurations it needs to run under `figgy/figgy.json`. Now we KNOW what we need,
lets sync the `desired_state` with the `actual_state`

```console
    $   figgy config sync --config figgy/figgy.json
```

**Refresh your browser to see who the secret admirer is:** http://localhost:5000/

Right now we are allowing the application to start even when it's missing configurations. 
This works because we have set `lazy_load=True`. If you disable lazy_load you'll see the app can't start without all required
configurations in ParameterStore. This is recommended for non-local deployments, but lazy_load is great for local 
development!

```python
    # src/app.py

    FIGS = Figs(svc, lazy_load=True)
```

### Fifth: Add a new config

In src/config.py add a new config, lets call this config the THIRD_WHEEL. It's an `AppFig` because it's unique to THIS application.
```python
    # src/config.py

    # Custom Figs specific to my application (app figs)
    SECRET_ADMIRER = AppFig("secret-admirer")
    ADMIRED_PERSON = AppFig("admired-person")
    SQL_DB_NAME = AppFig("db-name", default="SecretAdmirerDB")

    THIRD_WHEEL = AppFig("third-wheel")  # <--- Add this
```

Let's add our third wheel to our message.
```python
    # src/app.py

29      return f"Hello {FIGS.ADMIRED_PERSON}, {FIGS.SECRET_ADMIRER} is admiring you! {FIGS.THIRD_WHEEL} is super jealous."
```

Re run the app:
```console
    $   ./run_docker.sh
```

Look at your figgy.json - notice how it's updated and shows your new configuration in the `app_figs` section?

Rerun sync
```console
    $   figgy config sync --env dev --config figgy/figgy.json
```

You'll be prompted to add the missing config.

**Other paths to experiment with:**
    - Browe the Fig Orchard to see your configurations: `figgy config browse --env dev`
    - Delete the new config, then rerun sync (this will prompt you to run cleanup)
    - Try setting `lazy_load=True` in `src/app.py`
        - This will enable you to run the app to generate the `figgy.json`, run sync, then use the app and have it 
            dynamically pull the new config without a restart.
            
            
#### Using validating during your CICD process:
- See the `.github/workflows/cicd.yml` for an example of how you can install, configure, and use figgy to run build-time C
cicd validations!