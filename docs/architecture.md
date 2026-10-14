# System Architecture

## Project

AI Prompt Injection Detector

## 1. Architecture Overview

The AI Prompt Injection Detector is a FastAPI-based security service that analyzes untrusted prompts and identifies potential prompt injection attempts before they reach an AI application.

The application validates incoming requests, applies rate limiting, evaluates prompts using a deterministic security engine, and returns a structured security assessment.

## 2. High-Level Architecture

```text
                    USER
                      |
                      v
              +----------------+
              |   Web Client   |
              +----------------+
                      |
                      v
              +----------------+
              |    FastAPI     |
              |  Security API  |
              +----------------+
                      |
                      v
              +----------------+
              |  Rate Limiter  |
              |  10 requests   |
              |  per minute    |
              +----------------+
                      |
                      v
              +----------------------+
              |  Request Validation  |
              |                      |
              |  Pydantic validation |
              |  Required prompt     |
              |  Maximum length      |
              +----------------------+
                      |
                      v
              +----------------------+
              | Prompt Security      |
              | Engine               |
              |                      |
              | Pattern detection    |
              | Threat classification|
              | Risk scoring         |
              | Security decision    |
              +----------------------+
                      |
                      v
              +----------------------+
              |    API Response      |
              |                      |
              | Classification       |
              | Risk score           |
              | Severity             |
              | Action               |
              | Indicators           |
              +----------------------+
```

The diagram represents the implemented request-analysis pipeline. The service returns a security assessment; it does not currently forward prompts to an external LLM or implement an audit-logging subsystem.

## 3. Main Components

### 3.1 FastAPI Application

File: `app/main.py`

Responsibilities:

- Provides the HTTP API.
- Exposes the root and health-check endpoints.
- Accepts prompt-analysis requests.
- Coordinates request validation, rate limiting, and security analysis.
- Returns structured JSON responses.
- Handles rate-limit exceptions.

### 3.2 Rate Limiter

Technology: SlowAPI

Responsibilities:

- Limits requests to `POST /analyze` to 10 requests per minute per client IP address.
- Returns HTTP `429 Too Many Requests` when the limit is exceeded.
- Helps reduce excessive request traffic.

The current implementation uses in-memory rate-limit storage. A production deployment with multiple workers or application instances should use shared storage and configure trusted proxy handling appropriately.

### 3.3 Request Validation

Technology: Pydantic

Responsibilities:

- Validates the incoming request structure.
- Requires a prompt value.
- Rejects empty or whitespace-only prompts.
- Enforces the configured maximum prompt length of 100,000 characters.

### 3.4 Prompt Security Engine

File: `app/security_engine.py`

Responsibilities:

- Examines prompt content for suspicious patterns.
- Identifies potential prompt injection indicators.
- Classifies detected threats.
- Calculates a risk score.
- Assigns a severity level.
- Determines a recommended security action.

The engine uses deterministic detection logic rather than relying on an external LLM.

### 3.5 API Response

The API returns a structured JSON response containing the security assessment, including applicable fields such as:

- Classification
- Risk score
- Severity
- Recommended action
- Detection indicators

## 4. API Endpoints

| Method | Endpoint | Purpose | Rate Limited |
|---|---|---|---|
| GET | `/` | Returns basic application information | No |
| GET | `/health` | Checks application health | No |
| POST | `/analyze` | Analyzes a submitted prompt | Yes: 10 requests/minute per client IP |

## 5. Request Processing Flow

1. A client submits a prompt to `POST /analyze`.
2. The rate limiter checks the client's request rate.
3. Pydantic validates the request payload.
4. The prompt security engine analyzes the prompt.
5. The engine calculates the risk score and determines the classification, severity, and recommended action.
6. FastAPI returns the analysis result as JSON.
7. If the request limit is exceeded, the API returns HTTP `429 Too Many Requests`.

## 6. Security Controls

The current implementation includes the following controls:

- Request schema validation using Pydantic.
- Rejection of empty or whitespace-only prompts.
- Maximum prompt length enforcement.
- Deterministic prompt injection detection.
- Risk scoring and threat classification.
- API rate limiting.
- Automated tests for API behavior and rate-limit enforcement.

These controls reduce specific risks but do not guarantee detection of every prompt injection attack.

## 7. Limitations and Future Improvements

Current limitations:

- Detection relies on implemented patterns and rules.
- Sophisticated or previously unseen attacks may evade detection.
- In-memory rate-limit storage is not shared across application instances.
- The service does not currently provide persistent security-event auditing.
- The current implementation does not forward approved prompts to an external LLM.

Potential improvements:

- Add additional detection rules and adversarial test cases.
- Introduce shared rate-limit storage for multi-instance deployments.
- Add structured security-event logging and monitoring.
- Introduce configurable security policies.
- Evaluate detection performance against a documented test dataset.
- Integrate with an LLM application through a clearly defined enforcement interface.

## 8. Project Structure

```text
ai-prompt-injection-detector/
├── app/
│   ├── main.py
│   └── security_engine.py
├── docs/
│   ├── architecture.md
│   ├── environment.md
│   ├── security-requirements.md
│   └── threat-model.md
├── tests/
│   ├── test_api.py
│   └── test_security_engine.py
├── screenshots/
├── README.md
├── requirements.txt
└── pytest.ini
```

This is a simplified representation of the project structure. Additional files may exist in the repository.

## 9. Architecture Goal

The goal of the AI Prompt Injection Detector is to provide a testable security layer that analyzes untrusted prompt input, identifies suspicious patterns, assigns risk levels, and returns actionable security assessments through a documented API.
