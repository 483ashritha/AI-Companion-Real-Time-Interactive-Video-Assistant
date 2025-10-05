# Security & Deployment Checklist

This checklist helps ensure safe production deployment:

- [ ] Replace demo JWT with real auth and rotate secret
- [ ] Use HTTPS/TLS everywhere
- [ ] Use a managed TURN server and configure credentials securely
- [ ] Store recordings in S3 (or private blob storage) instead of local disk
- [ ] Configure Redis with password and private networking
- [ ] Add rate-limiting (e.g., via FastAPI middleware or API Gateway)
- [ ] Add CSP and other security headers via the reverse proxy
- [ ] Ensure CI secrets (GHCR_TOKEN) are stored as GitHub secrets
- [ ] Run dependency vulnerability scans and container image scans
- [ ] Configure monitoring and alerting (Sentry, Prometheus, etc.)
