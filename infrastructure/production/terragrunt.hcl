include { path = find_in_parent_folders() }

terraform { source = ".." }

inputs = {
    aws_account_id = "084828603127"
}