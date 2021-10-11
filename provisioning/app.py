#!/usr/bin/env python3
import os

from aws_cdk import core

from stacks.announcment_app_stack import AnnouncementStack


app = core.App()
env = core.Environment(account=os.environ.get("CDK_DEFAULT_ACCOUNT", None),
                       region=os.environ.get("CDK_DEFAULT_REGION", None))
AnnouncementStack(app, "AnnouncementStack", env=env)
app.synth()
