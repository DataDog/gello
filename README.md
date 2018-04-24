# Gello
:octocat: A self-hosted server for managing Trello cards based on GitHub webhook-events.

## Overview

Gello was developed by Datadog to help manage community contributions on our open-source GitHub repositories, and incorporate them into our biweekly sprints.

## Wiki Table Of Contents

[Feature Overview](https://github.com/DataDog/gello/wiki/Feature-Overview)
  * [Creating a Subscription](https://github.com/DataDog/gello/wiki/Feature-Overview#creating-a-subscription)
    * [Autocard](https://github.com/DataDog/gello/wiki/Feature-Overview#autocard)
    * [Manual](https://github.com/DataDog/gello/wiki/Feature-Overview#manual)
    * [Selecting Your Lists](https://github.com/DataDog/gello/wiki/Feature-Overview#selecting-your-lists)
  * [Aggregating Community Contributions](https://github.com/DataDog/gello/wiki/Feature-Overview#aggregating-community-contributions)
    * [Issues](https://github.com/DataDog/gello/wiki/Feature-Overview#aggregating-community-issues)
    * [Pull Requests](https://github.com/DataDog/gello/wiki/Feature-Overview#aggregating-community-pull-requests)

[How it Works](https://github.com/DataDog/gello/wiki/How-it-works)
  * [GitHub Webhooks](https://github.com/DataDog/gello/wiki/How-it-works#github-webhooks)
  * [GitHub Events](https://github.com/DataDog/gello/wiki/How-it-works#github-events)
    * [Pull Request Event](https://github.com/DataDog/gello/wiki/How-it-works#pull-request-event)
    * [Issue Event](https://github.com/DataDog/gello/wiki/How-it-works#issue-event)
    * [Pull Request Comment Event](https://github.com/DataDog/gello/wiki/How-it-works#pull-request-comment-event)
    * [Issue Comment Event](https://github.com/DataDog/gello/wiki/How-it-works#issue-comment-event)

[Configuration](https://github.com/DataDog/gello/wiki/Configuration)
  * [Configure the Server](https://github.com/DataDog/gello/wiki/Configuration#configure-the-server)
    * [GitHub API Token Permissions](https://github.com/DataDog/gello/wiki/Configuration#github-api-token)
    * [Trello Configuration](https://github.com/DataDog/gello/wiki/Configuration#trello-configuration)

[Deployment](https://github.com/DataDog/gello/wiki/Deployment)
  * [Deploying to Heroku](https://github.com/DataDog/gello/wiki/Deployment#deploying-to-heroku)

[Development Setup](https://github.com/DataDog/gello/wiki/Development-Setup)
  * [macOS Development Setup](https://github.com/DataDog/gello/wiki/Development-Setup#macos-development-setup)
  * [Running Unit Tests](https://github.com/DataDog/gello/wiki/Development-Setup#unit-tests)
  * [Generating Coverage Reports](https://github.com/DataDog/gello/wiki/Development-Setup#coverage-reports)

## Why _Gello_?
_Gello_ was named because it bridges the gap between the GitHub API and the Trello API.

> Does something not make sense or work as expected? Please open a [pull request](https://github.com/DataDog/gello/compare) to update this documentation. Thank you!
