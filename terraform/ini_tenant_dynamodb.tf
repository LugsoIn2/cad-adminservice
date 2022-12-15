resource "aws_dynamodb_table" "event_table" {
  name               = "event_table"
  billing_mode       = "PROVISIONED"
  read_capacity      = "30"
  write_capacity     = "30"
  hash_key           = "eventId"
  range_key          = "city"

  attribute {
    name = "eventId"
    type = "S"
  }

  attribute {
    name = "date"
    type = "N"
  }

  attribute {
    name = "city"
    type = "S"
  }

  ttl {
    enabled        = false
    attribute_name = "TimeToExist"
  }

  global_secondary_index {
    name               = "dateIndex"
    hash_key           = "city"
    range_key          = "date"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["dateString"]
  }

  tags = {
    Name        = "event_table_konstanz"
    Environment = "production"
  }

}
