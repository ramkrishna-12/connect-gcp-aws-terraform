# Engineering Assumptions


The hiring brief explicitly requires three tasks but does not specify the complete student JSON schema, exact validation limits, production group identities, or the final row-level business predicate. The following assumptions make the implementation executable without pretending those missing details were provided.

## Student onboarding schema

| Field | Type | Required | Rule |
|---|---|---:|---|
| first_name | string | Yes | 1-100 characters |
| last_name | string | Yes | 1-100 characters |
| email | string | Yes | Valid email, maximum 254 characters |
| date_of_birth | date | Yes | ISO date |
| region | string | Yes | APAC, EMEA, or AMER |
| has_learning_difficulty | Yes/No | Yes | Converted to Boolean |
| receives_learning_support | Yes/No | Yes | Converted to Boolean |
| needs_learning_support_assistant | Yes/No | Yes | Converted to Boolean |
| parental_consent | Yes/No | Yes | Must be Yes |
| notes | string | No | Maximum 500 characters |

## DCYN behavior

The library accepts only the exact strings `Yes` and `No`, case-insensitively after surrounding whitespace is removed. Other values are rejected. The resulting value is a Python Boolean.

## BigQuery row-level security assumption

The assignment requires Row-Level Security but does not specify the real production business rule. The staging example grants the configured analytics group access to rows where `region = 'APAC'`.

This is intentionally isolated in Terraform so it can be replaced with the real business rule without changing the surrounding architecture.

## Identity assumptions

The following Terraform variables must be supplied by the operator:

- `project_id`
- `ingestion_service_account`
- `analytics_group_email`

No real identity or credential is embedded in source control.

## Scope boundary

The brief mentions App Engine, Pub/Sub, BigQuery streaming sinks, and Django/React deployment in its assessment context. The three explicit tasks only require the raw landing bucket, staged/enforced BigQuery dataset, pipeline gates, and Django validation. Therefore this implementation does not provision an unnecessary application runtime or pretend to implement an end-to-end streaming application that the task did not explicitly request.
