variable "access_key" {

}

variable "secret_key" {
  
}
variable "ecr_name" {
  description = "ECR Repo name"
  type = string
  default = "cad-adminservice"
}

variable "tags" {
    description = "Key-Value maps for tagging"
    type = map(string)
    default = {
    "Environment" = "Prod"
    }
}

variable "image_mutability" {
    description = "image mutable or immutable"
    type = string
    default = "MUTABLE"
}