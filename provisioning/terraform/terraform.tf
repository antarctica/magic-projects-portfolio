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

      run_command = "waitress-serve --port $PORT bas_magic_projects_portfolio.app:app"
    }
  }
}
