###How to deploy solution
####1. Prerequisites
* AWS CLI installed
* AWS Console Access
* Python3+ installed
* AWS CDK installed
####2. Configure AWS user with programmatic access
1) Login to AWS Console
2) Go to IAM
3) Create user for AWS CDK tool (example: aws_cdk_user)
4) Assign next default permissions to user
    * IAMFullAccess
    * AmazonS3FullAccess
    * AmazonDynamoDBFullAccess
    * AmazonAPIGatewayAdministrator
    * AmazonCognitoPowerUser
    * AWSCloudFormationFullAccess
    * AWSLambda_FullAccess
    
*NOTE:* Permissions are too broad and *should not be used* for prod deployment.
Create custom role for deployment purposes
5) Enable only programmatic access
6) Create user and write down clientID and secret
7) Open terminal and type `aws configure`
8) Paste requested information
9) (Optional) Follow AWS docs for detailed instructions: [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
####3. Run provisioning scripts
1) Go to bin directory 
```shell 
cd ./bin
```
2) Run pack.sh to pack packages and app for lambda deployment
```shell
(Optional) chmod +x pack.sh
./pack.sh
```
3) Run provision.sh to deploy services into the AWS
```shell
(Optional) chmod +x provision.sh
./provision.sh
```
4) Wait for services to be created
5) Use link https://{{api-id}}.execute-api.us-west-1.amazonaws.com/prod from output to access endpoints

### How to retrieve auth token for user in pool
1. Register a user
```shell
aws cognito-idp sign-up --region {your-aws-region} --client-id {your-client-id} --username test_user --password password123
```

2. Confirm user registration
```shell
aws cognito-idp admin-confirm-sign-up --region {your-aws-region} --user-pool-id {your-user-pool-id} --username test_user
```

3. Authenticate (get id token and use it in postman). 
   auth.json in root of repo as example file. Adjust according to your env
```shell
aws cognito-idp admin-initiate-auth --region {your-aws-region} --cli-input-json file://auth.json
```
