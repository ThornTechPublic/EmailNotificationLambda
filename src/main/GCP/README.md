## Requirements

* [Gcloud cli installed](https://cloud.google.com/sdk/docs/install)

## Manual Deployment

This will outline the steps needed to create a zip packages and deploy it to GCP Cloud Functions.

1. Create the package zip by run the command `python3 deploy/GCP/make_zip.py` from the project root
2. In the [Google Function Console](https://console.cloud.google.com/functions/list), create a new function
3. Leave the environment as `1st gen`, give the function a name, and select a desired region
4. Change the Trigger type to `Cloud Storage` and select event type `finalizing/create`
5. Choose the bucket to watch for uploads and save the trigger
6. Add the environment variables as defined in
   the [Environment Variables section](/README.md#runtime_environment_variables)
7. Then hit next to go to the code section
8. In the runtime selector, choose `Python 3.9`
9. In the source code selector, choose `ZIP Upload`
10. Set the Entry Point to `invoke`
11. Browse to the `depoy/GCP/emailAlertGoogleArchive.zip`
12. Set a staging bucket for the zip file to be deployed from
13. Finally, hit Deploy
    Once the functions is finished deploying any file uploaded to the watched bucket will automatically be
    reported in an email.

## Environment Variable
These values are passed in as environment variables. Make sure to set all required env vars before running

* Required Variables
    * SENDER_EMAIL: Email address of sender account
    * DEST_EMAIL: Email address of receiving account(s)
        * If you wish to send the email to multiple addresses, set DEST_EMAIL to a comma-seperated list of receiving email addresses
    * PASSWORD: Password of sender account
        * This will usually be an app password, such as on Google.
        * See https://support.google.com/accounts/answer/185833?hl=en
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