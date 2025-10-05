# CI Pipeline

The repository contains a unified GitHub Actions pipeline at `.github/workflows/ci.yml` that:
- Runs backend pytest with Redis service
- Runs frontend unit tests (Jest)
- Runs Cypress end-to-end tests (via cypress-io/github-action)
- Builds and publishes Docker images to GHCR (requires `secrets.GHCR_TOKEN`)

To enable Docker publishing:
1. Create a GitHub Personal Access Token with `write:packages` and `delete:packages` scopes.
2. Add it to your repository secrets as `GHCR_TOKEN`.
