import os
import json
import boto3
from datetime import datetime

def get_boto3_client(service_name):
    """
    LocalStack se connect karne ke liye client banata hai.
    """
    return boto3.client(
        service_name,
        region_name="us-east-1",
        aws_access_key_id="mock",
        aws_secret_access_key="mock",
        endpoint_url="http://localhost:4566"
    )

def discover_leaking_resources():
    """
    Section 4.1: Active EC2 aur Orphaned EBS volumes ko dhoondhta hai.
    """
    ec2_client = get_boto3_client("ec2")
    leaking_resources = {
        "ec2_instances": [],
        "ebs_volumes": []
    }

    # 1. Active EC2 Instances dhoondho
    instances_response = ec2_client.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    
    for reservation in instances_response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance["InstanceId"]
            # Tags nikalne ke liye
            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
            
            leaking_resources["ec2_instances"].append({
                "id": instance_id,
                "type": instance["InstanceType"],
                "launch_time": str(instance["LaunchTime"]),
                "tags": tags
            })

    # 2. Orphaned (Unattached) EBS Volumes dhoondho
    volumes_response = ec2_client.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}] # available matlab unattached
    )
    
    for volume in volumes_response.get("Volumes", []):
        volume_id = volume["VolumeId"]
        tags = {tag["Key"]: tag["Value"] for tag in volume.get("Tags", [])}
        
        leaking_resources["ebs_volumes"].append({
            "id": volume_id,
            "size_gb": volume["Size"],
            "type": volume["VolumeType"],
            "tags": tags
        })

    return leaking_resources

if __name__ == "__main__":
    print("🔍 NimbusKart Cost Janitor Initiating Discovery...")
    found_resources = discover_leaking_resources()
    print(json.dumps(found_resources, indent=4))