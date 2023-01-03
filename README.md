# cad-adminservice
This repository includes the admin service backend written in Django.
## After cloning:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 adminservice/manage.py runserver
```

## To deactivate the venv:
```
deactivate
```
## New python dependencies:
```
python -m pip freeze > requirements.txt
```
## Django env for local
Put the .env Variable in root directory of the repo 

### DJANGO ALLOWED_HOST
Define in the env file the allowed hosts (comma seperated)
ALLOWED_HOSTS="localhost,127.0.0.1" 

## Docker
To be able to build the docker file locally, the [Terraform Repo](https://github.com/LugsoIn2/cad-terraform-all.git) needs to be located in the root directory of this repository.

Github Actions of this repository automatically clone the terraform repository to build the docker file in the action.

 


 

