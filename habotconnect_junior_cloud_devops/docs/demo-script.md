# Project Interview Demo Script

## Demo 1: Healthy commit

1. Open the repository.
2. Show the Terraform folder.
3. Show the GitHub Actions workflow.
4. Show the Django serializer and DCYN library.
5. Run the unit tests.
6. Show that the security gate is green.
7. Explain that the artifact job depends on the security gate.

## Demo 2: Formatting failure

1. Intentionally make a Terraform formatting violation.
2. Push the change.
3. Show `terraform fmt -check` failing.
4. Explain that the gate job fails.
5. Show that the artifact job does not execute.

## Demo 3: Hardcoded secret failure

Do not use a real credential. Use a clearly fake test token such as a non-production value in a temporary branch.

1. Add the fake secret to a temporary test file.
2. Push the change.
3. Show Gitleaks detecting the secret pattern.
4. Explain that the workflow fails closed.
5. Remove the test secret and rotate any credential if a real secret was ever exposed.

## Demo 4: Django validation

Show one valid payload and one invalid payload:

- valid `Yes` / `No` values;
- invalid value such as `Maybe`;
- missing parental consent;
- excessive notes length.

Explain that the serializer rejects invalid input before it reaches the data layer.

## Interview explanation

The strongest sentence to use:

> “I designed the deployment path so security is a prerequisite, not a warning. If formatting, secret scanning, infrastructure security, or schema tests fail, there is no successful gate and therefore no deployable artifact.”
