# Balorg AI Plugin Interface Specifications

## Overview

This document provides detailed interface specifications for all Balorg AI injector plugins, including method signatures, data structures, error handling, and implementation examples.

---

## Common Data Structures

### Artifact Structure
```typescript
interface Artifact {
  artifact_id: string;           // UUID
  name: string;                  // Human-readable name
  type: ArtifactType;            // Type of artifact
  version: string;               // Semantic version
  checksum: string;              // SHA-256 hash
  signature?: string;            // Base64-encoded signature
  provenance: Provenance;        // Origin and build info
  dependencies: Dependency[];    // Required dependencies
  allowed_environments: string[]; // Permitted deployment targets
  metadata: ArtifactMetadata;    // Type-specific metadata
}

enum ArtifactType {
  DEPENDENCY = 'dependency',
  CODE = 'code',
  DATA = 'data',
  MODEL = 'model',
  SECRETS = 'secrets'
}

interface Provenance {
  created_by: string;            // User or service ID
  created_at: string;            // ISO 8601 timestamp
  source: string;                // Git URL or origin
  build_id?: string;             // CI build identifier
  commit_hash?: string;          // Git commit SHA
}

interface Dependency {
  name: string;                  // Dependency name
  version: string;               // Semantic version or range
  source: string;                // Registry URL
  checksum: string;              // SHA-256 hash
  signature_required: boolean;   // Signature verification flag
}

interface ArtifactMetadata {
  language?: string;             // python, javascript, go, etc.
  runtime?: string;              // Runtime version
  entry_point?: string;          // Main execution entry
  schema?: object;               // Data schema (for data artifacts)
  model_type?: string;           // Model architecture (for model artifacts)
  [key: string]: any;            // Additional metadata
}
```

### Configuration Structure
```typescript
interface InjectionConfig {
  target: string;                // Target service or environment
  env: Environment;              // Deployment environment
  policy_profile: string;        // Policy to apply
  mode: ExecutionMode;           // Execution mode
  constraints: Constraints;      // Resource and security constraints
  callback_url?: string;         // Webhook for status updates
}

enum Environment {
  DEV = 'dev',
  STAGING = 'staging',
  PROD = 'prod'
}

enum ExecutionMode {
  EXPLORE = 'explore',           // Read-only exploration
  EXECUTE = 'execute',           // Full execution
  DRY_RUN = 'dry-run'           // Sandbox simulation
}

interface Constraints {
  max_memory?: string;           // e.g., "512MB"
  timeout?: string;              // e.g., "60s"
  allowed_apis?: string[];       // Permitted API categories
  network_access?: boolean;      // Network egress allowed
  filesystem_access?: 'none' | 'readonly' | 'readwrite';
}
```

### Result Structures
```typescript
interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: string[];
  metadata: object;
}

interface ValidationError {
  code: string;
  message: string;
  field?: string;
  severity: 'error' | 'warning';
}

interface InjectionResult {
  injection_id: string;
  status: InjectionStatus;
  timestamp: string;
  metadata: object;
  rollback_info: RollbackInfo;
}

enum InjectionStatus {
  QUEUED = 'queued',
  VALIDATING = 'validating',
  STAGING = 'staging',
  INJECTED = 'injected',
  FAILED = 'failed',
  REVERTED = 'reverted'
}

interface RollbackInfo {
  snapshot_id?: string;
  previous_state?: object;
  dependencies_to_restore?: string[];
}
```

---

## Plugin Interface Specification

### InjectorPlugin Base Interface

