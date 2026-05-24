# NimbusKart Cost Janitor

## ## Overview
NimbusKart Cost Janitor is an automated FinOps orchestration tool designed to discover and eliminate orphaned cloud infrastructure assets dynamically. Operating via Python boto3 and built on top of LocalStack local cloud architectures, it audits active compute hosts and loose storage disks to mitigate monthly cost leaks.

## ## How to run locally
```bash
# 1. Clone the repository
git clone [https://github.com/numan-khan/nimbuskart-cost-janitor.git](https://github.com/numan-khan/nimbuskart-cost-janitor.git)
cd nimbuskart-cost-janitor

# 2. Start LocalStack Background Core
docker run --rm -p 4566:4566 --name localstack -e "SERVICES=ec2" localstack/localstack:3.0

# 3. Apply Infrastructure State via Terraform
cd terraform
terraform init
terraform apply -auto-approve
cd ..

# 4. Trigger Janitor Framework Run
pip install -r janitor/requirements.txt
python janitor/cost_janitor.py

## Architecture
Plaintext
┌─────────────────┐       Deploys Mock      ┌────────────────┐
│   Terraform     ├────────────────────────►│   LocalStack   │
│ (Infrastructure)│                         │  (Fake Cloud)  │
└─────────────────┘                         └───────┬────────┘
                                                    │ Scans &
                                                    │ Cleans
                                                    ▼
                                            ┌────────────────┐
                                            │ Python Janitor │
                                            └────────────────┘
## Decisions & deviations
S3 Deletion Loop Deviation: Replaced S3 automation with local direct validation mocks to prevent internal community Docker engine API validation deadlocks.

Granular AWS Core Isolations: Bypassed AWS network gateways logic inside standard main.tf configs to keep execution loops under 15 seconds.

## Trade-offs
With one more week, I would introduce a distributed transactional lock management layer (using DynamoDB state tracking entries) to safely scale execution runtimes concurrently without structural race conditions.

## AI usage disclosure
Utilized LLM interfaces to target Python 3.14 runtime deprecation warning messages and scaffold infrastructure definitions swiftly. Complete execution workflows and unit metrics were manually tuned.
