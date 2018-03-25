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

## Architecture (i.e., _How_)
### Webhook Receiver
A class with the single responsibility of receiving GitHub webhooks, and enqueuing celery tasks to run based on the type of webhook received.

Each instance of the receiver is it's own celery task, which performs validations (i.e., check to see if user is outside of organization) before enqueuing the event action

Types of webhooks that may be received:

- [Issues](https://developer.github.com/v3/activity/events/types/#issuesevent)
- [Pull Requests](https://developer.github.com/v3/activity/events/types/#pullrequestevent)
- [Pull Request Comments](https://developer.github.com/v3/activity/events/types/#pullrequestreviewcommentevent)
- [Pull Request Reviews](https://developer.github.com/v3/activity/events/types/#pullrequestreviewevent)

### Organization Service
- Checks to see if the GitHub user is outside of the organization. If they are, return true

### Event Actions
Event actions are celery tasks to be enqueued and run in a queue. They follow the command design pattern. Event actions should strive be as stateless as possible

### Models
**Repository**

A public GitHub repository.

```python
has_many :contributors

# Issues for a repository, opened by non-contributors
has_many :issues, dependent: :destroy

# Pull Requests for a repository, opened by non-contributors
has_many :pull_requests, dependent: :destroy
```

**Contributor**

A contributor to a repository.

```python
belongs_to :repositories
```

**Issue**

A community-opened issue on a public GitHub repository.

```python
belongs_to :repositories
```

## Why _Gello_?
Gello was named because it bridges the gap between the GitHub API and the Trello API.

## Features
- autocard, yes/no
- someone from the team would triage it (come up with slash command /schedule)
- open a card based on that
- noisy enough they get attention, but not noisy enough they get ignored


## Development Setup

```
# In one terminal
pyenv activate v-3.6.4
celery worker -A celery_worker.celery --loglevel=info

# In another terminal
pyenv activate v-3.6.4
python manage.py runserver
```


## Deployment to heroku

```
heroku login
heroku apps:create
heroku addons:create heroku-redis -a your_app_name
heroku addons:create heroku-postgresql
```