```typescript
/**
 * Base interface that all injector plugins must implement
 */
interface InjectorPlugin {
  /**
   * Get plugin metadata
   */
  getMetadata(): PluginMetadata;
  
  /**
   * Validate artifact and configuration
   * 
   * @param artifact - Artifact to validate
   * @param config - Injection configuration
   * @returns Validation result with errors/warnings
   * @throws PluginError if validation cannot proceed
   */
  validate(artifact: Artifact, config: InjectionConfig): Promise<ValidationResult>;
  
  /**
   * Prepare artifact for injection
   * 
   * @param artifact - Validated artifact
   * @param context - Runtime context
   * @returns Prepared artifact ready for injection
   * @throws PluginError if preparation fails
   */
  prepare(artifact: Artifact, context: RuntimeContext): Promise<PreparedArtifact>;
  
  /**
   * Perform the injection
   * 
   * @param prepared - Prepared artifact
   * @param target - Target identifier
   * @returns Injection result with metadata
   * @throws PluginError if injection fails
   */
  inject(prepared: PreparedArtifact, target: string): Promise<InjectionResult>;
  
  /**
   * Revert/rollback an injection
   * 
   * @param injectionResult - Result from inject() call
   * @returns True if successfully reverted
   * @throws PluginError if revert fails
   */
  revert(injectionResult: InjectionResult): Promise<boolean>;
  
  /**
   * Get audit and provenance metadata
   * 
   * @returns Audit metadata
   */
  auditMetadata(): AuditMetadata;
  
  /**
   * Health check for plugin
   * 
   * @returns Health status
   */
  health(): HealthStatus;
}

interface PluginMetadata {
  plugin_id: string;
  plugin_type: ArtifactType;
  version: string;
  description: string;
  supported_runtimes: string[];
  capabilities: string[];
}

interface RuntimeContext {
  execution_id: string;
  environment: Environment;
  user_id: string;
  trace_id: string;
  policy: PolicyConfig;
  secrets_provider?: SecretsProvider;
}

interface PreparedArtifact {
  artifact: Artifact;
  instrumented_payload: any;
  dependencies_resolved: boolean;
  sandbox_ready: boolean;
  metadata: object;
}

interface AuditMetadata {
  plugin_type: string;
  plugin_version: string;
  operations: AuditOperation[];
  resource_usage: ResourceUsage;
}

interface AuditOperation {
  operation: string;
  timestamp: string;
  duration_ms: number;
  result: 'success' | 'failure';
  details: object;
}

interface ResourceUsage {
  cpu_ms: number;
  memory_mb: number;
  network_bytes: number;
  storage_bytes: number;
}

interface HealthStatus {
  healthy: boolean;
  message?: string;
  last_check: string;
}
```

---

## Specific Plugin Interfaces

### 1. Dependency Injector Plugin

```typescript
interface DependencyInjectorPlugin extends InjectorPlugin {
  /**
   * Resolve dependency tree
   * 
   * @param manifest - Dependency manifest
   * @returns Resolved dependency graph
   */
  resolveDependencies(manifest: DependencyManifest): Promise<DependencyGraph>;
  
  /**
   * Register dependency in container
   * 
   * @param dependency - Dependency to register
   * @param scope - Lifetime scope
   * @returns Registration handle
   */
  registerDependency(dependency: Dependency, scope: LifetimeScope): Promise<string>;
  
  /**
   * Unregister dependency from container
   * 
   * @param handle - Registration handle
   * @returns True if unregistered
   */
  unregisterDependency(handle: string): Promise<boolean>;
  
  /**
   * Check compatibility of dependencies
   * 
   * @param dependencies - Dependencies to check
   * @returns Compatibility report
   */
  checkCompatibility(dependencies: Dependency[]): Promise<CompatibilityReport>;
}

interface DependencyManifest {
  name: string;
  version: string;
  dependencies: Dependency[];
  dev_dependencies?: Dependency[];
  peer_dependencies?: Dependency[];
}

interface DependencyGraph {
  root: DependencyNode;
  all_dependencies: DependencyNode[];
  conflicts: DependencyConflict[];
}

interface DependencyNode {
  name: string;
  version: string;
  dependencies: DependencyNode[];
  depth: number;
}

interface DependencyConflict {
  package: string;
  required_versions: string[];
  resolution: string;
}

enum LifetimeScope {
  SINGLETON = 'singleton',      // One instance for entire application
  SCOPED = 'scoped',            // One instance per scope/request
  TRANSIENT = 'transient'       // New instance every time
}

interface CompatibilityReport {
  compatible: boolean;
  issues: CompatibilityIssue[];
  recommendations: string[];
}

interface CompatibilityIssue {
  severity: 'error' | 'warning' | 'info';
  package: string;
  message: string;
  fix?: string;
}
```

