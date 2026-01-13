# Shared Kubernetes Infrastructure

This folder contains shared Kubernetes configurations for the microservices architecture with Kong API Gateway.

## Folder Structure

```
shared-infra/k8s/
├── namespace.yaml              # Create microservices and kong namespaces
├── kong/
│   ├── kong-values.yaml        # Helm values for Kong installation
│   └── kong-rbac.yaml          # RBAC for Kong Ingress Controller
├── microservices-rbac.yaml     # RBAC for all microservices
└── README.md                   # This file
```

## Deployment Order

1. **Create Namespaces:**
   ```bash
   kubectl apply -f namespace.yaml
   ```

2. **Setup Kong API Gateway:**
   ```bash
   # Add Kong Helm repository
   helm repo add kong https://charts.konghq.com
   helm repo update
   
   # Install Kong
   helm install kong kong/kong -f kong/kong-values.yaml -n kong
   
   # Or apply RBAC first
   kubectl apply -f kong/kong-rbac.yaml
   ```

3. **Setup Microservices RBAC:**
   ```bash
   kubectl apply -f microservices-rbac.yaml
   ```

4. **Deploy Individual Microservices:**
   ```bash
   # Deploy auth-service
   kubectl apply -f ../auth_service/infra/k8s/manifests/
   
   # Deploy cart-service (when created)
   kubectl apply -f ../cart_service/infra/k8s/manifests/
   ```

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│             Kong API Gateway                    │
│    (Load Balancer + API Management)             │
│  Namespace: kong                                │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
    ┌───▼──────┐  ┌──▼────────┐ ┌──▼────────┐
    │   Auth   │  │   Cart    │ │  Other... │
    │ Service  │  │  Service  │ │ Services  │
    │ (3 pods) │  │ (3 pods)  │ │           │
    └──────────┘  └───────────┘ └───────────┘
    Namespace: microservices
```

## Adding New Microservices

When adding a new microservice (e.g., `cart_service`, `order_service`):

1. Create a new folder: `cart_service/`
2. Mirror the structure of `auth_service/`
3. Create `infra/k8s/manifests/` with:
   - `deploy.yaml` or `deploy-[version].yaml`
   - `service.yaml`
   - `ingress.yaml` (Kong Ingress)
   - `configmap.yaml`
   - `secrets.yaml`
4. Add ServiceAccount entry to `microservices-rbac.yaml`
5. Deploy using `kubectl apply -f cart_service/infra/k8s/manifests/`

## Kong Service Discovery

Services are automatically discovered via:
- **Kubernetes Service name**: Used as upstream in Kong
- **Namespace**: `microservices`
- **Service mesh**: Optional (Istio, Linkerd)

Kong will load balance traffic to all healthy pods using the Service DNS name.

## Security Considerations

- ServiceAccount tokens are **mounted** (required for discovery)
- RBAC limits permissions to minimum necessary
- Read-only root filesystem enforced in containers
- Security context properly configured
- Network policies can be added if needed

## Kong Ingress Examples

See individual service `infra/k8s/manifests/ingress.yaml` for Kong Ingress definitions.

Example Kong Ingress:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: auth-service-ingress
  namespace: microservices
  annotations:
    kubernetes.io/ingress.class: kong
spec:
  rules:
    - host: auth.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: auth-service
                port:
                  number: 8000
```
