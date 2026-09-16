variable organisation_name {
  type        = string
  default     = "GUSDATD"
  description = "description"
}

variable account_name {
  type        = string
  default     = "DAB70621"
  description = "description"
}

variable snowflake_user {
  type        = string
  default     = "sumant.dey"
  description = "description"
}

variable snowflake_role {
  type        = string
  default     = "SE_DE_PARTICIPANT"
  description = "description"
}

variable authenticator {
  type        = string
  default     = "SNOWFLAKE_JWT"
  description = "description"
}

variable private_key_path {
  type        = string
  default     = "~/.ssh/snowflake_rsa_key.p8"
  description = "description"
}

variable gcs_integration_name {
  type        = string
  default     = "GCS_NYC311_INTEGRATION"
  description = "description"
}

variable database_name {
  type        = string
  default     = "DE_CROSS_SKILLING_NYC_311"
  description = "description"
}

variable schema_name {
  type        = string
  default     = "SUMANT_DEY_RAW"
  description = "description"
}
variable schema_name_curated {
  type        = string
  default     = "SUMANT_DEY_CURATED"
  description = "description"
}
variable schema_name_consume {
  type        = string
  default     = "SUMANT_DEY_CONSUME"
  description = "description"
}

variable table_name{
  type        = string
  default     = "SUMANT_DEY_RAW_NYC_311_DATA_TABLE"
  description = "description"
}

variable csv_file_format_name {
  type        = string
  default     = "DE_CROSS_SKILLING_CSV_FILE_FORMAT"
  description = "description"
}

variable stage_name {
  type        = string
  default     = "SUMANT_GCS_BUCKET_STAGE"
  description = "description"
}

variable gcs_bucket_url {
  type        = string
  default     = "gcs://sumant_nyc311/"
  description = "description"
}

variable notification_integration_name {
  type        = string
  default     = "gcs_nyc311_notification_int"
  description = "description"
}