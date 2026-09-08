terraform {
  required_providers {
    snowflake = {
      source = "snowflakedb/snowflake"
    }
  }
}

locals {
  organization_name = "GUSDATD"
  account_name      = "DAB70621"
  private_key_path  = "~/.ssh/snowflake_rsa_key.p8"
}

provider "snowflake" {
    organization_name = local.organization_name
    account_name      = local.account_name
    user              = "sumant.dey"
    role              = "SE_DE_PARTICIPANT"
    authenticator     = "SNOWFLAKE_JWT"
    private_key       = file(local.private_key_path)
}


# resource "snowflake_warehouse" "SNOWFLAKE_LEARNING_WH" {
#   name           = "SNOWFLAKE_LEARNING_WH"
#   warehouse_size = "X-SMALL"
#   auto_suspend   = 60
#   initially_suspended = true
# }


# resource "snowflake_database" "DE_CROSS_SKILLING_NYC_311" {
#   name    = "DE_CROSS_SKILLING_NYC_311"
#   comment = "Database storing raw, unprocessed source system data."
# }

# Define the RAW schema within that database
resource "snowflake_schema" "SUMANT_DEY_RAW_CURATED" {
  database            = "DE_CROSS_SKILLING_NYC_311"
  name                = "SUMANT_DEY_RAW/CURATED"
  comment             = "Schema for raw ingest layers managed by tools like Fivetran/Airbyte."
}

