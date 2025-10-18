# Balorg AI Example Manifests and API Documentation

## Overview

This document provides concrete examples of manifests, API requests, and configuration files for the Balorg AI injection framework.

---

## Example Manifests

### 1. Dependency Manifest Example

```yaml
# dependency-manifest.yaml
name: balorg-nlp-service
version: 2.1.0
type: dependency

artifact:
  checksum: sha256:a3f5b1c2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2
  signature: base64encodedSignatureHere==
  
provenance:
  created_by: ml-team@example.com
  created_at: 2025-10-15T14:30:00Z
  source: https://github.com/example/balorg-nlp
  build_id: ci-build-12345
  commit_hash: abc123def456

dependencies:
  - name: transformers
    version: ^4.30.0
    source: https://pypi.org/
    checksum: sha256:b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5
    signature_required: true
    
  - name: torch
    version: ~2.0.0
    source: https://pypi.org/
    checksum: sha256:c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
    signature_required: true
    
  - name: numpy
    version: ^1.24.0
    source: https://pypi.org/
    checksum: sha256:d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7
    signature_required: false

peer_dependencies:
  - name: python
    version: ^3.9.0

dev_dependencies:
  - name: pytest
    version: ^7.0.0
    source: https://pypi.org/

metadata:
  language: python
  runtime: python3.9
  description: NLP service dependencies for Balorg AI
  
allowed_environments:
  - dev
  - staging
  - prod

policy_requirements:
  signature_verification: true
  sca_scan: true
  license_check: true
  allowed_licenses:
    - MIT
    - Apache-2.0
    - BSD-3-Clause
```

### 2. Code Artifact Manifest Example

```yaml
# code-manifest.yaml
name: balorg-reasoning-module
version: 1.5.2
type: code

artifact:
  checksum: sha256:e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8
  signature: base64encodedCodeSignatureHere==
  size_bytes: 2458624
  
provenance:
  created_by: reasoning-team@example.com
  created_at: 2025-10-16T09:15:00Z
  source: https://github.com/example/balorg-reasoning
  build_id: ci-build-67890
  commit_hash: def456abc789
  build_logs: https://ci.example.com/logs/67890

dependencies:
  - name: balorg-core
    version: ^3.0.0
    source: internal-registry
    checksum: sha256:f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9
    signature_required: true

metadata:
  language: javascript
  runtime: node18
  entry_point: dist/index.js
  module_format: esm
  source_maps: true
  optimized: true
  
  capabilities:
    - symbolic_reasoning
    - constraint_solving
    - planning
    
  api_version: v2
  
allowed_environments:
  - staging
  - prod

security:
  sandbox_required: true
  network_access: restricted
  filesystem_access: readonly
  allowed_apis:
    - logger
    - metrics
    - knowledge_graph
  forbidden_apis:
    - process.exec
    - child_process
    - fs.writeFile
```

### 3. Data Artifact Manifest Example

```json
{
  "name": "balorg-training-dataset",
  "version": "3.2.1",
  "type": "data",
  
  "artifact": {
    "checksum": "sha256:a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
    "signature": "base64encodedDataSignatureHere==",
    "size_bytes": 15728640000,
    "format": "parquet",
    "compression": "snappy"
  },
  
  "provenance": {
    "created_by": "data-team@example.com",
    "created_at": "2025-10-10T12:00:00Z",
    "source": "s3://balorg-datasets/training/v3.2.1/",
    "pipeline_id": "etl-pipeline-54321",
    "data_sources": [
      "wikipedia-20251001",
      "common-crawl-oct-2025",
      "internal-knowledge-base"
    ]
  },
  
  "schema": {
    "type": "avro",
    "definition": {
      "type": "record",
      "name": "TrainingExample",
      "fields": [
        {"name": "id", "type": "string"},
        {"name": "text", "type": "string"},
        {"name": "embedding", "type": {"type": "array", "items": "float"}},
        {"name": "labels", "type": {"type": "array", "items": "string"}},
        {"name": "metadata", "type": {"type": "map", "values": "string"}}
      ]
    }
  },
  
  "metadata": {
    "record_count": 10000000,
    "schema_version": "1.0",
    "pii_redacted": true,
    "quality_score": 0.95,
    "validation_passed": true,
    "sample_available": true,
    "sample_url": "s3://balorg-datasets/training/v3.2.1/sample.parquet"
  },
  
  "allowed_environments": ["dev", "staging", "prod"],
  
  "privacy": {
    "pii_fields": [],
    "retention_days": 365,
    "encryption_required": true,
    "anonymization_applied": true
  },
  
  "quality_metrics": {
    "completeness": 0.98,
    "consistency": 0.96,
    "accuracy": 0.95,
    "uniqueness": 0.99
  }
}
```

