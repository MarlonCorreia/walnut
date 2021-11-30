terraform {
  backend "s3" {
    bucket  = "walnut-backend-terraform"
    key     = "terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}