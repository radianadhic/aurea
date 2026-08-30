# Terraform - Infrastructure as Code for MDM Bank XYZ
# Provisions: AWS EKS, RDS, ElastiCache, MSK, S3, etc.

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
  backend "s3" {
    bucket = "mdm-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-southeast-3"
    dynamodb_table = "mdm-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "ap-southeast-3"  # Jakarta
  default_tags {
    tags = {
      Project     = "MDM-Bank-XYZ"
      Environment = "production"
      ManagedBy   = "Terraform"
      Owner       = "mdm-team@bankxyz.co.id"
    }
  }
}

# ============================================================
# VARIABLES
# ============================================================
variable "cluster_name" {
  default = "mdm-prod-eks"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "db_password" {
  sensitive = true
}

# ============================================================
# NETWORKING
# ============================================================
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "mdm-vpc"
  cidr = var.vpc_cidr

  azs             = ["ap-southeast-3a", "ap-southeast-3b", "ap-southeast-3c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
  database_subnets = ["10.0.20.0/24", "10.0.21.0/24", "10.0.22.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = false
  one_nat_gateway_per_az = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}

# ============================================================
# EKS CLUSTER
# ============================================================
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.30"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  # Managed node groups
  eks_managed_node_groups = {
    # General workload nodes
    general = {
      desired_size = 6
      min_size     = 3
      max_size     = 30

      instance_types = ["m6i.xlarge", "m6a.xlarge"]
      capacity_type  = "ON_DEMAND"

      labels = {
        workload = "general"
      }
    }

    # CPU-optimized for matching/ML
    compute-optimized = {
      desired_size = 3
      min_size     = 2
      max_size     = 15

      instance_types = ["c6i.2xlarge", "c6a.2xlarge"]
      capacity_type  = "ON_DEMAND"

      labels = {
        workload = "compute"
      }

      taints = [{
        key    = "workload"
        value  = "compute"
        effect = "NO_SCHEDULE"
      }]
    }

    # Memory-optimized for ClickHouse, ES
    memory-optimized = {
      desired_size = 3
      min_size     = 2
      max_size     = 10

      instance_types = ["r6i.2xlarge"]
      capacity_type  = "ON_DEMAND"

      labels = {
        workload = "memory"
      }
    }
  }

  # Fargate profiles for specific workloads
  fargate_profiles = {
    kube_system = {
      name = "kube-system"
      selectors = [
        { namespace = "kube-system" }
      ]
    }
  }

  tags = {
    Environment = "production"
  }
}

# ============================================================
# RDS POSTGRESQL (Patroni-compatible)
# ============================================================
resource "aws_db_subnet_group" "main" {
  name       = "mdm-db-subnet-group"
  subnet_ids = module.vpc.database_subnets
}

resource "aws_rds_cluster" "postgresql" {
  cluster_identifier     = "mdm-postgres-cluster"
  engine                 = "aurora-postgresql"
  engine_version         = "16.2"
  database_name          = "mdm"
  master_username        = "mdm_admin"
  master_password        = var.db_password
  port                   = 5432
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  storage_encrypted = true
  kms_key_id        = aws_kms_key.main.arn

  backup_retention_period = 30
  preferred_backup_window = "03:00-04:00"
  preferred_maintenance_window = "Mon:00:00-Mon:03:00"

  deletion_protection = true

  enabled_cloudwatch_logs_exports = ["postgresql"]

  serverlessv2_scaling_configuration {
    min_capacity = 2
    max_capacity = 64
  }

  tags = {
    Component = "database"
  }
}

# Writer instance
resource "aws_rds_cluster_instance" "writer" {
  identifier         = "mdm-postgres-writer"
  cluster_identifier = aws_rds_cluster.postgresql.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.postgresql.engine
  engine_version     = aws_rds_cluster.postgresql.engine_version
}

# ============================================================
# ELASTICACHE (Valkey/Redis)
# ============================================================
resource "aws_elasticache_replication_group" "valkey" {
  replication_group_id       = "mdm-valkey"
  description                = "MDM Valkey cluster for caching"
  engine                     = "valkey"
  engine_version             = "7.2"
  node_type                  = "cache.r6g.large"
  num_cache_clusters         = 3
  port                       = 6379
  parameter_group_name       = "default.valkey7"
  subnet_group_name          = aws_elasticache_subnet_group.main.name
  security_group_ids         = [aws_security_group.valkey.id]
  automatic_failover_enabled = true
  multi_az_enabled           = true

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.db_password

  snapshot_retention_limit = 5
  snapshot_window          = "05:00-07:00"
}

# ============================================================
# MSK (Managed Kafka)
# ============================================================
resource "aws_msk_cluster" "kafka" {
  cluster_name           = "mdm-kafka-cluster"
  kafka_version          = "3.7"
  number_of_broker_nodes = 5

  broker_node_group_info {
    instance_type   = "kafka.m5.large"
    client_subnets  = module.vpc.private_subnets
    security_groups = [aws_security_group.kafka.id]

    storage_info {
      ebs_storage_info {
        volume_size = 1000
      }
    }
  }

  encryption_info {
    encryption_at_rest_kms_key_id = aws_kms_key.main.arn
    encryption_in_transit {
      client_broker = "TLS"
      in_cluster    = true
    }
  }

  configuration_info {
    arn      = aws_msk_configuration.kafka.arn
    revision = aws_msk_configuration.kafka.latest_revision
  }

  logging_info {
    broker_logs {
      cloudwatch_logs {
        enabled   = true
        log_group = aws_cloudwatch_log_group.kafka.name
      }
    }
  }
}

# ============================================================
# S3 BUCKETS
# ============================================================
resource "aws_s3_bucket" "backups" {
  bucket = "mdm-backups-${var.cluster_name}"
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}

# ============================================================
# KMS KEY
# ============================================================
resource "aws_kms_key" "main" {
  description             = "MDM Bank XYZ encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

# ============================================================
# SECURITY GROUPS
# ============================================================
resource "aws_security_group" "rds" {
  name   = "mdm-rds-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
}

resource "aws_security_group" "valkey" {
  name   = "mdm-valkey-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
}

resource "aws_security_group" "kafka" {
  name   = "mdm-kafka-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
}

resource "aws_elasticache_subnet_group" "main" {
  name       = "mdm-valkey-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_msk_configuration" "kafka" {
  name              = "mdm-kafka-config"
  kafka_versions    = ["3.7"]
  server_properties = <<PROPERTIES
    auto.create.topics.enable = true
    default.replication.factor = 3
    min.insync.replicas = 2
    num.partitions = 12
    log.retention.hours = 168
    log.segment.bytes = 1073741824
    compression.type = producer
  PROPERTIES
}

resource "aws_cloudwatch_log_group" "kafka" {
  name              = "/aws/msk/mdm-kafka"
  retention_in_days = 30
}

# ============================================================
# OUTPUTS
# ============================================================
output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "rds_endpoint" {
  value = aws_rds_cluster.postgresql.endpoint
}

output "valkey_endpoint" {
  value = aws_elasticache_replication_group.valkey.primary_endpoint
}

output "kafka_bootstrap_servers" {
  value = aws_msk_cluster.kafka.bootstrap_brokers_tls
}
