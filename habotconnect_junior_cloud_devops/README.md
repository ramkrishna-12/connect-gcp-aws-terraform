# HabotConnect Junior Cloud & DevOps Engineer Hiring Project

**Project:** Secure staging provisioning, fail-closed CI/CD, and schema/DCYN validation

> Contact information is intentionally not embedded because it was not supplied with the project brief. Add the candidate's actual contact information to the top of the submitted code and answer documents before submission.

## Scope

This repository implements the three explicit tasks in the hiring project:

1. Terraform secure staging provisioning for a Google Cloud Storage raw landing bucket and a Google BigQuery staged/enforced dataset, including IAM conditions and BigQuery row-level security.
2. A fail-closed GitHub Actions gate for formatting, linting, Terraform validation, infrastructure security scanning, and hardcoded-secret detection.
3. A Django REST Framework serializer plus a deterministic Yes/No (DCYN) validation library for a student onboarding payload.

The project brief does not provide the exact student JSON schema, field limits, or production identities. Those details are therefore made explicit as documented engineering assumptions rather than silently invented.
<!-- 
## Repository layout

```text
.
├── .github/workflows/security-gate.yml
├── data/schema-mapping.xlsx
├── app/
│   ├── __init__.py
│   ├── dcyn.py
│   └── serializers.py
├── docs/
│   ├── architecture.md
│   ├── assumptions.md
│   └── demo-script.md
├── presentation/habotconnect_project.pptx
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── terraform.tfvars.example
├── tests/
│   └── test_serializer.py
└── README.md
```

## Architecture

```text
Student onboarding application
            |
            v
      CI/CD Build Gate
  +-----------------------+
  | format + lint         |
  | secret scan           |
  | Terraform validation  |
  | infrastructure scan  |
  +-----------+-----------+
              |
       PASS / FAIL-CLOSED
              |
              v
       GCP staging layer
   +-----------------------+
   | GCS D0 Raw Landing    |
   |         |             |
   |         v             |
   | Pub/Sub / ingestion   |
   |         |             |
   |         v             |
   | BigQuery D1            |
   | Staged/Enforced       |
   | + Row-Level Security |
   +-----------------------+
              ^
              |
      Django serializer
      + DCYN validation
```

## Task 1: Terraform

The Terraform configuration creates:

- A private Google Cloud Storage bucket named from the project identifier.
- Uniform bucket-level access.
- Public access prevention.
- Object versioning.
- A lifecycle rule for noncurrent object versions.
- A conditional object-creation grant restricted to the `raw/` object prefix.
- A private BigQuery dataset.
- A `student_onboarding` BigQuery table required to attach a row-level access policy.
- BigQuery row-level security for the configured analytics group.
- Least-privilege dataset/table permissions for the ingestion service account.

The row-level policy uses `region = 'APAC'` as a demonstration boundary. The assignment requires RLS but does not define the production business predicate, so this is explicitly documented as a replaceable staging assumption.

## Task 2: Fail-Closed CI/CD

The workflow runs on pushes and pull requests.

A deployment artifact is created only if the `security_gate` job succeeds. The security gate includes:

- Terraform formatting check.
- Terraform initialization and validation.
- TFLint.
- Checkov infrastructure security scanning.
- Ruff linting.
- Ruff formatting check.
- Gitleaks secret scanning.
- Unit tests for the Django validation library.

If any gate fails, the workflow stops and the build artifact job is skipped. This is the practical fail-closed implementation: there is no successful gate, therefore there is no deployable artifact.

## Task 3: Schema and DCYN

The example payload is deterministic and deliberately conservative:

- Names: required, 1-100 characters.
- Email: required, valid email format, maximum 254 characters.
- Date of birth: required, valid ISO date.
- Region: required and restricted to the documented staging regions.
- Four Yes/No fields are converted through the DCYN library.
- Consent must be `Yes` before the payload is accepted.
- Unknown fields are rejected.

See `docs/assumptions.md` and `data/schema-mapping.xlsx`.

## Local checks

### Python

```bash
python -m pip install -r requirements.txt
ruff check .
ruff format --check .
python -m unittest discover -s tests -v
```

### Terraform

```bash
cd terraform
terraform fmt -check -recursive
terraform init
terraform validate
tflint --init
tflint
```

A real Google Cloud project and authenticated credentials are required for `terraform plan` and `terraform apply`.

## Security notes

- No credentials are committed.
- Terraform uses variables for identities.
- The example variable file contains no real secrets.
- The GitHub workflow does not print secret values.
- GCS uniform bucket-level access and public access prevention are enabled.
- The ingestion principal receives object-creation access only within the raw prefix.
- BigQuery access is separated between ingestion and analytics use cases.
- Row-level security is applied at the BigQuery table boundary.

## Presentation

The PowerPoint deck contains 12 slides and covers:

1. Problem statement.
2. Requirements.
3. Architecture.
4. Terraform design.
5. Storage security.
6. BigQuery and row-level security.
7. CI/CD fail-closed gate.
8. Secret detection.
9. DCYN schema mapping.
10. Django validation.
11. Failure demonstration.
12. Final controls and submission checklist.

## Important before submission

The hiring brief requires full name and contact information at the top of answer/code files and asks for a maximum 15-slide presentation. The brief also requires any spreadsheet mapping sheets to have Wrap Text enabled and to use full forms only.

Before submitting:

1. Add actual contact information to the marked metadata areas.
2. Replace staging identity variables with the identities supplied by the company, if any.
3. Review the documented schema assumptions against any payload supplied later.
4. Run the local tests.
5. Run the GitHub workflow with one intentionally invalid commit to demonstrate the fail-closed behavior.
6. Submit through the Google Form specified in the hiring brief. -->
