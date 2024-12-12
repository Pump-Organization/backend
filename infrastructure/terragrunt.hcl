locals {
    env = path_relative_to_include()
}

remote_state {
    backend = "s3"
    config = {
        bucket = "pump-state-${local.env}"
        region = "us-west-1"
        key    = "terraform.tfstate"
    }
}

inputs = {
    # eventing.tf
    event_bus_name = "pump-event-bus-${local.env}"
    notification_dlq_name = "pump-notification-dlq-${local.env}"
    notification_event_rule_name = "pump-notification-event-rule-${local.env}"
    notification_queue_name = "pump-notification-queue-${local.env}"

    # main.tf
    aws_account_id = "597088031564"
    terraform_state_bucket_name = "pump-state-${local.env}"

    # media.tf
    media_bucket_name = "pump-media-${local.env}"
}