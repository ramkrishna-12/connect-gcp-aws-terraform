
variable "project_id" {
  description = "Google Cloud project identifier."
  type        = string

  validation {
    condition     = length(trimspace(var.project_id)) > 0
    error_message = "project_id must not be empty."
  }
}

variable "region" {
  description = "Google Cloud region used for the staging bucket."
  type        = string
  default     = "asia-south1"
}

variable "bucket_name_suffix" {
  description = "Optional suffix to make the globally unique bucket name explicit."
  type        = string
  default     = "d0-raw-landing"
}

variable "ingestion_service_account" {
  description = "Service account used by the ingestion process."
  type        = string

  validation {
    condition     = can(regex("^[^@\\s]+@[^@\\s]+\\.iam\\.gserviceaccount\\.com$", var.ingestion_service_account))
    error_message = "ingestion_service_account must be a Google service account email."
  }
}

variable "analytics_group_email" {
  description = "Google Group that receives the example APAC row-level policy."
  type        = string

  validation {
    condition = can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", var.analytics_group_email))
    error_message = "analytics_group_email must be a valid group email."
  }
}

variable "environment" {
  description = "Deployment environment label."
  type        = string
  default     = "staging"
}
