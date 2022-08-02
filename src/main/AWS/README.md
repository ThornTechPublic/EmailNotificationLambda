## Requirements

* AWS CLI with Administrator permission
* [SAM Local installed](https://github.com/awslabs/aws-sam-local)

## Manual Deployment

1. Navigate to [AWS ECR](https://console.aws.amazon.com/ecr/get-started)
2. Create a new ECR repository
3. Build the docker image from the `src/main` directory by running `docker build -f AWSDockerfile -t emailalert .`
4. Follow the instructions from the ECR repository `View Push Commands` button to tag and push the image to the ECR
   repository
6. Go to [AWS Lambda](https://console.aws.amazon.com/lambda/home)
7. Create a new Container image function
8. Browse to your ECR image and create
9. Once the function has been created, go to its configuration tab and set up
   the [environment variables](#lambda-environment-variables) below

Now the email alert lambda should be fully operational, and you can configure the [S3 Event](#bucket-setup) to trigger the
lambda when a file is uploaded to the bucket.

## Bucket setup

1. In the S3 console, go to the SFTP Gateway default bucket
2. In the properties tab, open the Events section
3. Click Add notification
4. Name the notification anything you want, select Event "All object create events", and leave Prefix and Suffix blank,
    select Send to Lambda Function, and select the lambda

## Lambda required permissions

The email alert lambda will require the following permissions to create log streams in CloudWatch

* AWSLambdaBasicExecutionRole

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