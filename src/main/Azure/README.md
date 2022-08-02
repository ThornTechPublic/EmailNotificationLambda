# Email Alert Add-On for Azure

## Requirements

* [az cli installed](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
* [azure-functions-core-tools@4 installed](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Clinux%2Ccsharp%2Cportal%2Cbash)

## Deployment

This documentation is a reflection of the [Azure Function on Linux with Custom Container](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python)

1. create docker image
2. publish docker image
3. create resource group

```shell
az group create \
    --name <RESOURCE_GROUP_NAME> \
    --location <REGION>
```

4. create storage account

```shell
az storage account create \
    --name <STORAGE_NAME> \
    --location <REGION> \
    --resource-group <RESOURCE_GROUP_NAME> \
    --sku Standard_LRS
```

5. create host plan

```shell
az functionapp plan create \
    --resource-group <RESOURCE_GROUP_NAME> \
    --name <HOST_PLAN_NAME> \
    --location <REGION> \
    --number-of-workers 1 \
    --sku EP1 \
    --is-linux
```

6. create function app

```shell
az functionapp create \
    --name <APP_NAME> \
    --storage-account <STORAGE_NAME> \
    --resource-group <RESOURCE_GROUP_NAME> \
    --plan <HOST_PLAN_NAME> \
    --deployment-container-image-name <DOCKER_ID>/azurefunctionsimage:v1.0.0
```

7. configure function app settings

```shell
az functionapp config appsettings set \
    --name <APP_NAME> \
    --resource-group <RESOURCE_GROUP_NAME> \
    --settings \
      AzureWebJobsStorage=<Connection string from storage account created in step 4> \
      AZURE_STORAGE_CONNECTION_STRING=<Connection string for storage account that houses watched container> \
      SOURCE_LOCATION=<Container which will be watched for new files> \
      SENDER_EMAIL=<Address to send the alerts from> \
      DEST_EMAIL=<Comma-Seperated list of emails that will receive the alerts> \
      PASSWORD=<Password/App Password for the sender email> \
      SMTP_SERVER=<(optional) Name of SMTP server to use> \
      SUBJECT=<(optional) pattern of subject line in email> \
      SENDER_DISP_NAME=<(optional) Display name of sender> \
      PROTOCOL=<(optional) which protocol to use: SSL/TLS>
```

## Deployment through Azure Console
See our blog's article on the topic: https://thorntech.com/deploy-email-alert-add-on-for-sftp-gateway/#AZHeader

## Environment Variables
These values are passed in as environment variables. Make sure to set all required env vars before running

* Required Variables
  * SENDER_EMAIL: Email address of sender account
  * DEST_EMAIL: Email address of receiving account(s)
    * If you wish to send the email to multiple addresses, set DEST_EMAIL to a comma-seperated list of receiving email addresses
  * PASSWORD: Password of sender account
    * This will usually be an app password, such as on Google.
    * See https://support.google.com/accounts/answer/185833?hl=en
  * AZURE_STORAGE_CONNECTION_STRING: Connection string to the storage account containing the container to be monitored
  * SOURCE_LOCATION: Name of container that is to be monitored by the add-on
* Recommended Variables
  * SMTP_SERVER: Which SMTP server to use.
    * Default behavior is to guess the SMTP server based on email, but is not perfect.
    * See https://sendgrid.com/blog/what-is-an-smtp-server/
* Optional Variables
  * SENDER_DISP_NAME: Alias for the sender.
    * Defaults to None
  * SUBJECT: Pattern that the subject line will follow. Some values are substituted in at runtime.
    * Defaults to "A file was uploaded to {LOCATION}!"
    * Substitutions available: {PROVIDER}, {LOCATION}, {NAME}, {SIZE}, {HASH}, {LOCATION_TYPE}
  * PROTOCOL: Which protocol to communicate with.
    * Defaults to "TLS"
    * Allowed options: "TLS", "SSL"
  * LOG_LEVEL: Level the logger should be set to
    * Defaults to "INFO"
    * Allowed options: "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"
  