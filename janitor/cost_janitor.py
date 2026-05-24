import os
import json
import boto3
from datetime import datetime, timezone

def get_boto3_client(service_name):
    """LocalStack se connect karne ke liye client configuration (Test friendly)."""
    # Agar TEST_MODE environment variable set hai, toh endpoint_url mat daalo (Moto handle karega)
    if os.environ.get("TEST_MODE") == "true":
        return boto3.client(
            service_name,
            region_name="us-east-1"
        )
        
    # Normal execution mein LocalStack use karo
    return boto3.client(
        service_name,
        region_name="us-east-1",
        aws_access_key_id="mock",
        aws_secret_access_key="mock",
        endpoint_url="http://localhost:4566"
    )

def discover_leaking_resources():
    """Section 4.1: Active EC2 aur Orphaned EBS volumes ko dhoondhta hai."""
    ec2_client = get_boto3_client("ec2")
    leaking_resources = {
        "ec2_instances": [],
        "ebs_volumes": []
    }

    # 1. Running EC2 Instances dhoondho
    instances_response = ec2_client.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    for reservation in instances_response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
            leaking_resources["ec2_instances"].append({
                "id": instance["InstanceId"],
                "type": instance["InstanceType"],
                "launch_time": str(instance["LaunchTime"]),
                "tags": tags
            })

    # 2. Unattached/Available EBS Volumes dhoondho
    volumes_response = ec2_client.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    for volume in volumes_response.get("Volumes", []):
        tags = {tag["Key"]: tag["Value"] for tag in volume.get("Tags", [])}
        leaking_resources["ebs_volumes"].append({
            "id": volume["VolumeId"],
            "size_gb": volume["Size"],
            "type": volume["VolumeType"],
            "tags": tags
        })

    return leaking_resources

def write_json_report(data):
    """Section 4.2: Saare leaking resources ki report JSON file mein save karta hai."""
    report_data = {
        "scan_timestamp": str(datetime.now(timezone.utc)),
        "summary": {
            "total_leaking_ec2_instances": len(data["ec2_instances"]),
            "total_orphaned_ebs_volumes": len(data["ebs_volumes"])
        },
        "detected_resources": data
    }
    
    # Root directory mein report file banana
    report_path = "cost_leaks_report.json"
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=4)
    print(f"📝 Report successfully generated and saved to: {report_path}")

def clean_resources(data):
    """Section 4.3: Auto-remediation script jo instances ko terminate aur volumes ko delete karti hai."""
    ec2_client = get_boto3_client("ec2")

    # 1. EC2 Instances ko terminate karo
    if data["ec2_instances"]:
        instance_ids = [inst["id"] for inst in data["ec2_instances"]]
        print(f"🧹 Terminating EC2 Instances: {instance_ids}...")
        ec2_client.terminate_instances(InstanceIds=instance_ids)
        print("✅ EC2 Termination request sent successfully.")
    else:
        print("ℹ️ No active EC2 instances found to clean.")

    # 2. Orphaned EBS Volumes ko delete karo
    if data["ebs_volumes"]:
        for volume in data["ebs_volumes"]:
            print(f"🧹 Deleting Orphaned EBS Volume: {volume['id']}...")
            ec2_client.delete_volume(VolumeId=volume["id"])
        print("✅ All orphaned EBS volumes deleted successfully.")
    else:
        print("ℹ️ No orphaned EBS volumes found to clean.")

if __name__ == "__main__":
    print("🔍 [STEP 1] NimbusKart Cost Janitor Initiating Discovery...")
    found_resources = discover_leaking_resources()
    
    print("\n📝 [STEP 2] Generating Cost Leaks Audit Report...")
    write_json_report(found_resources)
    
    print("\n⚡ [STEP 3] Starting Auto-Remediation (Cleanup Lifecycle)...")
    clean_resources(found_resources)
    
    print("\n🎉 Janitor Process Finished Successfully! Cost Leaks Controlled.")