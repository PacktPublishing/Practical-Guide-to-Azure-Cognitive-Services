# Ocean Smart Portal Demo

This is an example of using Cognitive Services within an interactive portal.
The demo will highlight the different Cognitive Services that you can interact
with. This code has been tested to run within a local Python environment as
well as running in a Docker container. It is recommended to use Docker if you
are unfamiliar with Python environments.

<!-- TOC -->

- [Ocean Smart Portal Demo](#ocean-smart-portal-demo)
  - [Azure](#azure)
  - [Create .env file with credentials](#create-env-file-with-credentials)
  - [Local](#local)
    - [Requirements (local)](#requirements-local)
    - [Running (local)](#running-local)
  - [Docker](#docker)
    - [Requirements (docker)](#requirements-docker)
    - [Running (docker)](#running-docker)

<!-- /TOC -->

## Azure

For the demo to work, it is required to have certain resources created. Also
you will need to create credentials in order to interact with some of the
resources the demo requires.

Depending on what features you want to demo, they have been separated by
chapter.

- [Chapter 8 - Form Recognizer](../Chapter%2008/Azure%20Templates/README.md)

## Create .env file with credentials

In order for the demo to initialize and use your Azure resources, create a `.env`
file with all the required variables needed for the demo to launch. A sample env file
was made named `sample.env`. Rename the file to `.env` and replace the values with
the correct information.

In your terminal:

```shell
$ cp sample.env .env
$
```

## Local

If you want to run the demo locally on your machine, it is required to have a
Python environment set up and configured before you start.

### Requirements (local)

The following is required to be installed on your system before following the
run steps.

- Python 3.9
- [Pipenv](https://pipenv.pypa.io/en/latest/)

### Running (local)

Verify you can run Pipenv:

```shell
$ pipenv --version
pipenv, version 2022.1.8
```

Run pipenv to install all required python packages.

```shell
$ pipenv install
Creating a virtualenv for this project...
Pipfile: C:\Users\user\SynologyDrive\Code\cognitive-services-book\Demo\Pipfile
Using C:/Python39/python.exe (3.9.7) to create virtualenv...
[==  ] Creating virtual environment...created virtual environment CPython3.9.7.final.0-64 in 4352ms
  creator CPython3Windows(dest=C:\Users\user\.virtualenvs\Demo-I_CdxxlR, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=C:\Users\user\AppData\Local\pypa\virtualenv)
    added seed packages: pip==21.3, setuptools==58.2.0, wheel==0.37.0
  activators BashActivator,BatchActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

Successfully created virtual environment!
Virtualenv location: C:\Users\user\.virtualenvs\Demo-I_CdxxlR
Pipfile.lock (f9f8f7) out of date, updating to (e56df5)...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
           Building requirements...
Resolving dependencies...
Success!
Updated Pipfile.lock (e56df5)!
Installing dependencies from Pipfile.lock (e56df5)...
  ================================ 33/33 - 00:00:41
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

Enter the Python environment and check pipenv is configured correctly.

```shell
$ pipenv shell
Loading .env environment variables...
Launching subshell in virtual environment...

$ pipenv check
Checking PEP 508 requirements...
Passed!
Checking installed package safety...
All good!
```

Create database tables

```shell
$ python manage.py migrate
Operations to perform:
  Apply all migrations: account, admin, auth, contenttypes, forms_recognizer, sessions, sites, socialaccount
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying account.0001_initial... OK
  Applying account.0002_email_max_length... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying forms_recognizer.0001_initial... OK
  Applying sessions.0001_initial... OK
  Applying sites.0001_initial... OK
  Applying sites.0002_alter_domain_unique... OK
  Applying socialaccount.0001_initial... OK
  Applying socialaccount.0002_token_max_lengths... OK
  Applying socialaccount.0003_extra_data_default_dict... OK
```

Create a superuser login.

```shell
$ python manage.py createsuperuser
Username (leave blank to use 'user'): admin
Email address: admin@example.com
Password:
Password (again):
Superuser created successfully.
```

Run the application and open a web browser to [http://127.0.0.1:8000](http://127.0.0.1:8000)

```shell
$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

Django version 4.0.2, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Docker

Using Docker is by far the easiest way to get started with the demo
application. The instructions below describe the process to get the portal
working with a Docker container.

### Requirements (docker)

The only software requirement here is to make sure you have Docker installed
and working in your local environment.

Docker installation instructions here: [Get Docker](https://docs.docker.com/get-docker/)

### Running (docker)

From a terminal run the following commands:

1. Build the container:

    ```shell
    $ docker build -t oceansmart .
    [+] Building 36.0s (12/12) FINISHED
    => [internal] load build definition from Dockerfile
    => => transferring dockerfile: 674B
    => [internal] load .dockerignore
    => => transferring context: 2.02kB
    => [internal] load metadata for docker.io/library/python:3.9-slim-buster
    => [1/7] FROM docker.io/library/python:3.9-slim-buster
    => [internal] load build context
    => => transferring context: 238.59kB
    => CACHED [2/7] WORKDIR /app
    => CACHED [3/7] RUN pip install pipenv
    => [4/7] COPY Pipfile* /tmp/
    => [5/7] RUN cd /tmp &&   pipenv lock --requirements > requirements.txt &&   pip install -r /tmp/requirements.txt
    => [6/7] COPY . /app
    => [7/7] RUN chmod +x /app/docker-entrypoint.sh &&   groupadd -g 1024 django &&   useradd --no-log-init -u 1024 -g 1024 django &&   chown django:django -R /app
    => exporting to image
    => => exporting layers
    => => writing image sha256:3313633d2fa11c2672fd866d8c0c1a3be60200ac6c5455602a159b6e4b30be4b
    => => naming to docker.io/library/oceansmart
    ```

1. Run the container:

   ```powershell
   $ docker run --rm -it -p 8000:8000 -v ${pwd}:/app -e DJANGO_SUPERUSER_PASSWORD=adminpassword oceansmart
   ```

   This command will run the container that was built but overwrite the working
   directory with the current directory so that the application can use the .env
   file. We also open port 8000 to allow traffic through the container to the host.
   Finally we set a super user password that will be created when you first start the
   container.
