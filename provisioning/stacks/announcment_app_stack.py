import os
import pathlib

from aws_cdk import core as cdk
from aws_cdk import aws_apigateway
from aws_cdk import aws_lambda
from aws_cdk import aws_dynamodb


LAMBDA_ASSET_PATH = os.path.join(pathlib.Path(__file__).parent, os.pardir, "api-lambda.zip")


class AnnouncementStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Lambda Function
        lambda_function = aws_lambda.Function(self, "ApiLambda", runtime=aws_lambda.Runtime("PYTHON_3_9"),
                                              handler="index.handler",
                                              code=aws_lambda.Code.from_asset(LAMBDA_ASSET_PATH))
        # Api Gateway
        api = aws_apigateway.LambdaRestApi(self, "ApiGateway", handler=lambda_function, proxy=False)
        announcements = api.root.add_resource("announcements")
        announcements.add_method("GET")
        announcements.add_method("POST")
        announcement = announcements.add_resource("{announcement}")
        announcement.add_method("GET")

        # DynamoDB
        partition_key = aws_dynamodb.Attribute(name="title", type=aws_dynamodb.AttributeType.STRING)
        sort_key = aws_dynamodb.Attribute(name="date", type=aws_dynamodb.AttributeType.STRING)
        table = aws_dynamodb.Table(self, "Announcements", partition_key=partition_key, sort_key=sort_key)


if __name__ == '__main__':
    pass
