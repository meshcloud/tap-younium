terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 5.42.0"
    }
  }
}

provider "github" {
  owner = "meshcloud"
}

data "github_repository" "tap" {
  name = "tap-younium"
}

resource "github_actions_secret" "config" {
  repository      = data.github_repository.tap.name
  secret_name     = "TEST_CONFIG_JSON"
  plaintext_value = file("../../.secrets/config.json")
}
