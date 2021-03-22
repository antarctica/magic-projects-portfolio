# MAGIC Projects Portfolio

Proof of concept projects portfolio implementation for MAGIC.

[View Portfolio](https://magic-projects-portfolio-zax8o.ondigitalocean.app/projects/-/group/strategic-objectives).

## Status

This project is an early alpha.

### Projects population

Whilst the data model is development the number of projects contained in the portfolio are very limited and is certainly
not representative of the number of projects happening within MAGIC.

Once it has stabilised, it is expected there the bulk of active projects will be added relatively quickly, followed by
an editing period to consolidate project information and agree common definitions of what is and isn't a project for
example. New projects will then be added as they occur and historic projects may be back populated if it's felt this
would be useful.

### Implementation

Currently [Airtable](https://airtable.com/tblOq1igQAPd3QcHb) is used as a database, backend and data entry/management
interface. This allows the data model can be iterated quickly and to gives a UI for managing data easily.

A [v2 data model (internal)](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/13) is currently
being implemented.

The frontend component is currently a Flask application hosted in the DigitalOcean App Platform. It currently loads
records dynamically from Airtable. As the number of records grow this may prove unsustainable as an approach given
Airtable's rate limits. Once the data model has stabilised it may desirable/necessary to render content statically.

Further information on upcoming changes to this project can be found in the issues and milestones in
[GitLab (internal)](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues).

**Note:** This project is designed to meet an internal need within the
[Mapping and Geographic Information Centre (MAGIC)](https://www.bas.ac.uk/team/magic) at BAS. It has been open-sourced
in case it's of use to others with similar needs.

## Purpose

This project is used to help:

* MAGIC team leaders
* MAGIC team members
* BAS senior leaders
* BAS staff in other teams
* the general public? ([#15](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/15) (Internal))

Understand the activities MAGIC are working on. These are generally called projects but this can be considered any
endeavour including:

* discrete projects or large tasks (e.g. digitising historic mapping)
* grant funded work (e.g. NERC funded science)
* externally focused work (e.g. ESA projects)
* internally commissioned work (e.g. projects that help MAGIC perform its functions)
* advice, training and outreach activities (e.g. drop-in sessions and end-user training)
* business as usual support to BAS or UK Government functions (e.g. MAGIC Helpdesk, Operations support, APC)

These activities span across the various Activity Areas and Strategic Objectives outlined in the [MAGIC Strategy]().

The Projects Portfolio is intended to show:

* how projects/activities fall under these different areas and objectives
* how MAGIC team members relate to these activities
* the status of each activity (ongoing, complete, historic, etc.)
* links to other information about each activity (e.g. grant proposals, project charters, etc.)

It is expected that in-depth/detailed information about each project will be held elsewhere, either in other BAS tools
(such as the Digital Workspace or SharePoint generally) or on websites ran by others (e.g. UKRI Gateway to Research).

This project therefore aims to index high level information about projects only.

## Usage

### To add a project

...

### To edit a project

...

### To remove a project

...

### To add a person to a project

...

### To remove a person from a project

...

### To add a link to a project

...

### To remove a link to a project

...

## Implementation

This project is comprised of several components:

1. data store
    * for holding information about products
    * implemented using an Airtable base with associated input web forms
1. website
    * for displaying projects in the portfolio
    * implemented as a Flask application, hosted in DigitalOcean App Platform

Product information is persisted within the *data store* component using an internally developed
[Data Model](#data-model).

Project information can be managed (created, modified, destroyed) through a User Interface provided by the *data store*
component, accessible to [Project Editors](#project-editors). Information can also be accessed/managed programmatically
through an API.

Project information is displayed within the *website* component, which retrieves information from the *data store*
using its API and renders it using templates. It also includes links to create new projects (via web forms provided by
the *data store* component) and remove existing projects (via the *data store* API).

Access to the *website* component is currently unrestricted (i.e. it is publicly/globally accessible).

### Project editors

Editing rights to data within the *data store* are restricted to MAGIC team leaders and system administrators.

To request changes to existing data please open an [Issue](#issue-tracking)

### Data model

As this project is developed its data model is evolving, it is currently version 2. The data model is currently
defined in Airtable as a:

* [schema](https://airtable.com/tblHIqNhOKnt1m56Y/viwJXOfFKPjirDqAv?blocks=hide)
* [set of code lists](https://airtable.com/tblsGJvKQPxLikViW/viwIFtXh5iuxylLsA?blocks=hide)

#### Projects

Projects represent activities and are the main entity in the data model, other entities relate to back to projects.

#### People

People represent individuals (MAGIC team members), they consist of a name and ORCID iD.

#### Project Links

Project links represent URLs associated with a project (e.g. a link to project's grant proposal or GitLab project).

Project links have a type so that the *website* component can understand the target of each link. Currently this is
only used to highlight where a link relates to the project (e.g. a website for the project) or GitLab/GitHub projects.

#### Project Roles

Project roles represents which people are associated with which projects. These associations are contextual and time
limited (e.g. 'for this project, this person was it's leader from 2010 until 2020').

### Jinja templates

A series of [Jinja2](https://jinja.palletsprojects.com/) templates are used for rendering pages in the *website*
component.

Templates use the [BAS Style Kit Jinja Templates](https://pypi.org/project/bas-style-kit-jinja-templates/) and styled
using the [BAS Style Kit](https://style-kit.web.bas.ac.uk).

### Feedback and contact forms

As this project is not intended for use by external users, feedback forms point to the project issue tracker in GitLab.

### DigitalOcean App Platform

The [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform/) is used to run this application.

This is partly to prove and understand the features this platform offers (for possible use in other projects) and to
avoid spending time setting up and configuring infrastructure (as this project was initially an idea at risk of not
being adopted).

The app platform manages the deployment and runtime of the *website* component. It is controlled by an 'app spec' which
configures:

* the components within the application (currently only a web process)
* the location of the source code repository used for the application
* environment variables used to [Configure](#configuration), and the command to run, the application

#### Application Docker Image

The App Platform automatically builds and deploys a container for running the *website* component using
[Cloud Native Buildpacks](https://buildpacks.io). For this application, the Python buildpack is used, which requires a
`requirements.txt` file to exist within the repository.

This is why when [Python dependencies](#dependencies) are changed, a requirements file needs to be exported from Poetry.
(see [#17](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/17) for more information).

It is possible to simulate the docker image DigitalOcean will build locally if needed for debugging etc.:

```shell
# install `pack` cli https://buildpacks.io/docs/tools/pack/
$ pack build magic-portfolio:latest
$ cd support/buildpacks/
$ docker-compose up
```

**Note:** Environment variables will be loaded from the local `.env` file used in
[Development Environments](#development-environment).

#### GitLab mirror repository

The App Platform currently only supports source code repositories located in:

* www.github.com
* www.gitlab.com

As the source code for this project is primarily held in the [BAS GitLab instance](https://gitlab.data.bas.ac.uk) it
is necessary to mirror the repository from the BAS GitLab instance to GitLab.com. This is automatic using GitLab's
mirroring functionality.

### Sentry error tracking

Not configured.

### Application logging

Logs for the *website* component are written to *stdout/stderr* as appropriate, they can be accessed from the the
DigitalOcean console.

## Configuration

Application configuration options for the *website* component are set using environment variables in the DigitalOcean
App Spec for this project. This specification is managed by Terraform in
[`provisioning/terraform/terraform.tf`](/provisioning/terraform/terraform.tf).

**Note:** In [Development Environments](#development-environment), environment variables are set using a local `.env`
file.

| Configuration Option | Description                                                                | Allowed Values                                                                             | Example Value                                                   |
| -------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| `AIRTABLE_KEY`       | Airtable API key                                                           | valid Airtable API key                                                                     | `keyrD2ea764604m6uQ`                                            |
| `AIRTABLE_BASE`      | Airtable Base ID                                                           | valid Airtable base ID                                                                     | `appKn6jdVjvP75eUC`                                             |
| `FLASK_APP`          | Entry point to Flask application                                           | valid reference to Python module/me                                                        | `bas_magic_projects_portfolio.app`                              |
| `FLASK_ENV`          | Flask environment name                                                     | valid Flask environment name                                                               | `production`                                                    |
| `FLASK_SESSION_KEY`  | Encryption key used to secure Flask sessions                               | [valid Flask session key](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) | `1ca0cb3f8b07fb0a116e4ba9382ea7695e97c4efba50cd7c` [1]          |

[1] Generate with `python3 -c 'import os; print(os.urandom(24).hex())'`.

## Setup

### Terraform

Terraform is used for configuring:

* the [GitLab project in GitLab.com](#gitlab-mirror-repository) as a deployment source for the DigitalOcean App Platform
* DigitalOcean App Platform application

Access to the [BAS DigitalOcean account](https://gitlab.data.bas.ac.uk/WSF/bas-do) are required to provision these
resources.

```
$ cd provisioning/terraform
$ docker-compose run terraform

$ terraform init
$ terraform validate
$ terraform fmt
$ terraform apply

$ exit
$ docker-compose down
```

#### Terraform remote state

State information for this project is stored remotely using a
[Backend](https://www.terraform.io/docs/backends/index.html).

Specifically the [AWS S3](https://www.terraform.io/docs/backends/types/s3.html) backend as part of the
[BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project.

Remote state storage will be automatically initialised when running `terraform init`. Any changes to remote state will
be automatically saved to the remote backend, there is no need to push or pull changes.

##### Remote state authentication

Permission to read and/or write remote state information for this project is restricted to authorised users. Contact
the [BAS Web & Applications Team](mailto:servicedesk@bas.ac.uk) to request access.

See the [BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project for how these
permissions to remote state are enforced.

### Manual steps

Once provisioned the following steps need to be taken manually:

1. configure [repository mirroring](https://gitlab.data.bas.ac.uk/WSF/bas-gitlab#repository-mirroring) between the
   BAS GitLab instance and the corresponding GitLab.com repository created by Terraform

## Development

### Development environment

A local Python virtual environment managed by [Poetry](https://python-poetry.org) is used for development.

```shell
# install pyenv as per https://github.com/pyenv/pyenv#installation and/or install Python 3.8.x
# install Poetry as per https://python-poetry.org/docs/#installation
# install pre-commit as per https://pre-commit.com/
$ poetry config virtualenvs.in-project true
$ git clone https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio.git
$ cd magic-projects-portfolio
$ poetry install
```

**Note:** Use the correct [Python Version](#python-version) for this project.

**Note:** To ensure the correct Python version is used, install Poetry using it's installer, not as a Pip package.

**Note:** Running `poetry config virtualenvs.in-project true` is optional but recommended to keep all project components
grouped together.

**Note:** Read & write access to this source repository is restricted. Contact the project maintainer to request access.

To run a local version of the application:

```shell
$ cp .env.example .env
# update .env with valid configuration option values (e.g. replace any `xxx` values)
$ poetry run flask run
```

### Dependencies

Python dependencies are managed using [Poetry](https://python-poetry.org) which are recorded in `pyproject.toml`.

* use `poetry add` to add new dependencies (use `poetry add --dev` for development dependencies)
* use `poetry update` to update all dependencies to latest allowed versions

Ensure the `poetry.lock` file is included in the project repository.

Ensure the `requirements.txt` file is updated whenever non-development dependencies are changed
`poetry export --format=requirements.txt`. See the [Application Docker Image](#application-docker-image) section for
more information.

Dependencies will be checked for vulnerabilities using [Safety](https://pyup.io/safety/) automatically in
[Continuous Integration](#continuous-integration). Dependencies can also be checked manually:

```shell
$ poetry export --dev --format=requirements.txt --without-hashes | safety check --stdin
```

### Code standards

All files should exclude trailing whitespace and include an empty final line.

Python code should be linted using [Flake8](https://flake8.pycqa.org/en/latest/):

```shell
$ poetry run flake8 src tests
```

This will check various aspects including:

* type annotations (except tests)
* doc blocks (pep257 style)
* consistent import ordering
* code formatting (against Black)
* estimated code complexity
* python anti-patterns
* possibly insecure code (this targets long hanging fruit only)

Python code should follow PEP-8 (except line length), using the [Black](https://black.readthedocs.io) code formatter:

```shell
$ poetry run black src tests
```

These conventions and standards are enforced automatically using a combination of:

* local Git [pre-commit hooks](https://pre-commit.com/) hooks/scripts (Flake8 checks only)
* remote [Continuous Integration](#continuous-integration) (all checks)

To run pre-commit hooks manually:

```shell
$ pre-commit run --all-files
```

### Templates

Application templates use the Flask application's Jinja environment configured to use general templates from the
[BAS Style Kit Jinja Templates](https://pypi.org/project/bas-style-kit-jinja-templates) package (for layouts, etc.) and
application specific templates from the [`templates/`](/templates/) directory.

Styles, components and patterns from the [BAS Style Kit](https://style-kit.web.bas.ac.uk) should be used where possible.
Configuration options for Style Kit Jinja Templates are set in the `app.py` module, including loading local styles and
scripts defined in [`static/`](/static/).

Application views should inherit from the application layout, [`app.j2`](/templates/layouts/app.j2).
[includes](https://jinja.palletsprojects.com/en/2.11.x/templates/#include) and
[macros](https://jinja.palletsprojects.com/en/2.11.x/templates/#macros) should be used to breakdown and reuse content
within views.

### Testing

Not configured.

#### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

## Deployment

### DigitalOcean App Platform (Deployment)

Changes pushed to the project repository (on the BAS GitLab server) will be automatically mirrored to the corresponding
GitLab.com repository which will trigger a deployment within the DigitalOcean App Platform.

See the [GitLab mirror repository](#gitlab-mirror-repository) section for more information.

### Continuous Deployment

Not Configured.

## Release procedure

For all releases:

1. create a release branch
2. close release in `CHANGELOG.md`
3. push changes, merge the release branch into `master` and tag with version

## Feedback

The maintainer of this project is the BAS Mapping and Geographic Information Centre (MAGIC), they can be contacted at:
[magic@bas.ac.uk](mailto:magic@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the
[Issue tracker](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues) for more information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

© UK Research and Innovation (UKRI), 2020 - 2021, British Antarctic Survey.

You may use and re-use this software and associated documentation files free of charge in any format or medium, under
the terms of the Open Government Licence v3.0.

You may obtain a copy of the Open Government Licence at http://www.nationalarchives.gov.uk/doc/open-government-licence/
