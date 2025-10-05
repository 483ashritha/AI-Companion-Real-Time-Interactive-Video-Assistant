## Final Submission v6

This archive is the final submission (v6) including security checklist and production notes.

![CI](https://img.shields.io/badge/ci-passing-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

# AI Companion Video Call & Streaming — Final Submission (Full Features)

This final package includes:
- FastAPI backend (Socket.IO signaling, Redis-backed room store and recordings metadata, JWT auth stub)
- Next.js frontend with Tailwind CSS, multiple pages, improved UI
- Client-side recording upload; server stores files and metadata in Redis
- Basic automated tests:
  - Backend: pytest tests for health, auth, recordings endpoints
  - Frontend: placeholder jest config and a simple smoke test
- Docker & docker-compose for easy local deployment
- `init_git.sh` helper to create a Git repo with commits ready for pushing

## How to run
See backend/ and frontend/ README files for step-by-step instructions.

## Notes
- For JWT auth demo, use credentials: username=demo, password=demo
- Redis is used for recordings metadata; Docker compose spins up Redis automatically.


## Security & Production Checklist

**Important:** This project is a demonstration and is *not* production-ready out of the box.
Before deploying to production, complete the following steps:

1. **Rotate secrets**: Replace `JWT_SECRET` with a strong random secret and store it in a secrets manager (GitHub Secrets / Vault).
2. **HTTPS / TLS**: Terminate TLS at a reverse proxy (NGINX, Cloud Load Balancer) — never expose the backend over plain HTTP publicly.
3. **TURN server**: Use a reliable TURN server (self-hosted or provider like Xirsys/Twilio) for NAT traversal.
4. **Authentication**: Replace the demo JWT stub with a proper user store (database) and hashed passwords (bcrypt) + refresh tokens.
5. **Rate limiting & CORS**: Harden CORS settings and add rate limiting / abuse protection on auth endpoints.
6. **Logging & Monitoring**: Configure centralized logs (ELK/CloudWatch) and health/metrics endpoints; consider Sentry for error monitoring.
7. **Secrets in CI**: Add `GHCR_TOKEN` to GitHub secrets for Docker publish; do not check secrets into source control.
8. **Storage**: Use managed object storage (S3) for recordings in production; secure bucket policies and lifecycle rules.
9. **Vulnerability scans**: Run `npm audit`, `pip-audit`, and container image scans before pushing to production registries.
10. **Pen testing**: Perform security review and penetration testing for public-facing deployments.

Follow these steps and the checklist in `docs/security_checklist.md` before public submission.


## Screenshots

![Hero Mockup](docs/screenshots/hero.png)
![Call Page](docs/screenshots/call.png)
![Recordings](docs/screenshots/recordings.png)

(Replace the above placeholders with real screenshots before final submission for better presentation.)
