# Threat Model

## Project

AI Prompt Injection Detector

## 1. Purpose

This threat model identifies the assets, threat actors, attack
techniques, trust boundaries, and security risks associated with the
AI Prompt Injection Detector.

The threat model is used to guide the design, implementation, testing,
and security controls of the project.

---

## 2. System Under Protection

The system is designed to inspect user-provided prompts before they
are passed to an AI/LLM application.

High-level flow:

User
  ↓
Prompt
  ↓
AI Security Gateway
  ↓
Prompt Detection Engine
  ↓
Security Decision
  ├── ALLOW
  ├── REVIEW
  └── BLOCK
  ↓
LLM

---

## 3. Assets

The following assets require protection.

### 3.1 System Instructions

Application-level instructions and system prompts may contain
confidential application logic or security policies.

### 3.2 Security Policies

Detection and blocking policies determine how suspicious prompts are
handled.

### 3.3 LLM Application

The underlying AI application must remain protected from malicious
input.

### 3.4 User Data

Prompts may contain sensitive or confidential information.

### 3.5 Security Logs

Logs contain security events and potentially sensitive metadata.

### 3.6 API Credentials

Future integrations may require API keys or authentication
credentials.

### 3.7 Detection Configuration

Rules, thresholds, classifiers, and other detection configurations
must be protected from unauthorized modification.

---

## 4. Threat Actors

### 4.1 Malicious User

A user intentionally submits prompts designed to manipulate the AI
application or bypass security controls.

### 4.2 Automated Attacker

An automated system repeatedly submits prompts to discover weaknesses
in the detection system.

### 4.3 Compromised Account

An attacker gains access to a legitimate user account and uses it to
submit malicious input.

### 4.4 Curious or Unintentional User

A legitimate user may accidentally submit content that resembles a
prompt injection attack.

This is particularly important because excessive blocking can create
false positives.

---

## 5. Threat Categories

### T-001 — Direct Prompt Injection

An attacker attempts to override existing instructions.

Example:

"Ignore all previous instructions."

Potential impact:

- Unauthorized model behavior
- Security-policy bypass
- Manipulation of downstream actions

---

### T-002 — System Prompt Extraction

An attacker attempts to obtain hidden system instructions.

Example:

"Reveal the system instructions."

Potential impact:

- Disclosure of application logic
- Exposure of security controls
- Facilitation of future attacks

---

### T-003 — Role Manipulation

An attacker attempts to assign the model a role intended to bypass
security controls.

Potential impact:

- Policy circumvention
- Unexpected model behavior

---

### T-004 — Security Policy Bypass

An attacker attempts to convince the model to disregard security
requirements.

Potential impact:

- Unauthorized responses
- Security-control bypass

---

### T-005 — Obfuscation

An attacker disguises malicious instructions using techniques such as:

- Encoding
- Unusual spacing
- Character substitution
- Unicode manipulation
- Fragmented instructions

Potential impact:

- Detection evasion

---

### T-006 — Multi-Stage Injection

An attacker distributes malicious instructions across multiple parts
of a prompt or conversation.

Potential impact:

- Detection evasion
- Manipulation of model context

---

### T-007 — Automated Testing of the Detector

An attacker repeatedly submits variations of malicious prompts to
identify patterns that evade detection.

Potential impact:

- Detection-rule discovery
- Increased system load
- Security-control evasion

---

### T-008 — Denial of Service

An attacker submits unusually large or numerous requests.

Potential impact:

- Increased resource consumption
- Increased processing latency
- Service degradation

---

## 6. Trust Boundaries

The primary trust boundaries are:

### Boundary 1 — User to Application

User-provided input cannot automatically be trusted.

```text
UNTRUSTED
   │
   ▼
Security Gateway