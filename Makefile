.PHONY: up down test bootstrap argocd-password load-test

up: ## Create kind cluster + Argo CD with Terraform
	cd terraform && terraform init && terraform apply -auto-approve

bootstrap: ## Point Argo CD at this repo (app-of-apps)
	kubectl apply -f gitops/root.yaml

test:
	cd app && python3 -m pytest

argocd-password:
	@kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo

load-test: ## Generate errors to trip the ApiHighErrorRate alert
	for i in $$(seq 1 500); do curl -s -o /dev/null localhost:8080/fail; done

down:
	cd terraform && terraform destroy -auto-approve
