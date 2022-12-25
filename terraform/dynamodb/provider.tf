terraform {
    backend "s3" {
     bucket         = "cad-terraform-state-service"
     key            = "terraform.tfstate"
     region         = "eu-central-1"
     dynamodb_table = "terraform_state"
   }
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.38.0"
    }
  }
}

provider "aws" {
    profile = ""
    region = "eu-central-1"
    access_key = var.access_key
    secret_key = var.secret_key
}