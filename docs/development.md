## Development

### Development Setup

- Docker
- ngrok

#### Installing

1. Building the python image and install dependencies.

   ```bash
   docker-compose build
   ```

2. In root directory of gello, create a .env file following the same format as .env.sample

   ```bash
   cp .env.sample .env
   ```

   Follow [configuration guide](configuration.md) to configure environment variables in .env

3. Running the containers

   ```bash
   docker-compose up
   ```

4. Connect to the gello docker instance

   ```bash
   docker-compose exec app bash
   ```

5. Run the database migrations

   ```bash
   python manage.py db upgrade
   ```

6. Run the deployment command to fetch API Data and create the admin user

   ```bash
   python manage.py deploy
   ```

7. In one terminal, start the worker

   ```bash
   docker-compose exec app bash
   celery worker -A celery_worker.celery --loglevel=info
   ```

8. In another terminal, run the server

   ```bash
   docker-compose exec app bash
   python run.py
   ```

9. Start a ngrok instance

   ```bash
   ngrok http 5000
   ```

10. Copy the https url of the ngrok instance and paste it in the Payload URL of
    your webhooks

11. Open your ngrok URL

12. Log in with your admin credentials `ADMIN_EMAIL` and `ADMIN_PASSWORD`.

### Miscellaneous

If you want to take a look at the database schema, the docker-compose contains
an administrator. You can navigate to http://localhost:8080, select the PostgreSQL database
database and enter the credentials present in the docker-compose file.

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

   ```python
    CreateGitHubWebhook.delay(
      # request.url_root
      url_root='http://7e9ea9dc.ngrok.io/',
      repo_id=create_form.get_repo_id()
    )
   ```

4. Now you can create new webhooks (through creating subscriptions) on Gello, and they would link to the ngrok url (which forwards to your localhost)

5. Don't forget to delete the test webhooks and change the line back when you're done!

#### Manual Testing

Flask comes with its own command line interface (CLI) which comes in handy for testing and debugging within the application context. To use the flask CLI,
simply run the following command from _Gello_'s root directory:

```bash
flask shell
```

If you're familiar with the IPython interface, you can run the flask CLI using IPython by installing a couple packages, then running the same command as above:

```bash
pip install ipython
pip install flask-shell-ipython
flask shell
```

From within the shell, you can access defined classes and call functions from within the application context. This is especially useful when you need to test and
debug parts of the application that require database access. For example, you can check that your database models are working correctly by fetching, creating,
and updating them from within the flask shell:

```python
import app.models as models
from app import db

# Fetch all boards
boards = models.Board.query.all()

# Create a new board
new_board = Board(name="New Board", url="https://example.com", trello_board_id="EXAMPLE")

# Add the new board to the session
db.session.add(new_board)

# edit an existing board
boards[0].name = "new name"

# Persist these changes
db.session.commit()
```

Other possible applications of the flask CLI include testing API service calls and celery tasks with custom inputs.

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

Verify that the `GITHUB_API_TOKEN` and `GITHUB_ORG_LOGIN` are set up correctly in `.env`, and that environment variables are loaded properly.
