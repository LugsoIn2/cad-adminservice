#!/bin/bash
customer_id=$1
city=$2
if [[ -n "$customer_id" && -n "$city" ]]; then
    terraform -chdir=/cad-terraform-all/subsc_standard init
    terraform -chdir=/cad-terraform-all/subsc_standard workspace select $customer_id || terraform -chdir=/cad-terraform-all/subsc_standard workspace new $customer_id
    terraform -chdir=/cad-terraform-all/subsc_standard apply -auto-approve -var="scraper_cities=$city"
else
    echo "argument error"
fi