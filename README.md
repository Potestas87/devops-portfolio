# DevOps Portfolio: GitOps on Kubernetes

A small Flask API delivered end to end: tests, image build, vulnerability scan, GitOps deployment, and monitoring with alerts. It runs on a local **kind** cluster, so it costs nothing.

```
git push ─► GitHub Actions ─► test ─► build ─► Trivy scan ─► push to GHCR
                                                          └► bump image tag in charts/api/values.yaml
                                                                   │
Terraform ─► kind cluster + Argo CD ─────────────► Argo CD syncs Git ─► api + monitoring
                                                                   │
                                          Prometheus scrapes /metrics ─► Grafana + alert rules
```

## Stack

| Concern | Tool |
| --- | --- |
| Infrastructure as code | Terraform (kind provider, Helm provider) |
| CI | GitHub Actions, pytest, Trivy |
| CD | Argo CD (app-of-apps, auto-sync, self-heal) |
| Packaging | Helm chart with probes, resource limits, non-root, read-only filesystem |
| Observability | kube-prometheus-stack, ServiceMonitor, PrometheusRule alert |

## Run it

Fork the repo and replace `potestas87` in `charts/api/values.yaml`, `gitops/**`, and `.github/workflows/ci.yml` with your GitHub username.

Prerequisites: Docker, `kind`, `kubectl`, `helm`, `terraform`.

```sh
make up          # cluster + Argo CD
make bootstrap   # Argo CD deploys the API and monitoring stack from Git
curl localhost:8080/          # the API
make load-test   # trips the ApiHighErrorRate alert
make down
```


## Roadmap

- [ ] Add a second service and a database
- [ ] Image signing with cosign, and Kyverno policy to require it
- [ ] Grafana dashboard as code
- [ ] Postmortem in `docs/` from a real failure drill
