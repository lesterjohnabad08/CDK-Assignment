import os.path
from aws_cdk.aws_s3_assets import Asset as S3asset

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

dirname = os.path.dirname(__file__)

class Assignment3CdkServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_assignment_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Instance Role and SSM Managed Policy
        InstanceRole = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        InstanceRole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        
        # Create an EC2 instance
        cdk_assignment_web_instance = ec2.Instance(self, "cdk_assignment_web_instance", 
                                            vpc=cdk_assignment_vpc,
                                            instance_type=ec2.InstanceType("t2.micro"),
                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                            role=InstanceRole)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Assignment3CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
