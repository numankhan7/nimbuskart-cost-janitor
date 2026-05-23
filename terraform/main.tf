terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    ec2 = "http://localhost:4566"
    s3  = "http://localhost:4566"
  }
}
module "network" {
  source       = "./modules/network"
  aws_region   = var.aws_region
  environment  = var.environment
  project_name = var.project_name
  owner        = var.owner
}
# 1. Security Group for Web Tier
resource "aws_security_group" "web_sg" {
  name        = "${var.environment}-web-sg"
  description = "Allow inbound HTTP/HTTPS and SSH"
  vpc_id      = module.network.vpc_id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # NOTE: 0.0.0.0/0 on port 22 is a security risk. 
  # We are keeping it as per spec but will document this deviation in README!
  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-web-sg"
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

# 2. Two EC2 Instances tagged as Web Tier
resource "aws_instance" "web_server_1" {
  ami           = "ami-df5dbec3" # Mock AMI ID for LocalStack
  instance_type = "t3.micro"
  subnet_id     = module.network.public_subnet_ids[0]
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "${var.environment}-web-server-1"
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "web_server_2" {
  ami           = "ami-df5dbec3"
  instance_type = "t3.micro"
  subnet_id     = module.network.public_subnet_ids[1]
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "${var.environment}-web-server-2"
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

# 3. One Orphans EBS Volume (Intentionally Left Unattached for Part B)
resource "aws_ebs_volume" "orphaned_volume" {
  availability_zone = "${var.aws_region}a"
  size              = 10 # 10 GB
  type              = "gp3"

  tags = {
    Name        = "${var.environment}-orphaned-ebs"
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}