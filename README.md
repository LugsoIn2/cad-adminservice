# CAD Adminservice
This repository includes the admin service backend written in Django.
## Local Development

### Start local dev server
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 adminservice/manage.py runserver
```

The backend is available at `localhost:8000`

### Deactivate the venv:
```
deactivate
```
### New python dependencies:
```
python -m pip freeze > requirements.txt
```
## Env File
Put the .env Variable in root directory of the repo 
```
AWS_ACCESS_KEY=XXX
AWS_SECRET=XXX
ALLOWED_HOSTS="0.0.0.0,localhost,127.0.0.1,adminservice.docker.internal"
```
## Local Docker Run
To be able to build the docker file locally, the [Terraform Repo](https://github.com/LugsoIn2/cad-terraform-all.git) needs to be located in the root directory of this repository.

Github Actions of this repository automatically clone the terraform repository to build the docker file in the action.

```
git clone <<cad-terraform-all repository>
docker compose up --build
```
The backend is available at `localhost:8000`



 

