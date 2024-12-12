## MEDIA

variable "media_bucket_name" { type = string }
resource "aws_s3_bucket" "media_bucket" {
  bucket = var.media_bucket_name
}

resource "aws_s3_bucket_public_access_block" "media_bucket_public_access_block" {
  bucket = aws_s3_bucket.media_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "pump_media_s3_policy" {
  bucket = aws_s3_bucket.media_bucket.bucket

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "s3:GetObject"
        Resource = "arn:aws:s3:::${var.media_bucket_name}/images/*"
      }
    ]
  })
}
