# CloudMage GitUtils Python3 Utility Package

<br>

## Description

This utility package was created to allow quick and easy access to Git repository data for a provided repository. The purpose of this library is to be able to either automatically detect a projects configured Git repository by searching for and parsing a .git/config file in a given file path, or to take an input consisting simply of the repositories URL (HTTP | Git formatted) along with an optional access token. Once the repository has been determined by either means, the library will create and return an object instance consisting of the repository data received from the determined providers API parsed into the respective object properties.

<br><br>

## Road Map

Currently this library gathers data from the Githubs main repository API, however, future development will include Gitlab and Bitbucket repository APIs as well. Once all of the main core providers repository API development has been completed commit, issue, release, and other datapoint development is planned.

<br><br>

## Python Version

This library is compatible with Python 3.6 and higher. It may work with earlier versions of Python3 but was not tested against anything earlier then 3.6. As Python 2.x is soon to be end of life, backward compatibility was not taken into consideration.

<br><br>

## Installation

This library has been published to [PyPi](https://pypi.org/project/cloudmage-gitutils/) and can be installed via normal python package manager conventions such as [pip](https://pip.pypa.io/en/stable/) or [poetry](https://pypi.org/project/poetry/).

<br>

```python
pip3 install cloudmage-gitutils
```

<br><br>

## Included Classes

<br>

### GitConfigParser

This class takes a directory path argument, which it uses as a target directory to search for a .git/config file. If a file is found, then the class will parse the URL from the config, and determines the git platform provider from the parsed URL path. This data is then used to return back an object instance with properties set to the parsed values.

<br>

#### GitConfigParser Object Arguments

- `path`: The path of the project or where a valid .git/config file can be found
- `verbose`: Enables verbose mode
- `log`: Redirects standard class log messages to a provided log object.

<br>

#### GitConfigParser Object Properties

- `path`: The path that was used to instantiate the object
- `verbose`: Verbose bool value that can be optionally passed to the class constructor
- `url`: The parsed URL value extracted from the discovered .git/config file
- `provider`: The parsed provider (github, gitlab, or bitbucket currently supported) from the determined URL string
- `user`: If a user was used in the config url, then the value of the configured user will be assigned to this property.
- `log`: The class logger. It will either write directly to stdout, stderr, or to a lob object if one was passed into the object constructor.

<br><br>

#### GitConfigParser Class Usage

```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None
```

<br>

__Optional Verbose Class Constructor Argument:__

When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.

<br>

```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br>

__Optional Log Object:__

When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels (`log.debug()`, `log.info()`, `log.warning()`, `log.error()`) and printed to the passed respective logger object method.

<br>

```python
from cloudmage-gitutils import GitConfigParser

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True, log=GitLog)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

for items in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br><br>

### GitHubAPI

This class takes a git repository URL as input, and then uses that input to construct and send a request to the github api for the targeted repository /repos endpoint. When a response is received and tested for validity, the JSON formatted response object is stored in the .data property, and used to populate the other class object properties listed below.

<br>

#### GitHubAPI Object Arguments

repo_url, auth_token=None, verbose=False, log=None):

- `repo_url`: The https or git formatted URL string of the target git repository
- `auth_token`: Optional git provider authentication token to be set in the API request headers to authenticate the API request.
- `verbose`: Optionally enable verbose class logging
- `log`: Optionally provide log object as argument, and all class logging will be re-routed to the logger object.

<br><br>

#### GitHubAPI Object Properties

- `verbose`: Verbose bool value that can be optionally passed to the class constructor
__Github Properties:__
- `name`: The name of the targeted Git Repository (derived from provided URL string)
- `namespace`: The namespace under which the repository is owned (derived from provided URL string)
- `id`: The repositories Github id
- `access`: Set to either `public` or `private` based on the github repository type
- `http_url`: The HTTPS url of the repository
- `git_url`: The GIT url of the repository
- `mirror`: Repository configured mirror (If configured)
- `description`: The repository description
- `created`: The repository creation date
- `updated`: The date the repository was last updated
- `last_push`: The the date of the last push to the repository
- `size`: The repository size
- `language`: The repository language
- `license`: The repository license
- `archived`: True or False depending on if the repository has been archived
- `disabled`: True or False depending on if the repository has been disabled
- `default_branch`: The repositories default branch, typically `master`
- `fork`: Indicator as to if the repository is a fork of another repository
- `forks`: Number of forks from the repository
- `watchers`: Number of repository watchers
- `stars`: Number of stars on the repository
- `issues`: Indicates if the repository has an issues section
- `open_issues`: Number of open issues in the repositories
- `homepage`: Value of repository homepage if configured
- `wiki`: Indicates if the repository has a wiki
- `pages`: Indicates if the repository has pages enabled
- `downloads`: Indicates if the repository has downloads enabled
- `projects`: Indicates if the repository has projects enabled.
- `owner`: Object containing owner attributes
  - `owner.id`: The github id of the repository owner
  - `owner.name`: The name of the repository owner (github username)
  - `owner.avatar`: The url of the repository owners avatar
  - `owner.url`: The github url for the repository user profile
- `state`: The state of the API request. Either `Success` or `Fail`
- `data`: A dictionary containing the original github JSON response object
- `log`: The class logger. It will either write directly to stdout, stderr, or to a lob object if one was passed into the object constructor.

<br><br>

#### GitHubAPI Class Usage

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}
```

<br>

__Passing an Authentication Token:__

When instantiating the class, an option `auth_token` argument can be provided. The argument is a valid auth token issued from the platform provider. If provided, the auth_token will be passed to the request handler method, where the method will construct request headers including the authentication token for authenticated requests to private repositories.

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}
```

<br>

__Optional Verbose Class Constructor Argument:__

When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.

```python
from cloudmage-gitutils import GitHubAPI

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL, verbose=True)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br>

__Optional Log Object:__

When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels (`log.debug()`, `log.info()`, `log.warning()`, `log.error()`) and printed to the passed respective logger object method.

```python
from cloudmage-gitutils import GitHubAPI

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

RepositoryURL = 'https://github.com/TheCloudMage/Mock-Repository.git'

Repo = GitHubAPI(RepositoryURL, verbose=True, log=GitLog)

repo_name = Repo.name
print(repo_name) # Mock-Repository

repo.url = Repo.http_url
print(repo_provider) # https://github.com/TheCloudMage/Mock-Repository

response_name = Repo.data.get('name')
print(response_name) # Mock-Repository

print(json.dumps, indent=4, sort_keys=True)
# Original github API response object.
{
    'name': 'Mock-Repository',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc',
    'etc': 'etc'
}

for items in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br><br>

## Contacts and Contributions

This project is owned and maintained by [@rnason](https://github.com/rnason)

<br>

To contribute, please:

- Fork the project
- Create a local branch
- Submit Changes
- Create A Pull Request
