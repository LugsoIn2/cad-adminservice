#!/bin/bash
customer_id=$1
if [[ -n "$customer_id" ]]; then
    terraform -chdir=/cad-terraform-all/subsc_standard init
    terraform -chdir=/cad-terraform-all/subsc_standard workspace select $customer_id || terraform -chdir=/cad-terraform-all/subsc_standard workspace new $customer_id
    terraform -chdir=/cad-terraform-all/subsc_standard apply -auto-approve
else
    echo "argument error"
fi