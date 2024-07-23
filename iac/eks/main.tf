module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.20.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  cluster_endpoint_private_access = false
  cluster_endpoint_public_access  = true

  enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    node_group = {
      instance_types = var.instance_types
      min_size       = var.min_capacity
      max_size       = var.max_capacity
      desired_size   = var.desired_capacity
    }
  }

  node_security_group_additional_rules = {
    ingress_internal_all = {
      description                   = "internal all"
      protocol                      = "-1"
      from_port                     = 0
      to_port                       = 0
      type                          = "ingress"
      source_node_security_group = true
    }
  }
}