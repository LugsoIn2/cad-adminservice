#!/bin/bash
customer_id=$1
city=$2
old_subscription=$3

# Destroy old infrastructure
if [[ -n "$old_subscription" ]]; then
    terraform -chdir=/cad-terraform-all/$old_subscription init
    terraform -chdir=/cad-terraform-all/$old_subscription workspace select $customer_id || terraform -chdir=/cad-terraform-all/$old_subscription workspace new $customer_id
    terraform -chdir=/cad-terraform-all/$old_subscription destroy -auto-approve -var="scraper_cities=$city"
else
    echo "nothing to destroy"
fi