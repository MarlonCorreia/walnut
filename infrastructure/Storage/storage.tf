resource "aws_s3_bucket" "bucket" {
  bucket = "${var.project}-backend-${terraform.workspace}"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend: ${terraform.workspace}"
    }
  )
}
