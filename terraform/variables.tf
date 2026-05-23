variable "aws_region" {
  type        = string
  description = "AWS region for local deployment"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "staging"
}
variable "project_name" {
  type    = string
  default = "NimbusKart"
}

variable "owner" {
  type    = string
  default = "numan-khan"
}