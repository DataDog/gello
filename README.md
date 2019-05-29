# Gello
:octocat: A self-hosted server for managing Trello cards based on GitHub webhook-events.

## Overview

Gello was developed by Datadog to help manage community contributions on our open-source GitHub repositories, and incorporate them into our biweekly sprints.

## Contents

1. [Feature Overview](#Feature-Overview)

2. [How it Works](#How-it-Works)

3. [Configuration](#Configuration)

4. [Deployment](#Deployment)

5. [Development Setup](#Development-Setup)


## Why _Gello_?
_Gello_ was named because it bridges the gap between the GitHub API and the Trello API.

> Does something not make sense or work as expected? Please open a [pull request](https://github.com/DataDog/gello/compare) to update this documentation. Thank you!

_Gello_ was developed to help Datadog manage GitHub Issues and Pull Requests opened by community members, and incorporate them into our biweekly sprints.


## Feature Overview

### Creating a Subscription

When you login to _Gello_, you will be prompted to create a new subscription.

![Creating a Subscription](https://github.com/DataDog/gello/blob/master/images/create_subscription.png)

Steps to create a new subscription:

1. Type in the name of the board you wish to create cards to. The input field will autocomplete with values pulled from Trello:

![Board Autocomplete](https://github.com/DataDog/gello/blob/master/images/board_autocomplete.png)

2. Type in the repository name you wish to create cards from. The input field will autocomplete with your organization's public repositories, pulled from GitHub:

![Repository Autocomplete](https://github.com/DataDog/gello/blob/master/images/repo_autocomplete.png)

3. Select if you would like `autocard` functionality for Issues, Pull Requests, or both:

When creating a new subscription, you are prompted to check if you would like the `autocard` setting for GitHub issues, and GitHub pull requests.

#### Autocard

If `autocard` is checked for issues or pull requests, Trello cards will automatically be created when an issue or pull request is created from a GitHub contributor outside of the organization.

#### Manual

If `autocard` is _not_ checked for issues or pull requests, Trello cards will not automatically be created when an issue or pull request is created by an external contributor. However, a person within the GitHub organization may comment `gello create_card` to create a Trello card for the board lists you have subscribed.

#### Selecting Your Lists

_Gello_ lets you select which lists you would like to create cards to for a subscribed board.

Steps to create a Subscribed List:

1. After creating a _subscription_ between a GitHub repository and a Trello board, click on a link under the "Subscribed Lists" column in the subscriptions table:

![Subscriptions](https://github.com/DataDog/gello/blob/master/images/subscriptions_highlight_subscribed_lists.png)

2. Fill out the form to create a subscribed list:

![Create a Subscribed List](https://github.com/DataDog/gello/blob/master/images/create_subscribed_list.png)

### Aggregating Community Contributions

In addition to creating cards on the lists of Trello boards subscribed, Gello keeps track of open community contributions, which are aggregated by GitHub repository, and can be filtered down by Trello board.

#### Aggregating Community Issues

To see open community issues on a repository aggregated by a Trello board, click on a link under the "Issues" column in the subscriptions table:

![Subscriptions Issues Link](https://github.com/DataDog/gello/blob/master/images/subscriptions_highlight_issues.png)

Here there's a paginated listing of all community issues still open, with links to the corresponding GitHub url, and Trello url (for the card created by _Gello_):

![Community Issues By Board](https://github.com/DataDog/gello/blob/master/images/community_issues_by_board.png)

#### Aggregating Community Pull Requests

Likewise, to see open community pull requests on a repository aggregated by a Trello board, click on a link under the "Pull Requests" column in the subscriptions table:

![Subscriptions Issues Link](https://github.com/DataDog/gello/blob/master/images/subscriptions_highlight_pull_requests.png)


## How It Works

_Gello_ works by _subscribing_ Trello boards to GitHub repositories through a web UI, and selecting the corresponding Trello lists you would like cards to be created to following a GitHub event.

### GitHub Webhooks
_Gello_ uses [GitHub webhooks](https://developer.github.com/webhooks/) to get event updates from the repositories subscribed.

When a subscription is made, _Gello_ will create a GitHub webhook on the corresponding repository with the following permissions: `Issues`, `Issue comments`, `Pull requests`, and `Pull request review comments`.

This will allow the server to receive webhook events whenever an issue or pull request is created or commented upon. They are necessary for both the _autocard_ and _manual_ settings.

### GitHub Events
#### Pull Request Event

For the _autocard_ setting, if a pull request is created by a person outside of the members of a GitHub organization on a subscribing repository, a Trello card will be submitted to a board list (or a number of lists), configurable in the _Gello_ web-UI.

#### Issue Event

Likewise, for the _autocard_ setting, if an issue is created by a person outside of the members of a GitHub organization on a subscribed repository, a Trello card will be submitted to a board list (or a number of lists), configurable in the _Gello_ web-UI.

#### Pull Request Comment Event

For the _manual_ setting, if a pull request has been created, and a member of the GitHub organization comments `gello create_card` on the pull request, a Trello card will be submitted to a board list (or a number of lists), configurable in the _Gello_ web-UI.

#### Issue Comment Event

For the _manual_ setting, if an issue has been created, and a member of the GitHub organization comments `gello create_card` on the issue, a Trello card will be submitted to a board list (or a number of lists), configurable in the _Gello_ web-UI.


## Configuration

### Configure the Server

_Gello_ requires certain environment variables to be set for the server to be run correctly.

```bash
# Admin user configuration
ADMIN_EMAIL='an_email_account@gmail.com'
ADMIN_PASSWORD='an_admin_password' # create a password for logging into gello

# Database configuration
DATABASE_URL='the_url_for_a_postgresql_database' # likely postgresql://localhost:5432/your_postgresql_database_name

# Redis configuration
REDIS_URL='the_url_for_a_redis_client' # defaults to 'redis://localhost:6379/0'

# GitHub configuration values
GITHUB_API_TOKEN='An API token for a user with access to your GitHub organization'
GITHUB_ORG_LOGIN='The login for your GitHub organization' # also the name for your Github organization

# Trello configuration values
TRELLO_ORG_NAME='The name for your Trello organization'
TRELLO_API_KEY='A user's public trello API key'
TRELLO_API_TOKEN='An API token generated by the corresponding user'
```

#### GitHub API Token

The GitHub API token you provide should have the following permissions set:

* `public_repo`
* `read:org`
* `write:repo_hook`

![GitHub API Token Permissions](https://github.com/DataDog/gello/blob/master/images/permissions.png)

#### Trello Configuration

_Gello_ requires two environment variables be set to properly configure the Trello integration.

1. `TRELLO_API_KEY`

This is the key found in the [Trello Developer API Keys page](https://trello.com/app-key):

![Trello API Key](https://github.com/DataDog/gello/blob/master/images/developer_api_key.png)

2. `TRELLO_API_TOKEN`

This is a token generated by from the same [Trello Developer API Keys page](https://trello.com/app-key):

![Trello API Token](https://github.com/DataDog/gello/blob/master/images/trello_api_token.png)


## Deployment

### Deploying to Heroku

1. Login with your heroku credentials

```bash
heroku login
```

2. Create your application

```bash
heroku apps:create --buildpack heroku/python
```

3. Add redis add-on for celery worker

```bash
heroku addons:create heroku-redis -a your_app_name
```

4. Add PostgreSQL add-on for database

```bash
heroku addons:create heroku-postgresql
```

5. Verify `REDIS` and `DATABASE` exist

```bash
heroku addons
```

![Addons](https://github.com/DataDog/gello/blob/master/images/heroku_addons.png)

6. Configure your environment variables

```bash
# NOTE: for heroku, you do not need to set the `DATABASE_URL` or `REDIS_URL`
# environment variables, since they are set automatically with the addons
heroku config:set ADMIN_EMAIL=email@email.com
heroku config:set ADMIN_PASSWORD=some_password
heroku config:set GITHUB_API_TOKEN=your_github_api_token
heroku config:set GITHUB_ORG_LOGIN=the_name_of_your_organization
heroku config:set TRELLO_ORG_NAME=your_trello_organization_name
heroku config:set TRELLO_API_KEY=your_trello_public_key
heroku config:set TRELLO_API_TOKEN=a_trello_token_you_generate
```

7. Push the code to heroku

```bash
git push heroku master
```

8. Start the celery worker on a dyno

```bash
heroku ps:scale worker=1
```

9. Open the application
```bash
heroku open
```


## Development Setup

### macOS Development Setup

0. If PostgreSQL and Redis are not installed locally, install them
    ```bash
    brew install postgresql
    brew install redis
    ```

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
    Follow [configuration guide](#Configuration) to configure environment variables in .env

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

### Unit Tests

Unit tests may be run with:

```bash
python manage.py test
```

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
 
