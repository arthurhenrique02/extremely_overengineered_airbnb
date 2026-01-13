# X Overengineered Airbnb

**Status**: In Progress | **Learning Timeline**: ~1 year


A deliberately over-engineered Airbnb clone built to demonstrate advanced distributed systems architecture and modern DevOps practices. This project implements a comprehensive microservices ecosystem using Python FastAPI and Go services, leveraging CockroachDB, Cassandra and maybe some other DBs (e.g. Neo4j for recommendation, etc) for data persistence, with gRPC for inter-service communication. The infrastructure is orchestrated through Kubernetes with Terraform for IaC, Docker containerization, and Kong API gateway for routing. Event-driven architecture powers the system through Kafka pub/sub messaging, implementing both event sourcing and CQRS patterns with Saga orchestration for distributed transactions.

The observability stack includes Prometheus for metrics collection, Grafana for visualization, Loki for log aggregation, and Tempo for distributed tracing. Data is persisted across multiple storage backends including S3 for object storage, with event streams maintaining complete audit trails. This intentionally complex setup serves as a reference implementation for production-grade distributed systems, showcasing enterprise-level patterns and technologies in a single, cohesive project.
