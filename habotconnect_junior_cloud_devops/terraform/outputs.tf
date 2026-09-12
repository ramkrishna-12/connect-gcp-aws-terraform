
output "raw_landing_bucket_name" {
  description = "D0 Raw Landing Google Cloud Storage bucket."
  value       = google_storage_bucket.raw_landing.name
}

output "staged_dataset_id" {
  description = "D1 Staged/Enforced BigQuery dataset."
  value       = google_bigquery_dataset.staged_enforced.dataset_id
}

output "student_onboarding_table_id" {
  description = "BigQuery table protected by row-level security."
  value       = google_bigquery_table.student_onboarding.table_id
}
