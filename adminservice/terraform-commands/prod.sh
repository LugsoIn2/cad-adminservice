terraform -chdir=/cad-terraform-all/prod init
terraform -chdir=/cad-terraform-all/prod workspace select prod
terraform -chdir=/cad-terraform-all/prod apply