### 2. Code Injector Plugin

```typescript
interface CodeInjectorPlugin extends InjectorPlugin {
  /**
   * Compile/transpile code if needed
   * 
   * @param code - Source code
   * @param options - Compilation options
   * @returns Compiled artifact
   */
  compile(code: string, options: CompileOptions): Promise<CompiledArtifact>;
  
  /**
   * Create sandbox environment
   * 
   * @param config - Sandbox configuration
   * @returns Sandbox instance
   */
  createSandbox(config: SandboxConfig): Promise<Sandbox>;
  
  /**
   * Execute code in sandbox
   * 
   * @param sandbox - Sandbox instance
   * @param code - Code to execute
   * @returns Execution result
   */
  executeInSandbox(sandbox: Sandbox, code: any): Promise<ExecutionResult>;
  
  /**
   * Instrument code for monitoring
   * 
   * @param code - Code to instrument
   * @returns Instrumented code
   */
  instrumentCode(code: any): Promise<any>;
}

interface CompileOptions {
  target: string;                // Compilation target
  optimize: boolean;             // Enable optimizations
  source_maps: boolean;          // Generate source maps
  strict: boolean;               // Strict mode
}

interface CompiledArtifact {
  bytecode: Buffer;
  source_map?: string;
  metadata: object;
}

interface SandboxConfig {
  runtime: string;               // Runtime environment
  memory_limit: string;          // Memory limit
  timeout: string;               // Execution timeout
  allowed_modules: string[];     // Whitelisted modules
  filesystem: 'none' | 'readonly' | 'virtual';
  network: 'none' | 'restricted' | 'full';
}

interface Sandbox {
  id: string;
  status: 'created' | 'running' | 'stopped';
  start(): Promise<void>;
  stop(): Promise<void>;
  execute(code: any): Promise<ExecutionResult>;
}

interface ExecutionResult {
  success: boolean;
  output: any;
  error?: Error;
  logs: string[];
  metrics: ExecutionMetrics;
}

interface ExecutionMetrics {
  execution_time_ms: number;
  cpu_usage: number;
  memory_peak_mb: number;
  network_bytes: number;
}
```

### 3. Data Injector Plugin

```typescript
interface DataInjectorPlugin extends InjectorPlugin {
  /**
   * Validate data against schema
   * 
   * @param data - Data to validate
   * @param schema - Schema definition
   * @returns Validation result
   */
  validateSchema(data: any, schema: Schema): Promise<SchemaValidationResult>;
  
  /**
   * Detect and handle PII
   * 
   * @param data - Data to scan
   * @returns PII detection result
   */
  detectPII(data: any): Promise<PIIDetectionResult>;
  
  /**
   * Redact or tokenize sensitive data
   * 
   * @param data - Data to process
   * @param strategy - Redaction strategy
   * @returns Processed data
   */
  redactSensitiveData(data: any, strategy: RedactionStrategy): Promise<any>;
  
  /**
   * Stream data in chunks
   * 
   * @param source - Data source
   * @param processor - Chunk processor
   * @returns Stream result
   */
  streamData(source: DataSource, processor: ChunkProcessor): Promise<StreamResult>;
}

interface Schema {
  type: 'json-schema' | 'avro' | 'protobuf';
  definition: object;
  version: string;
}

interface SchemaValidationResult {
  valid: boolean;
  errors: SchemaError[];
  validated_fields: string[];
}

interface SchemaError {
  field: string;
  message: string;
  expected: any;
  actual: any;
}

interface PIIDetectionResult {
  pii_found: boolean;
  pii_fields: PIIField[];
  confidence: number;
}

interface PIIField {
  field_path: string;
  pii_type: 'email' | 'phone' | 'ssn' | 'credit_card' | 'name' | 'address';
  confidence: number;
  sample?: string;
}

enum RedactionStrategy {
  REMOVE = 'remove',             // Delete the field
  MASK = 'mask',                 // Replace with ***
  TOKENIZE = 'tokenize',         // Replace with token
  HASH = 'hash',                 // Hash the value
  ENCRYPT = 'encrypt'            // Encrypt the value
}

interface DataSource {
  type: 'file' | 'stream' | 'database' | 'api';
  location: string;
  credentials?: object;
}

interface ChunkProcessor {
  process(chunk: any): Promise<any>;
}

interface StreamResult {
  chunks_processed: number;
  bytes_processed: number;
  errors: number;
  duration_ms: number;
}
```