### 4. Model Artifact Manifest Example

```yaml
# model-manifest.yaml
name: balorg-vision-encoder
version: 4.0.0
type: model

artifact:
  checksum: sha256:b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1
  signature: base64encodedModelSignatureHere==
  size_bytes: 548576256
  
provenance:
  created_by: vision-team@example.com
  created_at: 2025-10-12T16:45:00Z
  source: https://github.com/example/balorg-vision
  training_job_id: ml-job-99999
  training_duration_hours: 72
  training_cost_usd: 1250.50

model_metadata:
  framework: pytorch
  framework_version: 2.0.1
  architecture: vision_transformer
  architecture_variant: vit-large-patch16
  
  input_shape: [3, 224, 224]
  output_shape: [1024]
  parameter_count: 304000000
  model_size_mb: 523
  
  training_config:
    dataset: imagenet-21k
    epochs: 100
    batch_size: 256
    learning_rate: 0.001
    optimizer: adamw
    
  performance_metrics:
    top1_accuracy: 0.876
    top5_accuracy: 0.982
    inference_latency_ms: 12.5
    throughput_qps: 80
    memory_usage_mb: 2048

quantization:
  available: true
  quantized_versions:
    - format: int8
      size_mb: 131
      accuracy_drop: 0.002
      speedup: 4.2x
    - format: fp16
      size_mb: 261
      accuracy_drop: 0.0001
      speedup: 2.1x

dependencies:
  - name: torch
    version: ~2.0.0
  - name: torchvision
    version: ~0.15.0

allowed_environments:
  - staging
  - prod

deployment:
  recommended_batch_size: 32
  recommended_gpu: nvidia-a100
  min_memory_gb: 16
  warmup_samples: 100
```

### 5. Secrets Manifest Example

```yaml
# secrets-manifest.yaml
name: balorg-api-credentials
version: 1.0.0
type: secrets

artifact:
  checksum: sha256:c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2
  encrypted: true
  encryption_method: aes-256-gcm
  
provenance:
  created_by: security-team@example.com
  created_at: 2025-10-18T08:00:00Z
  source: hashicorp-vault
  
secrets:
  - name: openai_api_key
    type: api_key
    rotation_policy:
      frequency_days: 90
      auto_rotate: true
    allowed_services:
      - balorg-nlp-service
      - balorg-reasoning-module
    
  - name: database_password
    type: password
    rotation_policy:
      frequency_days: 30
      auto_rotate: true
    allowed_services:
      - balorg-data-service
    
  - name: tls_certificate
    type: certificate
    expires_at: 2026-10-18T08:00:00Z
    rotation_policy:
      frequency_days: 365
      auto_rotate: false
      notification_email: security-team@example.com

allowed_environments:
  - prod

security:
  encryption_at_rest: true
  encryption_in_transit: true
  access_logging: true
  approval_required: true
```

---

## API Request Examples

### 1. Upload Artifact

```bash
# Upload dependency artifact
curl -X POST https://api.balorg.ai/v1/artifacts \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: multipart/form-data" \
  -F "manifest=@dependency-manifest.yaml" \
  -F "binary=@balorg-nlp-deps.tar.gz"

# Response
{
  "artifact_id": "art-d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
  "checksum": "sha256:a3f5b1c2d4e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2",
  "signature_required": true,
  "upload_status": "completed",
  "created_at": "2025-10-18T07:20:00Z"
}
```

### 2. Request Injection

```bash
# Request dependency injection
curl -X POST https://api.balorg.ai/v1/injections \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "balorg-nlp-service",
    "injection_type": "dependency",
    "artifact_id": "art-d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
    "env": "staging",
    "version": "2.1.0",
    "policy_profile": "standard",
    "mode": "execute",
    "constraints": {
      "max_memory": "4GB",
      "timeout": "300s",
      "allowed_apis": ["logger", "metrics"]
    },
    "callback_url": "https://webhook.example.com/injection-status"
  }'

# Response
{
  "injection_id": "inj-f6a7b8c9-d0e1-2f3a-4b5c-6d7e8f9a0b1c",
  "status": "queued",
  "created_at": "2025-10-18T07:25:00Z",
  "estimated_duration_seconds": 180
}
```

### 3. Get Injection Status

