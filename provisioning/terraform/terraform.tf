# Terraform configuration
#
# Terraform source: https://www.terraform.io/docs/configuration/terraform.html
terraform {
  required_version = "~> 0.14"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.1"
    }
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "~> 3.1"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 1.4"
    }
  }

  # AWS S3 Remote state backend
  #
  # Implements a Terraform backend for storing state remotely so it can be used elsewhere.
  #
  # This backend is configured to use the common BAS Terraform Remote State project.
  #
  # Source: https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state
  # Terraform source: https://www.terraform.io/docs/backends/types/s3.html
  backend "s3" {
    bucket = "bas-terraform-remote-state-prod"
    key    = "v2/BAS-MAGIC-PROJECTS-PORTFOLIO/terraform.tfstate"
    region = "eu-west-1"
  }
}

# DO provider
#
# See https://registry.terraform.io/providers/digitalocean/digitalocean/1.23.0/docs#token
# for how to configure credentials to use this provider.
#
# Terraform source: https://registry.terraform.io/providers/digitalocean/digitalocean/latest
provider "digitalocean" {
}

# GitLab provider
#
# Note: The SAAS GitLab instance is used here rather than the BAS GitLab instance because the DigitalOcean App Platform
# only supports remotes from a limited number of domains.
#
# See https://registry.terraform.io/providers/gitlabhq/gitlab/latest/docs#token
# for how to configure credentials to use this provider.
#
# Terraform source: https://registry.terraform.io/providers/gitlabhq/gitlab/latest
provider "gitlab" {
  base_url = "https://gitlab.com/api/v4/"
}

# Azure Active Directory provider
#
# The BAS preferred identity management provider
#
# See https://www.terraform.io/docs/providers/azuread/guides/azure_cli.html for how to configure credentials to use
# this provider using the Azure CLI.
#
# AWS source: https://azure.microsoft.com/en-us/services/active-directory/
# Terraform source: https://www.terraform.io/docs/providers/azuread/index.html
provider "azuread" {
  # NERC Production AD
  tenant_id = "b311db95-32ad-438f-a101-7ba061712a4e"
}

# MAGIC Projects Portfolio - GitLab mirror
#
# Note: The SAAS GitLab instance is used here rather than the BAS GitLab instance because the DigitalOcean App Platform
# only supports remotes from a limited number of domains. This project will be linked to a corresponding project in the
# BAS GitLab instance using repository mirroring.
#
# Note: The namespace 479738 corresponds to the `antarctica` group.
#
# GitLab source: https://docs.gitlab.com/ee/user/project/
# Terraform source: https://registry.terraform.io/providers/gitlabhq/gitlab/latest/docs/resources/project
resource "gitlab_project" "magic_projects_portfolio_mirror" {
  path             = "magic-projects-portfolio"
  namespace_id     = 479738
  default_branch   = "main"
  visibility_level = "private"

  name        = "Magic Projects Portfolio"
  description = "Proof of concept projects portfolio implementation for MAGIC."

  container_registry_enabled       = false
  issues_enabled                   = false
  lfs_enabled                      = false
  merge_requests_enabled           = false
  packages_enabled                 = false
  pipelines_enabled                = false
  snippets_enabled                 = false
  wiki_enabled                     = false
  remove_source_branch_after_merge = true
}

# MAGIC Projects Portfolio - DigitalOcean Deploy token
#
# To allow the DigitalOcean App Platform access to the GitLab Project.
#
# Note: Tokens created through Terraform requires an expiry date
# Source: https://github.com/gitlabhq/terraform-provider-gitlab/issues/468
#
# GitLab source: https://docs.gitlab.com/ee/user/project/deploy_tokens/
# Terraform source: https://registry.terraform.io/providers/gitlabhq/gitlab/latest/docs/resources/deploy_token
resource "gitlab_deploy_token" "magic_projects_portfolio_mirror_do_app" {
  project    = gitlab_project.magic_projects_portfolio_mirror.id
  name       = "DigitalOcean App Platform"
  username   = "digitalocean"
  expires_at = "2100-01-01T00:00:00Z"
  scopes     = ["read_repository"]
}

