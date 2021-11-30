output "this_elasticache_cluster_arn" {
  description = "The ARN of the ElastiCache Cluster"
  value       = aws_elasticache_cluster.this.arn
}

output "this_elasticache_cluster_id" {
  description = "The ElastiCache cluster ID"
  value       = aws_elasticache_cluster.this.id
}

output "this_elasticache_subnet_group_id" {
  description = "The elasticache subnet group name"
  value       = aws_elasticache_subnet_group.this.id
}

output "this_elasticache_subnet_group_arn" {
  description = "The ARN of the elasticache subnet group"
  value       = aws_elasticache_subnet_group.this.arn
}
