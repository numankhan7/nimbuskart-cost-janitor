import os
import pytest
import boto3
from moto import mock_aws
from cost_janitor import discover_leaking_resources, clean_resources

@pytest.fixture
def aws_credentials():
    """Mock AWS Credentials pytest ke liye."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["TEST_MODE"] = "true"

@mock_aws
def test_janitor_lifecycle(aws_credentials):
    """Mock environment mein EC2 aur EBS banakar Janitor ka full lifecycle test karna."""
    # 1. Mock EC2 client setup karo aur fake resources banao
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    
    # Fake EC2 Instance banana testing ke liye
    run_instances_response = ec2_client.run_instances(
        ImageId="ami-12345678",
        MinCount=1,
        MaxCount=1,
        InstanceType="t3.micro"
    )
    instance_id = run_instances_response["Instances"][0]["InstanceId"]

    # Fake Orphaned EBS Volume banana testing ke liye
    volume_response = ec2_client.create_volume(
        AvailabilityZone="us-east-1a",
        Size=10,
        VolumeType="gp3"
    )
    volume_id = volume_response["VolumeId"]

    # 2. Test Section 4.1: Discovery Logic
    discovered = discover_leaking_resources()
    
    # Check karo ki script ne running instance aur volume pakda ya nahi
    assert len(discovered["ec2_instances"]) > 0
    assert len(discovered["ebs_volumes"]) > 0
    print(f"\n✅ Discovery Test Passed! Found Mock EC2: {instance_id} and EBS: {volume_id}")

    # 3. Test Section 4.3: Remediation Deletion Logic
    clean_resources(discovered)

    # 4. Verify ki ab sab delete ho chuka hai ya nahi
    post_cleanup_discovered = discover_leaking_resources()
    assert len(post_cleanup_discovered["ec2_instances"]) == 0
    assert len(post_cleanup_discovered["ebs_volumes"]) == 0
    print("✅ Remediation Test Passed! Mock Cloud is 100% cleaned.")