```bash
curl -X GET https://api.balorg.ai/v1/injections/inj-f6a7b8c9-d0e1-2f3a-4b5c-6d7e8f9a0b1c \
  -H "Authorization: Bearer ${JWT_TOKEN}"

# Response
{
  "injection_id": "inj-f6a7b8c9-d0e1-2f3a-4b5c-6d7e8f9a0b1c",
  "status": "injected",
  "created_at": "2025-10-18T07:25:00Z",
  "updated_at": "2025-10-18T07:28:00Z",
  "lifecycle_events": [
    {
      "phase": "queued",
      "status": "completed",
      "timestamp": "2025-10-18T07:25:00Z"
    },
    {
      "phase": "validation",
      "status": "completed",
      "timestamp": "2025-10-18T07:25:30Z",
      "details": "Static analysis passed, signature verified"
    },
    {
      "phase": "staging",
      "status": "completed",
      "timestamp": "2025-10-18T07:26:00Z",
      "details": "Dependencies resolved, sandbox prepared"
    },
    {
      "phase": "injection",
      "status": "completed",
      "timestamp": "2025-10-18T07:27:30Z",
      "details": "Injected to balorg-nlp-service"
    },
    {
      "phase": "verification",
      "status": "completed",
      "timestamp": "2025-10-18T07:28:00Z",
      "details": "Health checks passed"
    }
  ],
  "audit_metadata": {
    "trace_id": "trace-1a2b3c4d5e6f",
    "span_ids": ["span-001", "span-002", "span-003"],
    "logs_url": "https://logs.balorg.ai/trace/trace-1a2b3c4d5e6f"
  },
  "rollback_info": {
    "snapshot_id": "snap-9a8b7c6d5e4f",
    "can_rollback": true
  }
}
```

### 4. Dry-Run Injection

```bash
curl -X POST https://api.balorg.ai/v1/injections/inj-f6a7b8c9-d0e1-2f3a-4b5c-6d7e8f9a0b1c/dryrun \
  -H "Authorization: Bearer ${JWT_TOKEN}"

# Response
{
  "result": "success",
  "sandbox_id": "sandbox-2b3c4d5e6f7a",
  "execution_logs": [
    "[2025-10-18T07:30:00Z] Sandbox created",
    "[2025-10-18T07:30:05Z] Dependencies loaded",
    "[2025-10-18T07:30:10Z] Service initialized",
    "[2025-10-18T07:30:15Z] Health check: OK",
    "[2025-10-18T07:30:20Z] Sandbox terminated"
  ],
  "metrics": {
    "cpu_usage_percent": 15.5,
    "memory_usage_mb": 256,
    "execution_time_seconds": 20.3,
    "network_bytes_sent": 0,
    "network_bytes_received": 0
  },
  "validation_checks": [
    {
      "check": "dependency_resolution",
      "passed": true
    },
    {
      "check": "api_compatibility",
      "passed": true
    },
    {
      "check": "resource_limits",
      "passed": true
    }
  ]
}
```

### 5. Revert Injection

```bash
curl -X POST https://api.balorg.ai/v1/injections/inj-f6a7b8c9-d0e1-2f3a-4b5c-6d7e8f9a0b1c/revert \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Discovered compatibility issue in production",
    "force": false
  }'

# Response
{
  "status": "reverted",
  "reverted_at": "2025-10-18T07:35:00Z",
  "snapshot_restored": "snap-9a8b7c6d5e4f",
  "rollback_duration_seconds": 15.2,
  "service_status": "healthy"
}
```

### 6. Query Hybrid Knowledge

```bash
# Hybrid retrieval query (symbolic + vector)
curl -X POST https://api.balorg.ai/v1/knowledge/query \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query_embedding": [0.1, 0.2, 0.3, ..., 0.9],
    "symbolic_filters": {
      "entity_type": "person",
      "attributes": {
        "occupation": "scientist"
      },
      "provenance": "verified_sources"
    },
    "top_k": 10,
    "score_threshold": 0.7
  }'

# Response
{
  "results": [
    {
      "id": "entity-abc123",
      "type": "person",
      "name": "Marie Curie",
      "embedding_score": 0.92,
      "symbolic_match_score": 1.0,
      "combined_score": 0.96,
      "attributes": {
        "occupation": "scientist",
        "field": "physics",
        "nobel_prizes": 2
      },
      "provenance": "verified_sources",
      "last_updated": "2025-10-01T00:00:00Z"
    },
    ...
  ],
  "query_time_ms": 45.3,
  "total_matches": 127
}
```

### 7. Request Meta-Learning Adaptation

