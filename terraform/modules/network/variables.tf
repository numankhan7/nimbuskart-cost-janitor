variable "vpc_cidr" { default = "10.20.0.0/16" }
variable "public_subnet_1_cidr" { default = "10.20.1.0/24" }
variable "public_subnet_2_cidr" { default = "10.20.2.0/24" }
variable "aws_region" {}
variable "environment" {}
variable "project_name" {}
variable "owner" {}