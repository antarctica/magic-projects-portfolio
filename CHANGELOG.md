# MAGIC Projects Portfolio - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

**Note:** Issue links in this change log relate to an internal issue tracker.

## [Unreleased]

### Fixed

* Columns in the Projects grid now extend to an even height
  [#55](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/55)
* Project progress (status) being shown when blank
  [#51](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/51)

## [0.3.0] - 2021-04-29

### Added

* Ungrouped projects list (shown by default)
  [#44](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/44)
* Initial temporal extent support for projects (years only)
  [#26](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/26)
* Initial progress/status description for projects
  [#45](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/45)

### Fixed

* Incorrect link to project (old link)
  [#42](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/42)
* Incorrect roles listed for user permissions
  [#42](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/42)
* Various whitespace and other minor corrections
  [#42](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/42)
* Incorrect field used for project link URLs (preventing them from working)
  [#49](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/49)

### Changed

* Application session changed to 12 hours (from indefinite)
  [#43](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/43)
* Splitting sidebar on project details page into multiple sections arranged horizontally to better use space
  [#46](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/46)

## [0.2.0] - 2021-04-21

### Added

* App authentication and authorisation (auth) to restrict access to members of MAGIC using Azure OAuth
  [#8](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/8)
* Initial usage documentation on adding/removing Projects, Project Roles and Project Links
  [#16](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/16)
* New project entities (People, Project Roles)
  [#25](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/25)
* New project properties (acronym, status, duration)
  [#24](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/24)
* CI Environment definition
  [#21](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/21)
* Black formatting watcher in PyCharm
  [#21](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/21)

### Changed

* Improved projects by person view using project roles and people entities
  [#22](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/22)
* Switching to forms for V2 Airtable tables
  [#23](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues23)
* Switching to V2 tables in Airtable for existing properties
  [#21](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/21)

## [0.1.2] - 2021-03-23

### Fixed

* DigitalOcean App Platform deployments
  [#20](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/20)

## [0.1.1] - 2021-03-23

### Fixed

* custom CSS not being included in package
  [#19](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/19)

## [0.1.0] - 2021-03-23

### Added

* Python package
  [#18](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/18)
* Continuous Integration
  [#14](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/14)
* Code linting
  [#14](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/14)
* Project README
  [#1](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/1)
* Project boilerplate files
  [#1](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/1)
* Initial version
  [#11](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/11)
