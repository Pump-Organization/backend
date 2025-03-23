## EVENTS

variable "event_bus_name" { type = string }
resource "aws_cloudwatch_event_bus" "event_bus" {
  name = var.event_bus_name
}

################# Notifications Eventing ##########################

variable "notification_event_rule_name" { type = string }
resource "aws_cloudwatch_event_rule" "notification_event_rule" {
    name = var.notification_event_rule_name
    event_bus_name = aws_cloudwatch_event_bus.event_bus.name
    event_pattern = jsonencode({
        detail-type = [
            "FOLLOW-CREATED",
            "FOLLOW-DELETED",
            "INVITE-CREATED",
            "INVITE-DELETED",
            "LIKE-CREATED",
            "LIKE-DELETED",
            "COMMENT-CREATED",
            "COMMENT-DELETED",
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


############## Analytics Eventing ##########################

variable "analytics_event_rule_name" { type = string }
resource "aws_cloudwatch_event_rule" "analytics_event_rule" {
	name = var.analytics_event_rule_name
	event_bus_name = aws_cloudwatch_event_bus.event_bus.name
	event_pattern = jsonencode({
		detail-type = [
			"FOLLOW-CREATED",
			"FOLLOW-DELETED",
			"INVITE-CREATED",
			"INVITE-DELETED",
			"LIKE-CREATED",
			"LIKE-DELETED",
			"COMMENT-CREATED",
			"COMMENT-DELETED"
		]
	})
}

resource "aws_cloudwatch_event_target" "analytics_event_rule_target" {
	rule = aws_cloudwatch_event_rule.analytics_event_rule.name
	target_id = "SendToSQS"
	arn = aws_sqs_queue.analytics_queue.arn
	event_bus_name = aws_cloudwatch_event_bus.event_bus.name
}

variable "analytics_queue_name" { type = string }
resource "aws_sqs_queue" "analytics_queue" {
	name = var.analytics_queue_name
	redrive_policy = jsonencode({
		deadLetterTargetArn = aws_sqs_queue.analytics_dlq.arn
		maxReceiveCount = 3
	})
}

variable "analytics_dlq_name" { type = string }
resource "aws_sqs_queue" "analytics_dlq" {
	name = var.analytics_dlq_name
}

resource "aws_sqs_queue_redrive_allow_policy" "analytics_queue_redrive_allow_policy" {
	queue_url = aws_sqs_queue.analytics_queue.id

	redrive_allow_policy = jsonencode({
		redrivePermission = "byQueue"
		sourceQueueArns = [aws_sqs_queue.analytics_queue.arn]
	})
}

resource "aws_sqs_queue_policy" "analytics_queue_policy" {
  queue_url = aws_sqs_queue.analytics_queue.id

  policy = jsonencode({
	Version = "2012-10-17",
	Statement = [
	  {
		Effect = "Allow",
		Principal = {
		  Service = "events.amazonaws.com"
		},
		Action = "sqs:SendMessage",
		Resource = aws_sqs_queue.analytics_queue.arn
	  }
	]
  })
}


########### SNS TOPIC for push notifications ##########################

variable "apns_cert" {
  description = "APNs Certificate"
  type        = string
  sensitive   = true
}

variable "apns_key" {
  description = "APNs Private Key"
  type        = string
  sensitive   = true
}

resource "aws_sns_platform_application" "pump_apns" {
  name                = "PumpAPNs"
  platform           = "APNS"
  platform_credential = var.apns_key
  platform_principal = var.apns_cert
  event_delivery_failure_topic_arn = aws_sns_topic.sns_failure_topic.arn
}

resource "aws_sns_topic" "sns_failure_topic" {
  name = "sns-failure-notifications"
}