```bash
curl -X POST https://api.balorg.ai/v1/meta-learning/adapt \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "model-vision-encoder-4.0.0",
    "support_set": {
      "dataset_id": "ds-medical-xrays-v1",
      "num_samples": 100
    },
    "adaptation_config": {
      "method": "few_shot",
      "learning_rate": 0.001,
      "num_steps": 50,
      "freeze_layers": ["layer1", "layer2"]
    },
    "constraints": {
      "max_time_minutes": 10,
      "max_memory_gb": 8
    }
  }'

# Response
{
  "adaptation_id": "adapt-3c4d5e6f7a8b",
  "status": "completed",
  "adapted_model_id": "model-vision-encoder-4.0.0-adapted-medical",
  "metrics": {
    "adaptation_time_seconds": 420,
    "final_loss": 0.035,
    "validation_accuracy": 0.89,
    "parameter_changes": 0.012
  },
  "ready_for_deployment": true
}
```

---

## Configuration Examples

### 1. Policy Profile Configuration

```yaml
# policy-standard.yaml
policy_profile: standard
version: 1.0.0

validation:
  signature_verification: true
  checksum_verification: true
  sca_scan: true
  static_analysis: true
  
  allowed_licenses:
    - MIT
    - Apache-2.0
    - BSD-2-Clause
    - BSD-3-Clause
    
  forbidden_patterns:
    - "eval\\("
    - "exec\\("
    - "subprocess"
    - "__import__\\("

sandbox:
  enabled: true
  runtime: wasm
  
  resource_limits:
    max_memory: 1GB
    max_cpu_cores: 2
    timeout: 300s
    
  filesystem:
    mode: readonly
    allowed_paths:
      - /app/data
      - /tmp
      
  network:
    mode: restricted
    allowed_domains:
      - "*.balorg.ai"
      - "api.example.com"
      
  capabilities:
    allowed:
      - logger
      - metrics
      - knowledge_graph
    forbidden:
      - raw_exec
      - file_write
      - network_raw

authorization:
  approval_required: false
  approvers_count: 0
  
  allowed_roles:
    - developer
    - ml_engineer
    - data_scientist
    
rollback:
  automatic: true
  triggers:
    error_rate_threshold: 0.05
    latency_threshold_ms: 1000
    health_check_failures: 3
    
observability:
  logging_level: info
  trace_sampling_rate: 0.1
  metrics_retention_days: 30
```

### 2. Deployment Configuration

```yaml
# deployment-config.yaml
deployment:
  strategy: canary
  
  canary:
    initial_percentage: 5
    increment_percentage: 25
    interval_minutes: 60
    success_criteria:
      error_rate_max: 0.01
      latency_p99_max_ms: 500
      health_check_success_rate_min: 0.99
      
  rollback:
    automatic: true
    on_failure: true
    snapshot_retention_days: 7
    
  health_checks:
    liveness:
      path: /health/live
      interval_seconds: 10
      timeout_seconds: 5
      failure_threshold: 3
      
    readiness:
      path: /health/ready
      interval_seconds: 5
      timeout_seconds: 3
      failure_threshold: 2
      
    startup:
      path: /health/startup
      interval_seconds: 10
      timeout_seconds: 5
      failure_threshold: 30
      
  monitoring:
    alerts:
      - name: high_error_rate
        condition: error_rate > 0.05
        duration: 5m
        severity: critical
        
      - name: high_latency
        condition: latency_p99 > 1000ms
        duration: 10m
        severity: warning
        
      - name: memory_usage
        condition: memory_usage > 90%
        duration: 5m
        severity: warning
```

---

## Webhook Payload Examples

### Injection Status Update Webhook

```json
{
  "event_type": "injection.status_changed",
  "event_id": "evt-1a2b3c4d5e6f7a8b",
  "timestamp": "2025-10-18T07:28:00Z",
  "injection_id": "inj-f6a7b8c9-d0e1-2f3a-4b5c-6d7e8f9a0b1c",
  "previous_status": "staging",
  "current_status": "injected",
  "details": {
    "artifact_id": "art-d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
    "target": "balorg-nlp-service",
    "environment": "staging"
  },
  "metadata": {
    "duration_seconds": 180,
    "resource_usage": {
      "cpu_seconds": 45,
      "memory_mb": 512
    }
  }
}
```

### Injection Failed Webhook

```json
{
  "event_type": "injection.failed",
  "event_id": "evt-2b3c4d5e6f7a8b9c",
  "timestamp": "2025-10-18T07:30:00Z",
  "injection_id": "inj-a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
  "error": {
    "code": "DEPENDENCY_RESOLUTION_FAILED",
    "message": "Unable to resolve dependency: torch==2.0.0 conflicts with existing torch==1.13.0",
    "severity": "error",
    "recoverable": true
  },
  "details": {
    "phase": "validation",
    "artifact_id": "art-e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b"
  }
}
```

---

## Change Log

- v1.0.0 (2025-10-18): Initial manifest and API examples