### 4. Model/Weights Injector Plugin

```typescript
interface ModelInjectorPlugin extends InjectorPlugin {
  /**
   * Load model weights
   * 
   * @param artifact - Model artifact
   * @returns Loaded model
   */
  loadModel(artifact: Artifact): Promise<LoadedModel>;
  
  /**
   * Validate model architecture
   * 
   * @param model - Model to validate
   * @returns Validation result
   */
  validateModel(model: LoadedModel): Promise<ModelValidationResult>;
  
  /**
   * Quantize model for deployment
   * 
   * @param model - Model to quantize
   * @param config - Quantization config
   * @returns Quantized model
   */
  quantizeModel(model: LoadedModel, config: QuantizationConfig): Promise<LoadedModel>;
  
  /**
   * Configure A/B testing
   * 
   * @param models - Models to test
   * @param config - A/B test configuration
   * @returns Test configuration
   */
  setupABTest(models: LoadedModel[], config: ABTestConfig): Promise<ABTestSetup>;
}

interface LoadedModel {
  model_id: string;
  architecture: string;
  weights: Buffer;
  metadata: ModelMetadata;
  inference_ready: boolean;
}

interface ModelMetadata {
  framework: 'pytorch' | 'tensorflow' | 'onnx' | 'custom';
  input_shape: number[];
  output_shape: number[];
  parameter_count: number;
  model_size_mb: number;
}

interface ModelValidationResult {
  valid: boolean;
  checks: ModelCheck[];
  performance_metrics?: PerformanceMetrics;
}

interface ModelCheck {
  check_name: string;
  passed: boolean;
  message?: string;
}

interface PerformanceMetrics {
  inference_latency_ms: number;
  throughput_qps: number;
  memory_usage_mb: number;
}

interface QuantizationConfig {
  method: 'int8' | 'int4' | 'fp16' | 'dynamic';
  calibration_data?: any;
  accuracy_threshold?: number;
}

interface ABTestConfig {
  traffic_split: number[];       // Percentage for each model
  duration_hours: number;        // Test duration
  metrics_to_track: string[];    // Metrics to compare
  success_criteria: object;      // Criteria for winner
}

interface ABTestSetup {
  test_id: string;
  models: string[];
  traffic_split: number[];
  start_time: string;
  end_time: string;
}
```

### 5. Secrets Injector Plugin

```typescript
interface SecretsInjectorPlugin extends InjectorPlugin {
  /**
   * Retrieve secret from secrets manager
   * 
   * @param secretId - Secret identifier
   * @returns Secret value
   */
  getSecret(secretId: string): Promise<Secret>;
  
  /**
   * Store secret in secrets manager
   * 
   * @param secret - Secret to store
   * @returns Secret ID
   */
  storeSecret(secret: Secret): Promise<string>;
  
  /**
   * Rotate secret
   * 
   * @param secretId - Secret to rotate
   * @returns New secret ID
   */
  rotateSecret(secretId: string): Promise<string>;
  
  /**
   * Generate short-lived token
   * 
   * @param config - Token configuration
   * @returns Temporary token
   */
  generateToken(config: TokenConfig): Promise<Token>;
}

interface Secret {
  id?: string;
  name: string;
  value: string;
  type: 'api_key' | 'password' | 'certificate' | 'token' | 'custom';
  metadata: SecretMetadata;
}

interface SecretMetadata {
  created_at: string;
  expires_at?: string;
  rotation_policy?: RotationPolicy;
  allowed_services: string[];
}

interface RotationPolicy {
  frequency_days: number;
  auto_rotate: boolean;
  notification_email?: string;
}

interface TokenConfig {
  scope: string[];
  ttl_seconds: number;
  audience: string;
  claims?: object;
}

interface Token {
  token: string;
  expires_at: string;
  refresh_token?: string;
}
```

