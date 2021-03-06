has_private_subnets                    = false
vpc_cidr_block                         = "10.1.0.0/16"
subnet_public_A_cidr_block             = "10.1.0.0/24"
subnet_public_B_cidr_block             = "10.1.2.0/24"
alb_certificate_arn                    = ""
ecs_log_retention                      = 180
ecs_instance_type                      = "t3.micro"
ecs_key_name                           = "walnut-keypair"
ecs_max_instances                      = 1
ecs_min_instances                      = 1
ecs_desired_instances                  = 1
ecs_desired_service_tasks              = 1
ecs_deployment_maximum_percent         = 200
ecs_deployment_minimum_healthy_percent = 100
rds_backup_retention_period            = 1
rds_username                           = "root"
rds_db_name                            = "walnut"
rds_delete_protection                  = false
rds_instance_class                     = "db.t2.micro"
rds_allocated_storage                  = 5
rds_storage_encrypted                  = false
redis_engine_version                   = "5.0.6"
redis_node_type                        = "cache.t3.micro"
redis_parameter_group_name             = "default.redis5.0"
ecs_celery_worker_desired_service_tasks              = 1
ecs_celery_worker_deployment_maximum_percent         = 100
ecs_celery_worker_deployment_minimum_healthy_percent = 0
