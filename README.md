# cad-adminservice
## After cloning:
### cd into cloned folder
### python3 -m venv venv
### source venv/bin/activate
### python -m pip install -r requirements.txt

## To deactivate the venv:
### deactivate

## New python dependencies:
### python -m pip freeze > requirements.txt

## Django env for local
### put the .env Variable in root directory of the repo 

## Terraform
We use a terraform setup with global state management over AWS S3 Backend.
The TF workspace for this service: prod-adminservice
### Terraform AWS secrets for local testing
add a file with the following content and name "secrets.auto.tfvars" in the directory ./terraform/prod/
```sh
access_key = "id"
secret_key = "secret_key"
```

