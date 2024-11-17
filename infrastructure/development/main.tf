terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-1"
}

resource "aws_s3_bucket" "pump-media-development" {
  bucket = "pump-media-development"
}

resource "aws_s3_bucket_public_access_block" "pump_media_development" {
  bucket = aws_s3_bucket.pump-media-development.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "pump_media_s3_policy" {
  bucket = aws_s3_bucket.pump-media-development.bucket

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "s3:GetObject"
        Resource = "arn:aws:s3:::pump-media-development/images/*"
      }
    ]
  })
}
