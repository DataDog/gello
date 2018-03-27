# Gello :octocat:
A server for managing Trello cards based on GitHub webhook-events
___

## Purpose (i.e., _Why_)
Gello, was developed to help Datadog manage GitHub Issues and Pull Requests open by community members, and incorporate them into our biweekly sprints.

## Features (i.e., _What_)
### GitHub Events
Gello responds to GitHub events on repositories you subscribe to.

**GitHub Pull Request Event**

If a pull request is created by a person outside of the members of an organization on a subscribing repository, a Trello card will be submitted to a board (or list of boards), configurable in the Gello web-UI.

**GitHub Issue Creation Event**

Likewise, if an issue is created by a person outside of the members of an organization on a subscribed repository, a Trello card will be submitted to a board (or list of boards), configurable in the Gello web-UI.

### Web UI
Gello lets you select what members you wish to exclude from the. By default, it excludes all members in an organization.

## Configuration
### Configure the Server
- talk about environment variables you need

### Authenticate With GitHub
- talk about how you can authenticate with your GitHub account

### Subscribe A Repository
- talk about setting up the webhooks URL

## Development Setup

```
# In one terminal
pyenv activate v-3.6.4
celery worker -A celery_worker.celery --loglevel=info

# In another terminal
pyenv activate v-3.6.4
python manage.py runserver
```

## Deployment to Heroku

```bash
# Login with your heroku credentials
heroku login

# Create your application
heroku apps:create --buildpack heroku/python

# Add redis for celery
heroku addons:create heroku-redis -a your_app_name

# Add postgresql for database
heroku addons:create heroku-postgresql

# Verify REDIS and DATABASE exist
heroku addons

# Push the code to heroku
git push heroku master

# Configure your environment variables
heroku config:set ADMIN_EMAIL=email@email.com
heroku config:set ADMIN_PASSWORD=some_password
heroku config:set ADMIN_PASSWORD=some_password
heroku config:set GITHUB_API_TOKEN=your_github_api_token
heroku config:set GITHUB_ORG_LOGIN=the_name_of_your_organization
heroku config:set TRELLO_API_KEY=your_trello_public_key
heroku config:set TRELLO_API_TOKEN=a_trello_token_you_generate

# Start the celery worker on a dyno
heroku ps:scale worker=1

# Open the application
heroku open
```

## Why _Gello_?
Gello was named because it bridges the gap between the GitHub API and the Trello API.
