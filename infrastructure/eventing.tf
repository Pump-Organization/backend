## EVENTS

variable "event_bus_name" { type = string }
resource "aws_cloudwatch_event_bus" "event_bus" {
  name = var.event_bus_name
}

variable "notification_event_rule_name" { type = string }
resource "aws_cloudwatch_event_rule" "notification_event_rule" {
    name = var.notification_event_rule_name
    event_bus_name = aws_cloudwatch_event_bus.event_bus.name
    event_pattern = jsonencode({
        detail-type = [
            "FOLLOW-CREATED",
            "INVITE-CREATED",
        ]
    })
}

resource "aws_cloudwatch_event_target" "notification_event_rule_target" {
    rule = aws_cloudwatch_event_rule.notification_event_rule.name
    target_id = "SendToSQS"
    arn = aws_sqs_queue.notification_queue.arn
    event_bus_name = aws_cloudwatch_event_bus.event_bus.name
}

variable "notification_queue_name" { type = string }
resource "aws_sqs_queue" "notification_queue" {
    name = var.notification_queue_name
    redrive_policy = jsonencode({
        deadLetterTargetArn = aws_sqs_queue.notification_dlq.arn
        maxReceiveCount = 3
    })
}

variable "notification_dlq_name" { type = string }
resource "aws_sqs_queue" "notification_dlq" {
    name = var.notification_dlq_name
}

resource "aws_sqs_queue_redrive_allow_policy" "notification_queue_redrive_allow_policy" {
    queue_url = aws_sqs_queue.notification_queue.id

    redrive_allow_policy = jsonencode({
        redrivePermission = "byQueue"
        sourceQueueArns = [aws_sqs_queue.notification_queue.arn]
    })
}

resource "aws_sqs_queue_policy" "notification_queue_policy" {
  queue_url = aws_sqs_queue.notification_queue.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "events.amazonaws.com"
        },
        Action = "sqs:SendMessage",
        Resource = aws_sqs_queue.notification_queue.arn
      }
    ]
  })
}
