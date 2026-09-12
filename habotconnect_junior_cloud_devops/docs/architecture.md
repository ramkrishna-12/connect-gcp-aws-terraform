# Architecture and Engineering Logic

## 1. Request flow

1. A developer creates a commit.
2. GitHub Actions starts the security gate.
3. Formatting and lint checks run.
4. Gitleaks scans the repository for hardcoded secrets.
5. Terraform is formatted and validated.
6. TFLint checks Terraform quality.
7. Checkov scans infrastructure-as-code for security misconfiguration.
8. Django validation tests run.
9. Only a completely successful gate permits the artifact job to execute.

## 2. Data flow

```text
Application
   |
   | validated onboarding payload
   v
Django REST Framework serializer
   |
   | deterministic Yes/No conversion
   v
DCYN logic
   |
   v
Raw landing
Google Cloud Storage / D0 Raw Landing
   |
   v
Staged / enforced
Google BigQuery / D1 Staged/Enforced
   |
   +--> Row-Level Security
   |
   +--> Analytics consumers
```

## 3. Storage controls

The raw bucket uses uniform bucket-level access so object-level access control lists do not compete with bucket IAM. Public access prevention is enabled. The ingestion principal receives object creation permission only under the `raw/` prefix through an IAM condition.

## 4. BigQuery controls

The dataset is private. A student onboarding table provides the physical boundary needed for the row-level access policy. The analytics group receives a predicate-restricted view of the table.

## 5. Fail-closed principle

The pipeline deliberately has no deployment step that can bypass `security_gate`.

```text
security_gate
     |
     +-- failure --> workflow stops
     |
     +-- success --> build artifact
```

This is stronger than merely reporting security findings. A failure is an actual control-flow dependency.

## 6. Why the design is operationally useful

The controls are deterministic:

- formatting is machine-checked;
- linting is machine-checked;
- secrets are scanned automatically;
- infrastructure is security-scanned;
- schema validation is encoded as executable rules;
- deployment artifacts are dependent on the gate result.

The intent is to replace human memory with enforceable controls, matching the Poka-Yoke requirement in the hiring brief.
