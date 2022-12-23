terraform {
  backend "s3" {
     bucket         = "cad-terraform-state-service"
     key            = "terraform.tfstate"
     region         = "eu-central-1"
     dynamodb_table = "terraform_state"
   }
}

module "ecr-repo" {
    source = "./../../modules/ecr"
    ecr_name = var.ecr_name
    tags = {
    "Environment" = "Prod"
    }
    image_mutability = "MUTABLE"
}