# MAGIC Projects Portfolio - DigitalOcean App Platform Application
#
# = Variable interpolation
# As Terraform and the DigitalOcean AppSpec use the same syntax for variable interpolation (${}), escaping is used
# using the `$${}` syntax.
# Source: https://www.terraform.io/docs/configuration/expressions.html#string-literals (end of section)
#
# = Encrypted variables
# on first run, encrypted variables need to be set using cleartext values. They will be encrypted by DigitalOcean and
# then appear in ciphertext in returned state. Values should then be updated to use these ciphertext values.
#
# DigitalOcean source: https://www.digitalocean.com/docs/app-platform/
# Terraform source: https://registry.terraform.io/providers/digitalocean/digitalocean/latest/docs/resources/app
resource "digitalocean_app" "magic_projects_portfolio" {
  spec {
    name   = "magic-projects-portfolio"
    region = "ams"

    service {
      name               = "flask-app"
      environment_slug   = "python"
      instance_count     = 1
      instance_size_slug = "basic-xxs"
      source_dir         = "provisioning/do-app-platform"

      git {
        repo_clone_url = replace(gitlab_project.magic_projects_portfolio_mirror.http_url_to_repo, "https://", "https://${gitlab_deploy_token.magic_projects_portfolio_mirror_do_app.username}:${gitlab_deploy_token.magic_projects_portfolio_mirror_do_app.token}@")
        branch         = "main"
      }

      env {
        key   = "FLASK_ENV"
        value = "production"
        scope = "RUN_AND_BUILD_TIME"
        type  = "GENERAL"
      }
      env {
        key   = "FLASK_SESSION_KEY"
        value = "EV[1:4JbEmGp8j+7vyGQ8upixL1TxhrhPdRf1:J4gWTzZGj4H1WJ2u0EXm1BLOUcZiw8ArYwpisx+9QZBGMzxvTyPkhoiUUcUMKwLU3AgwxTw9BFuDL8h/KeHa6w==]"
        scope = "RUN_AND_BUILD_TIME"
        type  = "SECRET"
      }
      env {
        key   = "AIRTABLE_KEY"
        value = "EV[1:TwjSE/c5G3A/MXoy6mZ08gzce9y1zRR2:iHgKJphlDPI/zgKi6VcdXzzlB95uz4OpZPYANA6GupHh]"
        scope = "RUN_AND_BUILD_TIME"
        type  = "SECRET"
      }
      env {
        key   = "AIRTABLE_BASE"
        value = "appCn6jjVdvP75UbN"
        scope = "RUN_AND_BUILD_TIME"
        type  = "GENERAL"
      }
      env {
        key   = "AUTH_CLIENT_ID"
        value = "44a4edf5-0a30-473d-838e-6bdfb4178c0c"
        scope = "RUN_AND_BUILD_TIME"
        type  = "GENERAL"
      }
      env {
        key   = "AUTH_CLIENT_SECRET"
        value = "EV[1:tB0tmR1Yx+hLAbgMHOPYuCi8XJKDdhjE:UiBCLLaIqccqFuGt+CaSamI3wHET3fVLmaXITymAEcMxMr45lnNxS4kwwtZQ4rInfC0=]"
        scope = "RUN_AND_BUILD_TIME"
        type  = "SECRET"
      }
      env {
        key   = "AUTH_CLIENT_TENANCY"
        value = "https://login.microsoftonline.com/b311db95-32ad-438f-a101-7ba061712a4e"
        scope = "RUN_AND_BUILD_TIME"
        type  = "GENERAL"
      }

      run_command = "waitress-serve --port $PORT bas_magic_projects_portfolio.app:app"
    }
  }
}

# MAGIC Projects Portfolio - Azure AD App Registration
#
# This resource relies on the Azure Active Directory Terraform provider being previously configured
#
# Azure source: https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-how-applications-are-added
# Terraform source: https://www.terraform.io/docs/providers/azuread/r/application.html
resource "azuread_application" "magic_projects_portfolio" {
  display_name               = "MAGIC Projects Portfolio"
  owners                     = ["7aa5b9f2-25c1-4a88-8627-c0d7d1326b55"]
  public_client              = false
  available_to_other_tenants = false
  homepage                   = "https://gitlab.data.bas.ac.uk/MAGIC/magic-projects-portfolio"
  oauth2_allow_implicit_flow = false
  group_membership_claims    = "None"

  reply_urls = [
    "http://localhost:5000/auth/callback",
    "${digitalocean_app.magic_projects_portfolio.live_url}/auth/callback"
  ]

  required_resource_access {
    # Microsoft graph
    resource_app_id = "00000003-0000-0000-c000-000000000000"

    resource_access {
      # 'offline_access' scope
      id   = "7427e0e9-2fba-42fe-b0c0-848c9e6a8182"
      type = "Scope"
    }
    resource_access {
      # 'openid' scope
      id   = "37f7f235-527c-4136-accd-4a02d197296e"
      type = "Scope"
    }
    resource_access {
      # 'email' scope
      id   = "64a6cdd6-aab1-4aaf-94b8-3cc8405e90d0"
      type = "Scope"
    }
    resource_access {
      # 'profile' scope
      id   = "14dad69e-099b-42c9-810b-d002981feec1"
      type = "Scope"
    }
  }

  optional_claims {
    id_token {
      name = "email"
    }
    id_token {
      name = "family_name"
    }
    id_token {
      name = "given_name"
    }
  }

  app_role {
    allowed_member_types = [
      "User"
    ]
    description  = "Read all projects in the MAGIC Projects Portfolio."
    display_name = "BAS.MAGIC.Portfolio.Projects.Read.All"
    is_enabled   = true
    value        = "BAS.MAGIC.Portfolio.Projects.Read.All"
  }

  app_role {
    allowed_member_types = [
      "User"
    ]
    description  = "Update or remove all projects in the MAGIC Projects Portfolio."
    display_name = "BAS.MAGIC.Portfolio.Projects.Write.All"
    is_enabled   = true
    value        = "BAS.MAGIC.Portfolio.Projects.Write.All"
  }
}

# MAGIC Projects Portfolio - Azure AD Enterprise application (security principle)
#
# This resource implicitly depends on the 'azuread_application.magic_projects_portfolio' resource
# This resource relies on the Azure Active Directory Terraform provider being previously configured
#
# Azure source: https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-how-applications-are-added
# Terraform source: https://www.terraform.io/docs/providers/azuread/r/service_principal.html
resource "azuread_service_principal" "magic_projects_portfolio" {
  application_id               = azuread_application.magic_projects_portfolio.application_id
  app_role_assignment_required = true
}
