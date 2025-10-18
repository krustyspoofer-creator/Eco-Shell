# EchoShell Plugins

This directory contains plugin manifests for extending EchoShell capabilities.

## Plugin Types

- **encoder**: Text encoding and embedding generation
- **reasoner**: Reasoning and inference engines
- **planner**: Task planning and orchestration
- **datastore**: Data storage and retrieval
- **runtime**: Runtime environments and execution engines

## Available Plugins

### nlp-encoder-v1
NLU Encoder (v1) - Text encoder producing embeddings and token metadata for Balorg.

**Type**: encoder  
**Version**: 2025.10.18  
**Entrypoint**: grpc://nlp-encoder.internal:50051

**Capabilities**:
- encode_text
- stream_encode

**Security Profile**: default-strict
- Signature required
- Network egress: deny
- Secrets access: vault
- Forbidden syscalls: fork, exec, ptrace

See [nlp-encoder-v1.yaml](./nlp-encoder-v1.yaml) for full specification.
