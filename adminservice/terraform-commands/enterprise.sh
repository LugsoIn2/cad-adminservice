#!/bin/bash
customer_id=$1
city=$2
old_subscription=$3

# Destroy old infrastructure
if [[ -n "$old_subscription" ]]; then
    terraform -chdir=/cad-terraform-all/$old_description init
    terraform -chdir=/cad-terraform-all/$old_description workspace select $customer_id || terraform -chdir=/cad-terraform-all/subsc_enterprise workspace new $customer_id
    terraform -chdir=/cad-terraform-all/$old_description destroy -auto-approve -var="scraper_cities=$city"
else
    echo "nothing to destroy"
fi

# Apply new infrastructure
if [[ -n "$customer_id" && -n "$city" ]]; then
    terraform -chdir=/cad-terraform-all/subsc_enterprise init
    terraform -chdir=/cad-terraform-all/subsc_enterprise workspace select $customer_id || terraform -chdir=/cad-terraform-all/subsc_enterprise workspace new $customer_id
    terraform -chdir=/cad-terraform-all/subsc_enterprise apply -auto-approve -var="scraper_cities=$city"
else
    echo "argument error"
fi