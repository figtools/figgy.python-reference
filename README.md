![Figgy](.assets/logo-black-text.png)

[Figgy Website](https://www.figgy.dev)

[Figgy Docs](https://www.figgy.dev/docs/)

# figgy.python-reference 

An example Flask application demonstrating how you can leverage Figgy for application config management.

To run the DEMO from top to bottom, these are the requirements:

- FiggyCLI must be installed: [Install instructions](https://www.figgy.dev/docs/getting-started/install/)

Optional: See your configuration changes [In Real Time](https://www.figgy.dev/tabs/sandbox/). Any changes you (or anyone) make with
figgy push notifications to this web page. This demonstrates the event-driven nature of Figgy.

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

When prompted to select a role, you will want to select the **DBA** role. Input whatever you want for other prompts.
 
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
**auto-generated a definition of the configurations** it needs to run under `figgy/figgy.json`. Now we KNOW what we need,
lets sync the `desired_state` with the `actual_state`

```console
    $   figgy config sync --env dev
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
    $   figgy config sync --env dev 
```

Go to: `http://localhost:5000` to see who the third wheel is.

You'll be prompted to add the missing config.

### Sixth: What about those DB credentials?

Remember a few minutes ago when you were asked to input database users and credentials? This was to demonstrate a few things.
First, we impersonated the DBA and stored our super-secret credentials in a place special to our DBA user that other
user-types do not have access to. 

In our `config.py` file you'll see this:
```python
    # Merged Connection URL (merged figs)
    SQL_CONNECTION_STRING = MergeFig(
        name="replicated/sql-connection",
        pattern=["mysql://", SQL_USER, ":", SQL_PASSWORD, "@", SQL_HOSTNAME, ":", SQL_PORT, "/", SQL_DB_NAME]
    )
```

What we are doing here is defining a "merge schema" for how to build our special database connection string.

SQL_USER and SQL_PASSWORD are the two values you stored in the super-secret DBA secret-store. 

SQL_HOSTNAME, SQL_PORT, and SQL_DB_NAME are global non-secret shared parameters that you are having shared into your 
`/app/YOUR_SERVICE_NAME` namespace because they are declared that way in `config.py`:

```python
    # Global figs used by many services that we need to use (replicated figs)
    SQL_HOSTNAME = ReplicatedFig(source="/shared/resources/dbs/fig-db/dns", name="replicated/sql/hostname")
    SQL_PORT = ReplicatedFig(source="/shared/resources/dbs/fig-db/port", name="replicated/sql/port")
    SQL_DB_NAME = ReplicatedFig("/shared/resources/dbs/fig-db/db-name", name="replicated/sql/db-name")
```

All of these values are merged together by `figgy` and kept in sync behind-the-scenes. Your CLI does not do any of this 
merging, the Figgy serverless ecosystem does. 

The net of it all is, if you go to: `http://localhost:5000/db` you'll see your DB connection string that has been URI encoded
and dynamically assembled based on the schema defined in `config.py`


### Other paths to experiment with:

- Try `figgy config validate ` to see how CICD can easily vaildate your apps configurations.
- Browse the Fig Orchard to see your configurations: `figgy config browse --env dev`
- Delete a new config, then rerun sync (this will prompt you to run cleanup)
            
#### Using validating during your CICD process:
- See the `.github/workflows/cicd.yml` for an example of how you can install, configure, and use figgy to run build-time
cicd validations!