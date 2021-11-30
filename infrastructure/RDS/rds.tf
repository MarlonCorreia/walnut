resource "random_string" "password" {
  length  = 16
  special = false
}

resource "aws_db_subnet_group" "this" {
  name = "${var.project}-${terraform.workspace}-db-subnet-group"

  subnet_ids = var.subnet_ids
  tags = {
    Project     = var.project
    Name        = "DB Subnet Group"
    Environment = terraform.workspace
  }
}

resource "aws_db_instance" "this" {
  identifier = "${var.project}-${terraform.workspace}"

  engine         = "postgres"
  engine_version = "12.5"

  instance_class              = var.instance_class
  allocated_storage           = var.allocated_storage
  storage_type                = "gp2"
  storage_encrypted           = var.storage_encrypted
  allow_major_version_upgrade = false
  apply_immediately           = true
  multi_az                    = false

  name     = var.db_name
  username = var.username
  port     = "5432"
  password = random_string.password.result
  lifecycle {
    ignore_changes = [password]
  }

  maintenance_window        = "Mon:00:00-Mon:02:00"
  backup_window             = "02:00-03:00"
  backup_retention_period   = var.backup_retention_period
  deletion_protection       = var.delete_protection
  final_snapshot_identifier = "${var.project}-${terraform.workspace}-final-snapshot"
  skip_final_snapshot       = true

  vpc_security_group_ids = var.vpc_security_group_ids
  db_subnet_group_name   = aws_db_subnet_group.this.name
  publicly_accessible    = false

  copy_tags_to_snapshot = true
  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend: ${terraform.workspace}"
    }
  )
}