---

## Error Handling

### Plugin Error Types

```typescript
class PluginError extends Error {
  code: string;
  severity: 'fatal' | 'error' | 'warning';
  recoverable: boolean;
  metadata: object;
  
  constructor(message: string, code: string, severity: string, recoverable: boolean) {
    super(message);
    this.name = 'PluginError';
    this.code = code;
    this.severity = severity;
    this.recoverable = recoverable;
  }
}

// Specific error types
class ValidationError extends PluginError {}
class PreparationError extends PluginError {}
class InjectionError extends PluginError {}
class RevertError extends PluginError {}
```

### Error Codes

```typescript
enum PluginErrorCode {
  // Validation errors
  INVALID_ARTIFACT = 'INVALID_ARTIFACT',
  INVALID_CONFIG = 'INVALID_CONFIG',
  CHECKSUM_MISMATCH = 'CHECKSUM_MISMATCH',
  SIGNATURE_INVALID = 'SIGNATURE_INVALID',
  
  // Preparation errors
  DEPENDENCY_RESOLUTION_FAILED = 'DEPENDENCY_RESOLUTION_FAILED',
  COMPILATION_FAILED = 'COMPILATION_FAILED',
  SANDBOX_CREATION_FAILED = 'SANDBOX_CREATION_FAILED',
  
  // Injection errors
  TARGET_NOT_FOUND = 'TARGET_NOT_FOUND',
  PERMISSION_DENIED = 'PERMISSION_DENIED',
  RESOURCE_EXHAUSTED = 'RESOURCE_EXHAUSTED',
  INJECTION_TIMEOUT = 'INJECTION_TIMEOUT',
  
  // Revert errors
  SNAPSHOT_NOT_FOUND = 'SNAPSHOT_NOT_FOUND',
  REVERT_FAILED = 'REVERT_FAILED',
  
  // System errors
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  NETWORK_ERROR = 'NETWORK_ERROR',
  STORAGE_ERROR = 'STORAGE_ERROR'
}
```

---

## Plugin Lifecycle

```
1. Plugin Registration
   ↓
2. Plugin Initialization (init)
   ↓
3. Health Check (health)
   ↓
4. Validation Request (validate)
   ↓
5. Preparation (prepare)
   ↓
6. Injection (inject)
   ↓
7. Audit Logging (auditMetadata)
   ↓
8. [Optional] Revert (revert)
   ↓
9. Plugin Teardown
```

---

## Best Practices

### 1. Validation
- Validate early and fail fast
- Provide detailed error messages
- Check all constraints before proceeding
- Validate checksums and signatures

### 2. Preparation
- Use idempotent operations
- Create snapshots for rollback
- Resolve all dependencies upfront
- Minimize preparation time

### 3. Injection
- Use atomic operations where possible
- Implement health checks post-injection
- Log all state changes
- Provide rollback information

### 4. Revert
- Always support rollback
- Test revert operations regularly
- Maintain rollback metadata
- Use snapshots for quick recovery

### 5. Audit
- Log all operations
- Include timestamps and correlation IDs
- Track resource usage
- Report security-relevant events

### 6. Error Handling
- Catch and classify all errors
- Provide recovery suggestions
- Use structured error objects
- Implement retry logic with backoff

---

## Example Implementation

See `examples/dependency_injector_plugin.py` for a complete reference implementation of the Dependency Injector Plugin.

---

## Testing Guidelines

### Unit Tests
- Test each method independently
- Mock external dependencies
- Test error conditions
- Verify audit logging

### Integration Tests
- Test plugin registration
- Test full injection lifecycle
- Test rollback scenarios
- Test concurrent injections

### Performance Tests
- Measure validation time
- Measure preparation time
- Measure injection time
- Monitor resource usage

---

## Change Log

- v1.0.0 (2025-10-18): Initial plugin interface specification
