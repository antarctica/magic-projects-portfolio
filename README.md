# MAGIC Projects Portfolio

Proof of concept projects portfolio implementation for MAGIC.

[View Portfolio](https://magic-projects-portfolio-zax8o.ondigitalocean.app).

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
## Usage

This project therefore aims to index high level information about projects only.
* [MAGIC Projects Portfolio (Restricted)](https://magic-projects-portfolio-zax8o.ondigitalocean.app).
* [MAGIC Projects Portfolio database [Airtable] (Restricted)](https://airtable.com/tblMOrCQYic2zq3R8).

### To view projects

**Note:** You need permission to *view projects* to complete this task. See the [Access Control](#access-control)
section for more information.

1. visit the MAGIC Projects Portfolio
1. click the *Sign in to Continue* button
1. if prompted, sign in to your BAS/NERC account (i.e. the account you use for your BAS email)
1. if promoted, allow the Projects Portfolio to access your basic profile information (only needed once)

### To add a project

**Note:** You need permission to *view projects* and *change projects* to complete this task. See the
[Access Control](#access-control) section for more information.

1. follow the steps to [View Projects](#to-view-projects) to access and sign in to the Projects Portfolio
1. click the green *Add Project* button in the top right
1. complete the web-form as directed

### To edit a project

**Note:** You need permission to *access the backend database* to complete this task. See the
[Access Control](#access-control) section for more information.

1. visit the MAGIC Projects Portfolio database [Airtable]
1. select the relevant table with the `(V2)` prefix (consult the 'Data Model (V2)' if unsure which table to edit)
1. make adjustments as needed

### To remove a project

**Note:** You need permission to *view projects* and *change projects* to complete this task. See the
[Access Control](#access-control) section for more information.

1. follow the steps to [View Projects](#to-view-projects) to access and sign in to the Projects Portfolio
1. click the name of the project to be deleted
1. on the project details page, click the *Delete Project* button from the bottom of the sidebar to the right

### To add a person to a project

**Note:** You need permission to *view projects* and *change projects* to complete this task. See the
[Access Control](#access-control) section for more information.

1. follow the steps to [View Projects](#to-view-projects) to access and sign in to the Projects Portfolio
1. click the name of the project to be deleted
1. on the project details page, click the *Add Role* button from the bottom of the sidebar to the right
1. complete the web-form as directed

### To remove a person from a project

**Note:** You need permission to *access the backend database* to complete this task. See the
[Access Control](#access-control) section for more information.

1. follow the steps to [Edit Projects](#to-edit-a-project) to access Projects Portfolio database
1. choose the *Project Roles (V2)* table
1. remove the relevant row associating a person with a project

See [#28](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/28) for making this task self-service.

### To add a link to a project

**Note:** You need permission to *view projects* and *change projects* to complete this task. See the
[Access Control](#access-control) section for more information.

1. follow the steps to [View Projects](#to-view-projects) to access and sign in to the Projects Portfolio
1. click the name of the project to be deleted
1. on the project details page, click the *Add Link* button from the bottom of the sidebar to the right
1. complete the web-form as directed

### To remove a link to a project

**Note:** You need permission to *view projects* and *change projects* to complete this task. See the
[Access Control](#access-control) section for more information.

## Implementation
1. follow the steps to [View Projects](#to-view-projects) to access and sign in to the Projects Portfolio
1. click the name of the project to be deleted
1. on the project details page, for the relevant link, select the broken link icon shown to the right of the sidebar

This project is comprised of several components:
### Access control

1. data store
    * for holding information about products
    * implemented using an Airtable base with associated input web forms
1. website
    * for displaying projects in the portfolio
    * implemented as a Flask application, hosted in DigitalOcean App Platform
Different permissions are required to access or change projects within the Portfolio website, and/or the backend
database, summarised in the table below:

Product information is persisted within the *data store* component using an internally developed
[Data Model](#data-model).
| Permission                    | Role (Azure)                             | Role (Airtable) | Assigned To          |
| ----------------------------- | ---------------------------------------- | --------------- | -------------------- |
| *view projects*               | `BAS.MAGIC.Portfolio.Projects.Write.All` | N/A             | MAGIC team members   |
| *change projects*             | `BAS.MAGIC.Portfolio.Projects.Read.All`  | N/A             | MAGIC team members   |
| *access the backend database* | N/A                                      | *Editor*        | Specific Individuals |

Project information can be managed (created, modified, destroyed) through a User Interface provided by the *data store*
component, accessible to [Project Editors](#project-editors). Information can also be accessed/managed programmatically
through an API.
In most circumstances, only the *view projects* and *change projects* permissions are required to use the Projects
Portfolio. These permissions are assigned to all MAGIC team members (using the central
[MAGIC security group (internal)](https://gitlab.data.bas.ac.uk/MAGIC/general/-/wikis/Azure-authentication#magic-security-group)).

Project information is displayed within the *website* component, which retrieves information from the *data store*
using its API and renders it using templates. It also includes links to create new projects (via web forms provided by
the *data store* component) and remove existing projects (via the *data store* API).
The *access the backend database* permission is only needed to access, and update, the backend Airtable database.
This is not normally needed, and is informally restricted to system administrators. To request permission, please
contact @felnne.

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
[Cloud Native Buildpacks](https://buildpacks.io). For this application, the Python buildpack is used using the
[`provisioning/do-app-platform/requirements.txt`](/provisioning/do-app-platform/requirements.txt) requirements file.

This file depends on the [Application Python Package](#python-package).

#### GitLab mirror repository

The App Platform currently only supports source code repositories located in:

* www.github.com
* www.gitlab.com
### Authentication and authorisation

As the source code for this project is primarily held in the [BAS GitLab instance](https://gitlab.data.bas.ac.uk) it
is necessary to mirror the repository from the BAS GitLab instance to GitLab.com. This is automatic using GitLab's
mirroring functionality.
For the frontend Flask application, Microsoft Azure's OAuth functionality is used with Active Directory user accounts
from the NERC tenancy.

### Sentry error tracking
For the backend Airtable database, Airflow's native permissions system is used with Airtable accounts.

Not configured.
#### Azure Active Directory

### Application logging
The Projects Portfolio is registered as an Azure *App Registration* with an associated security principle.

*App Roles* are defined within this app registration for the different permissions listed in the
[Access Control](#access-control) section (specifically the 'Role (Azure)' column). These permissions are associated
with the users and groups as required through the security principle. Additional ID token claims for the user's name
and email address are used for personalisation. The app registration, roles, claims and other configuration options are
defined as code using [Terraform](#terraform).

Logs for the *website* component are written to *stdout/stderr* as appropriate, they can be accessed from the the
DigitalOcean console.
The [MSAL for Python](https://msal-python.readthedocs.io) library is used to implement the OAuth authorisation code
grant in the Flask frontend. App roles and optional claims are included as claims in the ID token returned by this
grant, stored in the browser session. The roles claim is checked by methods in the frontend app to verify permissions.

## Configuration

Application configuration options for the *website* component are set using environment variables in the DigitalOcean
App Spec for this project. This specification is managed by Terraform in
[`provisioning/terraform/terraform.tf`](/provisioning/terraform/terraform.tf).

**Note:** In [Development Environments](#development-environment), environment variables are set using a local `.env`
file.

| Configuration Option  | Description                                   | Example Value                                                                |
| --------------------- | --------------------------------------------- | ---------------------------------------------------------------------------- |
| `FLASK_APP`           | Entry point to Flask application              | `bas_magic_projects_portfolio.app`                                           |
| `FLASK_ENV`           | Flask environment name                        | `production`                                                                 |
| `FLASK_SESSION_KEY`   | Encryption key used to secure Flask sessions  | `65682e1a8e545f881b38c14e9bcfba9cfc0cdd1151479b88` [1]                       |
| `AIRTABLE_KEY`        | Airtable API key                              | `keyrD2ea764604m6uQ`                                                         |
| `AIRTABLE_BASE`       | Airtable Base ID                              | `appKn6jdVjvP75eUC`                                                          |
| `AUTH_CLIENT_ID`      | Azure App Registration client ID              | `44a4edf5-0a30-473d-838e-6bdfb4178c0c` [2]                                   |
| `AUTH_CLIENT_SECRET`  | Azure App Registration client secret          | `JgxIzLfbV5j.jJ0s~HNDib_Mbs72nA-3x1` [3]                                     |
| `AUTH_CLIENT_TENANCY` | Azure tenancy containing the App Registration | `https://login.microsoftonline.com/b311db95-32ad-438f-a101-7ba061712a4e` [2] |

[1] Generate with `python3 -c 'import os; print(os.urandom(24).hex())'`, see the
[Flask quick start](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) for more information.

[2] Retrieve these details from the Azure Portal for the application registration for this project.

[3] Generate through the Azure Portal, see the
[Microsoft documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret)
for more information.

## Setup

### Terraform

Terraform resources are defined in [`provisioning/terraform/terraform.tf`](/provisioning/terraform/terraform.tf).

[Terraform](https://terraform.io) is used for configuring:

* the [GitLab project in GitLab.com](#gitlab-mirror-repository) as a deployment source for the DigitalOcean App Platform
* the [DigitalOcean App Platform](#digitalocean-app-platform) application
* the [Microsoft Azure App Registration](#authentication-and-authorisation) (including app roles and claims)

Access to the [BAS DigitalOcean account](https://gitlab.data.bas.ac.uk/WSF/bas-do) and NERC Azure Tenancy are
required to provision these resources. Docker and Docker Compose are required to run the Terraform binary required for
resources in this project.

**Note:** This Terraform configuration needs to be applied in stages, as resources need to be manually configured before
others are created. See the numbered steps in the commands below:

```shell
# step 1 - create Terraform container (includes Azure CLI client)
$ cd provisioning/terraform
$ docker-compose run terraform

# step 2 - setup Terraform and ensure syntax is valid and formatting normalised
$ terraform init
$ terraform validate
$ terraform fmt

# step 3 - sign in to Azure CLI to allow access to Azure managed resources
$ az login --allow-no-subscriptions

# step 4  - create Azure resources
$ terraform apply --target azuread_application.magic_projects_portfolio
$ terraform apply --target azuread_service_principal.magic_projects_portfolio

# step 5 - configure Azure resources (see manual steps section)

# step 6 - create the GitLab mirror repository
$ terraform apply --target gitlab_project.magic_projects_portfolio_mirror
$ terraform apply --target gitlab_deploy_token.magic_projects_portfolio_mirror_do_app

# step 7 - configure repository mirroring (see manual steps section)

# step 8 - set DigitalOcean encrypted variables to initial cleartext values (see notes in terraform.tf)

# step 9 - create DigitalOcean app
$ terraform apply --target digitalocean_app.magic_projects_portfolio

# step 10  - retrieve ciphertext values for encrypted env variables from spec in DigitalOcean console
#           and update configuration to match

# step 11 - ensure all changes are in sync (Terraform should report no changes will be made)
$ terraform plan

# step 12 - if ok, apply configuration to update state
$ terraform apply

# step 13 - quit and remove Terraform container
$ exit
$ docker-compose down
```

#### Manual steps

##### Azure resources

To configure the app registration:

1. login to the [Azure Portal](https://portal.azure.com) and select *Azure Active Directory* -> *App registrations*
1. select the app registration representing this project
1. select the *Branding* page:
   * set the *Logo* to the project avatar from
   * set the *Homepage* to the Flask frontend endpoint
   * set the *Publisher domain* to *bas.ac.uk*
1. select the *Certificates & secrets* page and click the *New client secret* button:
   * set the *Description* to: `app`
   * set *Expires* to: *24 months*
1. select the *Manifest* page:
   * set the `accessTokenAcceptedVersion` property to: `2`

Once complete, copy the relevant client ID, secret and tenancy endpoint from the app registration for use in settings.

To configure the service principle (app roles):

1. login to the [Azure Portal](https://portal.azure.com) and select *Azure Active Directory* ->
   *Enterprise applications*
1. select the app registration representing this project (hint: search by application ID, name is unreliable)
1. select the *Properties* page:
   * set *User assignment required?* to: *Yes*
1. select the *Users & groups* page and click the *Add user/group* button:
   * for *User and groups*: click to add selections and search for the `G_BAS_MAGIC_App` group
   * for *Select a role*: click to add selects and choose `BAS.MAGIC.Portfolio.Projects.Read.All`
1. repeat the previous step, choosing the same group but with the `BAS.MAGIC.Portfolio.Projects.Write.All` role

**Note:** If permissions are broadened from just MAGIC, move this section to usage or implementation sections.

##### Repository mirroring

1. configure [repository mirroring](https://gitlab.data.bas.ac.uk/WSF/bas-gitlab#repository-mirroring) between the
   BAS GitLab instance and the corresponding GitLab.com repository created by Terraform by creating a personal
   access token in GitLab.com

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

### Python Package

This project is distributed as a Python package, available through the 
[BAS GitLab Python registry](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/packages), installable 
using Pip.

Both source and binary (Python wheel) packages are built automatically during 
[Continuous Deployment](#continuous-deployment) for all tagged releases.

A shared public access deploy token is used to allow this Python package to installed anonymously:

* username: `anonymous-public-access`
* password: `PxsyfybkCmKDNYWUXCzs`

To install using Pip:

```shell
$ python3 -m pip install bas-magic-projects-portfolio --extra-index-url https://anonymous-public-access:PxsyfybkCmKDNYWUXCzs@gitlab.data.bas.ac.uk/api/v4/projects/853/packages/pypi/simple
```

### DigitalOcean App Platform (Deployment)

Commits made against the master branch will be mirrored to the 
[GitLab.com mirror repository](#gitlab-mirror-repository), which will update the `requirements.txt` file used to 
specify which version of the application [Application Python Package](#python-package) is installed.

A forced deployment of the DigitalOcean App Platform app will be triggered automatically during
[Continuous Deployment](#continuous-deployment) for all tagged releases.

A force deployment is used to ensure the [Deployment Docker Container](#application-docker-image) is updated to use the 
application [Application Python Package](#python-package) version specified in the `requirements.txt` file.

### Continuous Deployment

All tagged commits will trigger a Continuous Deployment process using GitLab's CI/CD platform, configured in
`.gitlab-ci.yml`.

## Release procedure

For all releases:

1. create a release branch
1. close release in `CHANGELOG.md`
1. bump package version using `poetry version`
1. update `provisioning/do-app-platform/requirements.txt` to match package version
1. push changes, merge the release branch into `master` and tag with version

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
