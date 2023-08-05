# CloudMage GitUtils Python Utility Package Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<br>

## [v0.0.1] - Initial Package Release (2019-02-12)

### Added by: [@rnason](https://github.com/rnason)

- GitHubAPI class to create an object from a retrieved github api request to the repositories /repos endpoint.
- Github Object consisting of properties that match a response from a git api /repos request.
- Created class method to parse a given repository URL, extract, and then set the repository namespace and name properties from the given URL.
- Created class method to handle the request to the the Github API /repos endpoint and store the full response in the .data object property.
- Created class method to handle setting all of the class object properties to the values received from the Github API response JSON object.
- Created logging feature that will allow the class consumer to pass their own log, or to log directly to stdout, stderr.
- Unit Tests for GitHubAPI class.
- Created GitConfigParser Class to retrieve repository configuration based from target directory .git/config file.
- Created class method to parse the url setting out of the .git/config file.
- Created class method to parse the provider setting out of the .git/config file.
- Unit Tests for GitConfigParser class.
