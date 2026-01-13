# Microservice Deployment Template

Use this structure when adding new microservices (e.g., `cart_service`, `order_service`, etc.)

## Folder Structure for New Microservice

```
cart_service/
├── main.py
├── pyproject.toml
├── README.md
└── infra/
    └── k8s/
        └── manifests/
            ├── deploy.yaml          # Main deployment manifest
            ├── service.yaml         # Kubernetes Service
            ├── ingress.yaml         # Kong Ingress
            ├── configmap.yaml       # Configuration
            └── secrets.yaml         # Secrets
```

## File Templates

### 1. service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: cart-service
  namespace: microservices
  labels:
    app: cart-service
    version: 1.0.0
spec:
  type: ClusterIP
  selector:
    app: cart-service
  ports:
    - name: http
      port: 8000  # Adjust port if different
      targetPort: http
      protocol: TCP
```

### 2. ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cart-service-ingress
  namespace: microservices
  labels:
    app: cart-service
  annotations:
    kubernetes.io/ingress.class: kong
    kong.ingress.kubernetes.io/strip-path: "true"
    kong.ingress.kubernetes.io/preserve-host: "true"
spec:
  rules:
    - host: cart.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: cart-service
                port:
                  number: 8000
```

### 3. deploy.yaml (Production-Ready with Kong Compatibility)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-service
  namespace: microservices
  labels:
    app: cart-service
    version: 1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cart-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  minReadySeconds: 10
  revisionHistoryLimit: 5
  template:
    metadata:
      labels:
        app: cart-service
        version: 1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 12094
        fsGroup: 12094
        seccompProfile:
          type: RuntimeDefault
      serviceAccountName: cart-service  # Must match name in shared-infra/k8s/microservices-rbac.yaml
      automountServiceAccountToken: true  # REQUIRED for Kong service discovery
      terminationGracePeriodSeconds: 30
      containers:
        - name: cart-service
          image: arthurhenrique02/cart-service:1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          env:
            - name: ENVIRONMENT
              valueFrom:
                configMapKeyRef:
                  name: cart-service-config
                  key: environment
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: cart-service-config
                  key: log_level
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
              scheme: HTTP
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          securityContext:
            privileged: false
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: var-run
              mountPath: /var/run
            - name: cache
              mountPath: /var/cache
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15"]
      volumes:
        - name: tmp
          emptyDir: {}
        - name: var-run
          emptyDir: {}
        - name: cache
          emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - cart-service
                topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: cart-service
```

## Steps to Add New Microservice

1. **Create directory structure:**
   ```bash
   mkdir -p cart_service/infra/k8s/manifests
   ```

2. **Create manifest files** using templates above (adjust names/ports as needed)

3. **Add ServiceAccount to microservices-rbac.yaml:**
   ```bash
   cd shared-infra/k8s/
   # Edit microservices-rbac.yaml and add new ServiceAccount and RoleBinding
   ```

4. **Deploy:**
   ```bash
   # Deploy shared infrastructure (if not already done)
   kubectl apply -f shared-infra/k8s/
   
   # Deploy microservice
   kubectl apply -f cart_service/infra/k8s/manifests/
   ```

## Key Differences from Standard Kubernetes Deployments

| Setting | Standard | Kong-Compatible | Why |
|---------|----------|-----------------|-----|
| `namespace` | `default` | `microservices` | Better organization and isolation |
| `automountServiceAccountToken` | `false` | `true` | Kong controller needs API access |
| `volumeMounts` | `/tmp`, `/var/run` | + `/var/cache` | Support for Kong plugins |
| `Service.type` | `LoadBalancer` | `ClusterIP` | Kong handles external traffic |
| `Ingress.class` | `nginx` | `kong` | Uses Kong Ingress Controller |

## Verification

After deployment, verify services are registered with Kong:

```bash
# List all Kong Services
kubectl get services -n microservices

# Check Kong Ingress Controller logs
kubectl logs -n kong -l app.kubernetes.io/name=kong -c ingress-controller

# Verify service discovery
kubectl get ingress -n microservices
```
