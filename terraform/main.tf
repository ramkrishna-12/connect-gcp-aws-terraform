
locals {
  common_labels = {
    environment = var.environment
    managed_by  = "terraform"
    project     = "habotconnect-hiring"
  }

  raw_bucket_name = "${var.project_id}-${var.bucket_name_suffix}"

  student_table_schema = jsonencode([
    {
      name        = "student_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Unique student identifier."
    },
    {
      name = "first_name"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "last_name"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "email"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "date_of_birth"
      type = "DATE"
      mode = "REQUIRED"
    },
    {
      name = "region"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "has_learning_difficulty"
      type = "BOOL"
      mode = "REQUIRED"
    },
    {
      name = "receives_learning_support"
      type = "BOOL"
      mode = "REQUIRED"
    },
    {
      name = "needs_learning_support_assistant"
      type = "BOOL"
      mode = "REQUIRED"
    },
    {
      name = "parental_consent"
      type = "BOOL"
      mode = "REQUIRED"
    },
    {
      name = "notes"
      type = "STRING"
      mode = "NULLABLE"
    }
  ])
}

resource "google_storage_bucket" "raw_landing" {
  name                        = local.raw_bucket_name
  location                    = var.region
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      num_newer_versions = 5
    }

    action {
      type = "Delete"
    }
  }

  labels = local.common_labels
}

resource "google_storage_bucket_iam_member" "ingestion_raw_object_creator" {
  bucket = google_storage_bucket.raw_landing.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${var.ingestion_service_account}"

  condition {
    title       = "RawPrefixOnly"
    description = "Allow object creation only beneath the raw prefix."
    expression  = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.raw_landing.name}/objects/raw/')"
  }
}

resource "google_bigquery_dataset" "staged_enforced" {
  dataset_id                 = "d1_staged_enforced"
  friendly_name              = "D1 Staged Enforced"
  description                = "Validated staging dataset for student onboarding analytics."
  location                   = "US"
  delete_contents_on_destroy = false

  labels = local.common_labels
}

resource "google_bigquery_dataset_iam_member" "ingestion_data_editor" {
  dataset_id = google_bigquery_dataset.staged_enforced.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.ingestion_service_account}"
}

resource "google_bigquery_dataset_iam_member" "analytics_data_viewer" {
  dataset_id = google_bigquery_dataset.staged_enforced.dataset_id
  role       = "roles/bigquery.dataViewer"
  member     = "group:${var.analytics_group_email}"
}

resource "google_bigquery_table" "student_onboarding" {
  dataset_id          = google_bigquery_dataset.staged_enforced.dataset_id
  table_id            = "student_onboarding"
  schema              = local.student_table_schema
  deletion_protection = true

  labels = local.common_labels
}

resource "google_bigquery_table_iam_member" "analytics_table_viewer" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_onboarding.table_id
  role       = "roles/bigquery.dataViewer"
  member     = "group:${var.analytics_group_email}"
}

resource "google_bigquery_row_access_policy" "analytics_apac" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_onboarding.table_id
  policy_id  = "analytics_apac"

  filter_predicate = "region = 'APAC'"

  grantees = [
    "group:${var.analytics_group_email}"
  ]
}
