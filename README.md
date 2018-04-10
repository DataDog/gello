# Gello
:octocat: A self-hosted server for managing Trello cards based on GitHub webhook-events.

## Overview

Gello was developed by Datadog to help manage community contributions on our open-source GitHub repositories, and incorporate them into our biweekly sprints.

## Wiki Table Of Contents

[Feature Overview](/wiki/Feature-Overview)
  * [Creating a Subscription](/wiki/Feature-Overview#creating-a-subscription)
    * [Autocard](/wiki/Feature-Overview#autocard)
    * [Manual](/wiki/Feature-Overview#manual)
    * [Selecting Your Lists](/wiki/Feature-Overview#selecting-your-lists)
  * [Aggregating Community Contributions](/wiki/Feature-Overview#aggregating-community-contributions)
    * [Issues](/wiki/Feature-Overview#aggregating-community-issues)
    * [Pull Requests](/wiki/Feature-Overview#aggregating-community-pull-requests)

[How it Works](/wiki/How-it-works)
  * [GitHub Webhooks](/wiki/How-it-works#github-webhooks)
  * [GitHub Events](/wiki/How-it-works#github-events)
    * [Pull Request Event](/wiki/How-it-works#pull-request-event)
    * [Issue Event](/wiki/How-it-works#issue-event)
    * [Pull Request Comment Event](/wiki/How-it-works#pull-request-comment-event)
    * [Issue Comment Event](/wiki/How-it-works#issue-comment-event)

[Configuration](/wiki/Configuration)
  * [Configure the Server](/wiki/Configuration#configure-the-server)
    * [GitHub API Token Permissions](/wiki/Configuration#github-api-token)
    * [Trello Configuration](/wiki/Configuration#trello-configuration)

[Deployment](/wiki/Deployment)
  * [Deploying to Heroku](/wiki/Deployment#deploying-to-heroku)

[Development Setup](/wiki/Development-Setup)
  * [macOS Development Setup](/wiki/Development-Setup#macos-development-setup)

## Why _Gello_?
_Gello_ was named because it bridges the gap between the GitHub API and the Trello API.

> Does something not make sense or work as expected? Please open a [pull request](https://github.com/DataDog/gello/compare) to update this documentation. Thank you!
