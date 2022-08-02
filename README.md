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

## Customize Emails
The add-on uses the src/main/res/email.html and src/main/res/email.txt files as templates for the emails it sends.
The html file is the main representation while the txt file is the non-html backup.
In order to send custom emails, edit or replace the email.html and email.txt files with the template you want.

At runtime, the program will substitute some values in as follows (without the quotation marks):

* "{PROVIDER}": Cloud provider that received the file.
* "{LOCATION}": Bucket or container that the file is in. On Azure this is the storage account followed by the container. EX: "{storage account}/{container name}"
* "{FILEPATH}": Filepath of remote file (including folders). EX: users/user1/testfile.txt
* "{DIRECTORY}": Directory of the remote file. EX: users/user1
* "{FILENAME}": Filename of remote file (excluding folders). EX: testfile.txt
* "{SIZE}": Size of uploaded file
* "{HASH}": MD5 hash of uploaded file
* "{LOCATION_TYPE}": "Container" on Azure, "Bucket" otherwise.
* "{USER}": Name of user folder that was uploaded to. EX: If uploaded to users/user1/..., {USER} substitutes to "user1".

Azure only substitutions:

* "{STORAGE_ACCOUNT}": Name of storage account that is uploaded to.
* "{CONTAINER}": Name of container that is uploaded to.

AWS and GCP only substitutions:

* "{BUCKET}": Name of bucket that is uploaded to. (Alias of {LOCATION} substitution)

In the event that a substitution cannot be found, no error is raised and the text is left alone.
These substitutions are done with str.replace() so no functions can be run through it.
