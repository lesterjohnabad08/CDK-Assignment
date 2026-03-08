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

        # Script in S3 as Asset
        webinitscriptasset = S3asset(self, "Asset", path=os.path.join(dirname, "configure.sh"))

        # Get public subnets
        public_subnets = cdk_assignment_vpc.select_subnets(
            subnet_type=ec2.SubnetType.PUBLIC
        ).subnets
        
        #-----------------------------------------------------------------------
        # Create an EC2 instance Web Server 1 in the public subnet of the VPC
        cdk_assignment_web_instance_1 = ec2.Instance(self, "cdk_assignment_web_instance_1", 
                                            vpc=cdk_assignment_vpc,                                            
                                            vpc_subnets=ec2.SubnetSelection(subnets=[public_subnets[0]]),# this line is to specify the subnet type for the EC2 instance
                                            instance_type=ec2.InstanceType("t2.micro"),
                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                            role=InstanceRole)
        
        # Add the script as a user data command
        asset_path = cdk_assignment_web_instance_1.user_data.add_s3_download_command(
            bucket=webinitscriptasset.bucket,
            bucket_key=webinitscriptasset.s3_object_key
        )

        # Userdata executes script from S3
        cdk_assignment_web_instance_1.user_data.add_execute_file_command(
            file_path=asset_path
            )
        webinitscriptasset.grant_read(cdk_assignment_web_instance_1.role)
        
        # Allow inbound HTTP traffic in security groups
        cdk_assignment_web_instance_1.connections.allow_from_any_ipv4(ec2.Port.tcp(80))

        #-----------------------------------------------------------------------
        # Create an EC2 instance Web Server 2 in the public subnet of the VPC
        cdk_assignment_web_instance_2 = ec2.Instance(self, "cdk_assignment_web_instance_2", 
                                            vpc=cdk_assignment_vpc,                                            
                                            vpc_subnets=ec2.SubnetSelection(subnets=[public_subnets[1]]), # This line is to specify the subnet type for the EC2 instance
                                            instance_type=ec2.InstanceType("t2.micro"),
                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                            role=InstanceRole)
        # Add the script as a user data command
        asset_path = cdk_assignment_web_instance_2.user_data.add_s3_download_command(
            bucket=webinitscriptasset.bucket,
            bucket_key=webinitscriptasset.s3_object_key
        )

        # Userdata executes script from S3
        cdk_assignment_web_instance_2.user_data.add_execute_file_command(
            file_path=asset_path
            )
        webinitscriptasset.grant_read(cdk_assignment_web_instance_2.role)
        
        # Allow inbound HTTP traffic in security groups
        cdk_assignment_web_instance_2.connections.allow_from_any_ipv4(ec2.Port.tcp(80))

         
