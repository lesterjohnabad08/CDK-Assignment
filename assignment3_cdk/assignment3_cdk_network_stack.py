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


class Assignment3CdkNetworkStack(Stack):

    @property
    def vpc(self):
        return self.cdk_assignment_vpc

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC. CDK by default creates and attaches internet gateway for VPC
        self.cdk_assignment_vpc = ec2.Vpc(self, "cdk_assignment_vpc", 
                            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
                            max_azs=2,
                            subnet_configuration=[
                                ec2.SubnetConfiguration(
                                    name="PublicSubnet",
                                    subnet_type=ec2.SubnetType.PUBLIC
                                    ),
                                ec2.SubnetConfiguration(
                                    name="PrivateSubnet",
                                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                                    )
                                ]
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Assignment3CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
