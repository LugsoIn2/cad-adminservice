#!/bin/bash
customer_id=$1
city=$2
if [[ -n "$customer_id" && -n "$city" ]]; then
    terraform -chdir=/cad-terraform-all/subsc_enterprise init
    terraform -chdir=/cad-terraform-all/subsc_enterprise workspace select $customer_id || terraform -chdir=/cad-terraform-all/subsc_enterprise workspace new $customer_id
    terraform -chdir=/cad-terraform-all/subsc_enterprise apply -auto-approve -var="scraper_cities=$city"
else
    echo "argument error"
fi