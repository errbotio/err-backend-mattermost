# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

##  [3.0.0] 2021-10-20

### Added
  - restructured code to use source layout for pypi packaging.
  - documentation added for readthedocs.

### Changed

### Removed


##  [2.1.0] 2021-11-27

### Added
  - create or use thread when sending message with `in_reply_to`.
  - support of `DIVERT_TO_THREAD` option.
  - ability to define custom event handlers.
  - email field to Person object.
  - cache attributes in order to prevent excessive http requests for Person object.
  
### Changed
  - room occupant no longer processed as list type.
  - code formatted with black.
  - message size limt to 16377 characters.
  - return any combination of first name/surname for Person.fullname without trailing or leading space.
  - moved project to official errbotio organisation https://github.com/errbotio/errbot-mattermost-backend.git
  
### Removed


##  [2.0.2] 2017-11-27

### Added

### Changed
  - channelid to be optional to join a room.
  
### Removed
