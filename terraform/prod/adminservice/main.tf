terraform {
  backend "s3" {
     bucket         = "cad-terraform-state-service"
     key            = "env:/prod-adminservice/terraform.tfstate"
     region         = "eu-central-1"
     dynamodb_table = "terraform_state"
   }
}

#module "eks" {
#  source = "./eks"
#}