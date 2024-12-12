provider "aws" {
  region = "us-west-1"
}

terraform {
  backend "s3" {}
}

## REMOTE TF STATE

variable "aws_account_id" { type = string }
variable "terraform_state_bucket_name" { type = string }
resource "aws_s3_bucket_policy" "terraform_state_bucket_policy" {
  bucket = var.terraform_state_bucket_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "EnforcedTLS"
        Effect = "Deny"
        Principal = "*"
        Action = "s3:*"
        Resource = [
          "arn:aws:s3:::${var.terraform_state_bucket_name}",
          "arn:aws:s3:::${var.terraform_state_bucket_name}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      },
      {
        Sid = "RootAccess"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.aws_account_id}:root"
        }
        Action = "s3:*"
        Resource = [
          "arn:aws:s3:::${var.terraform_state_bucket_name}",
          "arn:aws:s3:::${var.terraform_state_bucket_name}/*"
        ]
      }
    ]
  })
}
