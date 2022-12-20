# create VPC for Cluster
resource "aws_vpc" "EKS-Event-VPC" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "EKS-Event-VPC"
  }
}



