## DYNAMODB

variable "notification_dynamodb_table_name" { type = string }
resource "aws_dynamodb_table" "notification_dynamodb_table" {
    name = var.notification_dynamodb_table_name
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "PK"
    range_key = "SK"

    attribute {
        name = "PK"
        type = "S"
    }

    attribute {
        name = "SK"
        type = "S"
    }

    attribute {
        name = "viewed"
        type = "N"
    }

    global_secondary_index {
        name = "ViewStatusIndex"
        hash_key = "PK"
        range_key = "viewed"
        projection_type = "ALL"
    }
}