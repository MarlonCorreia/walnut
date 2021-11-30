locals {
  project = "walnut"
  region  = "us-east-1"
  common_tags = {
    Environment = terraform.workspace
    Project     = "Walnut"
  }
}