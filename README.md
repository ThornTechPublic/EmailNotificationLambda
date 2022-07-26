# Email Alert Add-On

## What is Email Alert Add-On

Email Alert Add-on is an automated alert that is fired when a file is uploaded to a source cloud storage
location in AWS, Azure, and GCP.

## How it works

When files are uploaded to the source cloud storage location, an event is used to trigger the Email Alert add-on,
which sends an SMTP message.

# Instructions for Use and Deployment

## Requirements

* [Python 3.9 installed](https://www.python.org/downloads/)
* [Pipenv installed](https://github.com/pypa/pipenv)
    - `pip install pipenv`
* [AWS requirements](src/main/AWS/README.md#Requirements)
* [Azure requirements](src/main/Azure/README.md#Requirements)
* [GCP requirements](src/main/GCP/README.md#Requirements)


## Environment setup

1. run `pipenv install -r src/provider/requirements.txt`
2. run `pipenv lock && pipenv sync`

## Updating python version

1. Update `required:python_version` in Pipfile to "3.9"
2. run `pipenv install --python=python3.9`

## Updating dependencies

### To unpin dependencies and allow them to be updated

1. modify dependency version in pipfile from `==x.x.x` to `>=x.x.x`
2. run `pipenv update`

### To pin dependencies into a non-updatable state

1. run `pipenv run freeze > src/requirements.txt`
2. run `pipenv install -r src/requriement.txt`

## Shared Module
All cloud providers use the `src/main/res/` module and its contents for sending emails. Before deploying to any 
cloud provider you should copy the contents of the res directory into the provider specific res directory. 

