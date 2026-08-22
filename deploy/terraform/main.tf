
terraform {
  required_version = ">= 1.5.0"
}
variable "environment" { type = string default = "prod" }
variable "replicas" { type = number default = 3 }
output "topospace_environment" { value = var.environment }
output "recommended_replicas" { value = var.replicas }

# Cloud-provider resources are intentionally left to deployment modules.
# This root module is the stable composition point for VPC/Kubernetes/DB/Redis/KMS modules.
