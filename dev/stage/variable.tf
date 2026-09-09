variable "location" {
  description = "Location gcloud"
  type        = string
  default     = "EU"
}

variable "bucket" {
  description = "Raw NYC practise Bucket name"
  type = string
  default = "sumant_nyc311"
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "ee-india-se-data"
}

variable "file_path" {
  description = "Oauth key file"
  type        = string
  default     = "/Users/sumant/.ssh/ee-india-se-data-0f3e7b1c5d4f.json"
}