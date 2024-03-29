# MAGIC Projects Portfolio

Projects portfolio for the [Mapping and Geographic Information Centre (MAGIC)](https://www.bas.ac.uk/team/magic) at the
[British Antarctic Survey](https://www.bas.ac.uk).

[View Portfolio (Restricted, MAGIC)](https://magic-projects-portfolio-895c5.ondigitalocean.app).

**Note:** This project is designed to meet an internal need within MAGIC. It has been open-sourced in case it's of use
to others with similar needs.

## Status

This project is a mature alpha. After some real world testing it will progress to a beta and if successful, a live,
production, service.

Whilst an alpha, there are significant performance limitations, partially complete features, and general rough edges.

## Purpose

This project is intended to help people understand the things MAGIC are working on, at a relatively high 'project'
level. In addition, this Portfolio shows:

1. how these projects relate to the Strategic Objectives and Activity Areas defined in the
   [MAGIC Strategy (Internal)](https://nercacuk.sharepoint.com/sites/BASDigitalw/people-teams/magic/MAGIC%20Documents/MAGIC-Strategy-2021.pdf).
1. how MAGIC team members relate to these projects
1. the status of each project (proposal, complete, historic, etc.)
1. links to more in-depth/detailed information about each project (e.g. proposal documents/plans, specifications, etc.)

These links could include information held in:

* other BAS tools - such as the Digital Workspace, RMS, GitLab, etc.
* external websites - such as UKRI Gateway to Research, ESA funding database, etc.

The audience for this Portfolio is:

* MAGIC team leaders
* MAGIC team members
* other BAS staff (? [#34](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/34) (Internal))
* the public (? [#15](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/15) (Internal))

## Usage

* [MAGIC Projects Portfolio (Restricted)](https://magic-projects-portfolio-895c5.ondigitalocean.app).
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

1. follow the steps to [View Projects](#to-view-projects) to access and sign in to the Projects Portfolio
1. click the name of the project to be deleted
1. on the project details page, for the relevant link, select the broken link icon shown to the right of the sidebar

### Access control

Different permissions are required to access or change projects within the Portfolio website, and/or the backend
database, summarised in the table below:

| Permission                    | Role (Azure)                             | Role (Airtable) | Assigned To          |
| ----------------------------- | ---------------------------------------- | --------------- | -------------------- |
| *view projects*               | `BAS.MAGIC.Portfolio.Projects.Read.All`  | N/A             | MAGIC team members   |
| *change projects*             | `BAS.MAGIC.Portfolio.Projects.Write.All` | N/A             | MAGIC team members   |
| *access the backend database* | N/A                                      | *Editor*        | Specific Individuals |

In most circumstances, only the *view projects* and *change projects* permissions are required to use the Projects
Portfolio. These permissions are assigned to all MAGIC team members (using the central
[MAGIC security group (internal)](https://gitlab.data.bas.ac.uk/MAGIC/general/-/wikis/Azure-authentication#magic-security-group)).

The *access the backend database* permission is only needed to access, and update, the backend Airtable database.
This is not normally needed, and is informally restricted to system administrators. To request permission, please
contact @felnne.

## Implementation

[Airtable](https://airtable.com/tblOq1igQAPd3QcHb) is used as a database and application backend. This tool was chosen
so that the application [Data Model](#data-model) can iterated quickly, as it offers a pre-built admin UI, data entry
forms and API for accessing information.

A Flask application, hosted in the DigitalOcean App Platform, is used as a frontend application. This tool was chosen
to give greater control over how projects are displayed and to allow the backend to be changed in the future without
end-users being aware.

The Flask frontend communicates with the Airtable backend using the Airtable API dynamically at runtime. Microsoft
Azure is used to enforce permissions in the Flask frontend. Airtable permissions are used to control access to the
backend.

### Data model

The data model for this application is held in Airtable, specifically in these tables:

* [schema](https://airtable.com/tblHIqNhOKnt1m56Y/viwJXOfFKPjirDqAv?blocks=hide)
* [set of code lists](https://airtable.com/tblsGJvKQPxLikViW/viwIFtXh5iuxylLsA?blocks=hide)

There have been multiple versions/iterations of this data model. The current revision is **V2**.

#### Projects

Projects represent activities and are the main entity in the data model, other entities relate to back to projects.

#### People

People represent individuals (MAGIC team members), they consist of a name and ORCID iD.

#### Project Links

Project links represent URLs associated with a project (e.g. a link to project's grant proposal or GitLab project).

Project links have a type so the frontend can understand the system it links to. This functionality is not yet used.

#### Project Roles

Project roles represent which people are associated with which projects. These associations are contextual (e.g.
project leader or member).

### Jinja templates

A series of [Jinja2](https://jinja.palletsprojects.com/) templates are used for rendering pages in the *website*
component.

Templates use the [BAS Style Kit Jinja Templates](https://pypi.org/project/bas-style-kit-jinja-templates/).

### Feedback and contact forms

Feedback forms point to the project issue tracker in GitLab, as we are not expecting feedback from externals.

### DigitalOcean App Platform

The [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform/) is used to run this application.
The app platform manages deploying and running the Flask frontend.

This was chosen partly to prove and understand the features this platform offers (for use in other projects), and to
avoid spending time setting up and configuring infrastructure (as this project's usefulness is still unproven).

#### Application Docker Image

The App Platform automatically builds and deploys a container for running the Flask frontend using
[Cloud Native Buildpacks](https://buildpacks.io). For this application, the Python buildpack is used, with the
[`provisioning/do-app-platform/requirements.txt`](/provisioning/do-app-platform/requirements.txt) requirements file
used as an input. This requirements file depends on the [Application Python Package](#python-package).

#### GitLab mirror repository

As the App Platform only supports source code repositories located in Github.com or GitLab.com, it is necessary to
mirror the repository from the BAS GitLab instance to GitLab.com. This is automatic using GitLab's repo mirroring.

### Sentry error tracking

Not yet configured, see [#35 (Internal)](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/35).

### Application logging

Logs for the *website* component are written to *stdout/stderr* as appropriate. In the DigitalOcean App Platform,
logs can be accessed through the [DigitalOcean console](https://cloud.digitalocean.com).

### Authentication and authorisation

For the frontend Flask application, Microsoft Azure's OAuth functionality is used with Active Directory user accounts
from the NERC tenancy.

For the backend Airtable database, Airflow's native permissions system is used with Airtable accounts.

#### Azure Active Directory

The Projects Portfolio is registered as an Azure *App Registration* with an associated security principle.

*App Roles* are defined within this app registration for the different permissions listed in the
[Access Control](#access-control) section (specifically the 'Role (Azure)' column). These permissions are associated
with the users and groups as required through the security principle. Additional ID token claims for the user's name
and email address are used for personalisation. The app registration, roles, claims and other configuration options are
defined as code using [Terraform](#terraform).

The [MSAL for Python](https://msal-python.readthedocs.io) library is used to implement the OAuth authorisation code
grant in the Flask frontend. App roles and optional claims are included as claims in the ID token returned by this
grant, stored in the browser session. The roles claim is checked by methods in the frontend app to verify permissions.

## Configuration

Application configuration options for the Flask frontend are set using environment variables in the DigitalOcean
App Spec in [Terraform](#terraform).

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

### Session length

Configuration options for Flask's session are hard-coded within the application. Their effect is to use permanent
sessions with the fixed duration of 12 hours - meaning users will need to re-authenticate at least every 12 hours.

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

Application templates use the Flask application's Jinja environment configured to load templates from:

* the [BAS Style Kit Jinja Templates](https://pypi.org/project/bas-style-kit-jinja-templates) package
* the [`src/bas_magic_projects_portfolio/templates/`](/src/bas_magic_projects_portfolio/templates/) directory

Styles, components and patterns from the [BAS Style Kit](https://style-kit.web.bas.ac.uk) should be used where possible.
Configuration options for Style Kit Jinja Templates are set in the `app.py` module, including loading local styles and
scripts defined in [`static/`](/src/bas_magic_projects_portfolio/static/).

Application views should inherit from the application layout,
[`app.j2`](/src/bas_magic_projects_portfolio/templates/layouts/app.j2).
[includes](https://jinja.palletsprojects.com/en/2.11.x/templates/#include) and
[macros](https://jinja.palletsprojects.com/en/2.11.x/templates/#macros) should be used to breakdown and reuse content
within views.

### Testing

Not configured, see [#36 (Internal)](https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio/-/issues/36).

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

Commits made against the `main` branch will be mirrored to the
[GitLab.com mirror repository](#gitlab-mirror-repository). This includes the
[`requirements.txt`](/provisioning/do-app-platform/requirements.txt) file used to specify which version of the
application [Application Python Package](#python-package) is installed. This file should be updated as part of each
[Release](#release-procedure).

The DigitalOcean App Platform app will be force deployed during [Continuous Deployment](#continuous-deployment) for
all git tags. Force deploys ensure the [Deployment Docker Container](#application-docker-image) does not cache build
dependencies (i.e. this application).

### Continuous Deployment

All tagged commits will trigger a Continuous Deployment process using GitLab's CI/CD platform, configured in
`.gitlab-ci.yml`.

## Release procedure

For all releases:

1. create a release branch
1. close release in `CHANGELOG.md`
1. bump package version using `poetry version`
1. update `provisioning/do-app-platform/requirements.txt` to match package version
1. push changes, merge the release branch into `main` and tag with version

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
