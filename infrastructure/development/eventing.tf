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

## EVENTS

variable "event_bus_name" { type = string }
resource "aws_cloudwatch_event_bus" "event_bus" {
  name = var.event_bus_name
}

resource "aws_cloudwatch_event_rule" "notification_event_rule" {
    name = "notification-event-rule"
    event_bus_name = aws_cloudwatch_event_bus.event_bus.name
    event_pattern = jsonencode({
        detail-type = [
            "FOLLOW",
            "INVITE"
        ]
    })
}

resource "aws_cloudwatch_event_target" "notification_event_rule_target" {
    rule = aws_cloudwatch_event_rule.notification_event_rule.name
    target_id = "SendToSQS"
    arn = aws_sqs_queue.notification_queue.arn
    event_bus_name = var.event_bus_name
}

variable "notification_queue_name" { type = string }
resource "aws_sqs_queue" "notification_queue" {
    name = var.notification_queue_name
    redrive_policy = jsonencode({
        deadLetterTargetArn = aws_sqs_queue.notification_event_dlq.arn
        maxReceiveCount = 3
    })
}

variable "notification_event_dlq_name" { type = string }
resource "aws_sqs_queue" "notification_event_dlq" {
    name = var.notification_event_dlq_name
}

resource "aws_sqs_queue_redrive_allow_policy" "notification_queue_redrive_allow_policy" {
    queue_url = aws_sqs_queue.notification_queue.id

    redrive_allow_policy = jsonencode({
        redrivePermission = "byQueue"
        sourceQueueArns = [aws_sqs_queue.notification_queue.arn]
    })
}
