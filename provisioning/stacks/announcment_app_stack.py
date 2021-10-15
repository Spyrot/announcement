import os
import pathlib

import aws_cdk.aws_cognito
from aws_cdk import core as cdk
from aws_cdk import aws_apigateway
from aws_cdk import aws_lambda
from aws_cdk import aws_dynamodb
from aws_cdk import aws_cognito


LAMBDA_ASSET_PATH = os.path.join(pathlib.Path(__file__).parent, os.pardir, "lambda.zip")

# All values and names are hardcoded, these lines should be refined to keep everything parametrized
# according to env


class AnnouncementStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Lambda Function
        lambda_function = aws_lambda.Function(self, "ApiLambda", runtime=aws_lambda.Runtime.PYTHON_3_9,
                                              handler="main.handler",
                                              code=aws_lambda.Code.from_asset(LAMBDA_ASSET_PATH),
                                              environment={"DB_REGION": "us-west-1"})
        # Api Gateway
        api = aws_apigateway.LambdaRestApi(self, "ApiGateway", handler=lambda_function, proxy=False)
        announcements = api.root.add_resource("announcements")
        docs = api.root.add_resource("docs")

        # DynamoDB
        partition_key = aws_dynamodb.Attribute(name="title", type=aws_dynamodb.AttributeType.STRING)
        db = aws_dynamodb.Table(self, "announcements",
                                partition_key=partition_key, table_name="announcements")
        db.grant_read_write_data(lambda_function)

        # Cognito
        sign_in_alias = aws_cdk.aws_cognito.SignInAliases(username=True, email=True)
        auth_flow = aws_cdk.aws_cognito.AuthFlow(user_password=True)
        user_pool = aws_cognito.UserPool(self, "announcement_app_users",
                                         user_pool_name="announcement_app_users",
                                         sign_in_aliases=sign_in_alias)
        user_pool.add_client("app-client", auth_flows=auth_flow, generate_secret=False)
        auth = aws_apigateway.CognitoUserPoolsAuthorizer(self, "usersAuthorizer", cognito_user_pools=[user_pool])
        announcements.add_method("GET", authorizer=auth, authorization_type=aws_apigateway.AuthorizationType.COGNITO)
        announcements.add_method("POST", authorizer=auth, authorization_type=aws_apigateway.AuthorizationType.COGNITO)
