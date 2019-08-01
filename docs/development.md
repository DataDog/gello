## Development

### Development Setup

#### Prerequisites

- macOS
- PostgreSQL
    ```bash
    brew install postgresql
    ```
- Redis (make sure the server runs on default port - 6379)
    ```bash
    brew install redis
    redis-server
    ```

#### Installing

1. Install the pip package manager

    ```bash
    sudo easy_install pip
    ```

2. Install [Pyenv with brew](https://github.com/pyenv/pyenv#homebrew-on-mac-os-x)

    ```bash
    brew update
    brew install pyenv pyenv-virtualenv
    ```

3. Install Python 3.6.4 with Pyenv

    ```bash
    pyenv install 3.6.4
    ```

4. Create and activate `virtualenv` with Python 3.6.4

    ```bash
    pyenv virtualenv 3.6.4 v-3.6.4
    pyenv activate v-3.6.4
    ```

5. Install the dependencies

    ```bash
    pip install pipenv
    pipenv install
    ```

6. Create a PostgreSQL database

    ```bash
    createdb your_postgresql_database_name
    ```

7. In root directory of gello, create a .env file following the same format as .env.sample

    ```bash
    cp .env.sample .env
    ```
    Follow [configuration guide](configuration.md) to configure environment variables in .env

8. Run the database migrations

    ```bash
    python manage.py db upgrade
    ```

9. Run the deployment command to fetch API Data and create the admin user

    ```bash
    python manage.py deploy
    ```

10. In one terminal, start the worker

    ```bash
    pyenv activate v-3.6.4
    celery worker -A celery_worker.celery --loglevel=info
    ```

11. In another terminal, run the server

    ```bash
    pyenv activate v-3.6.4
    python run.py
    ```

### Testing

#### Unit Tests

Unit tests may be run with:

```bash
python manage.py test
```

Gello will use the `TEST_DATABASE_URL` as the database when you run tests, so be sure to export it before running `python manage.py test`.

```bash
export TEST_DATABASE_URL='the_url_for_a_postgresql_database'
```

#### Integration Tests

1. Follow [instructions](https://ngrok.com/download) to download and setup ngrok

2. Expose localhost (usually port 5000)

    ```bash
    ./ngrok http 5000
    ```
    You should see a line that looks similar to this:

    ```bash
    Forwarding    http://7e9ea9dc.ngrok.io -> 127.0.0.1:5000
    ```

3. Copy the url `*.ngrok.io`

    In [views.py](../app/controllers/subscriptions/views.py), replace the value of `url_root` with this url (temporarily for testing)

    ```bash
    CreateGitHubWebhook.delay(
        url_root='http://7e9ea9dc.ngrok.io/', # request.url_root,
        repo_id=create_form.get_repo_id()
    )
    ```

4. Now you can create new webhooks (through creating subscriptions) on Gello, and they would link to the ngrok url (which forwards to your localhost)

5. Don't forget to delete the test webhooks and change the line back when you're done!


### Coverage Reports

Coverage reports may be generated with:

```bash
coverage run --source=app manage.py test
coverage report
```

### Common Errors

Below are errors that you might encounter during local set-up and their solutions:

#### ZipImportError
> zipimport.ZipImportError: can't decompress data; zlib not available

Run '`brew info zlib`', and follow output instructions to set corresponding environment variables.

#### pyenv-virtualenv Initialization Error
> Failed to activate virtualenv. Perhaps pyenv-virtualenv has not been loaded into your shell properly. Please restart current shell and try again.

Add the following to your bashrc file ( ~/.bashrc):

```bash
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

#### GithubException
> github.GithubException.RateLimitExceededException: 403 {'message': "API rate limit exceeded."}

Verify that the *GITHUB_API_TOKEN* and *GITHUB_ORG_LOGIN* are set up correctly in *.env*, and that environment variables are loaded properly.
