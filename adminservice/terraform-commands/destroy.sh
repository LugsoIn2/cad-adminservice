#!/bin/bash
customer_id=$1
if [[ -n "$customer_id" ]]; then
    terraform -chdir=/cad-terraform-all/subsc_enterprise init
    terraform -chdir=/cad-terraform-all/subsc_enterprise workspace select $customer_id || terraform -chdir=/cad-terraform-all/subsc_enterprise workspace new $customer_id
    terraform -chdir=/cad-terraform-all/subsc_enterprise destroy -auto-approve
else
    echo "argument error"
fi