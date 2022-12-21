module "ecr-repo" {
    source = "./../../modules/ecr"
    ecr_name = var.ecr_name
    tags = {
    "Environment" = "Prod"
    }
    image_mutability = "MUTABLE"
}