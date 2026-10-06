# System Architecture

## Project

AI Prompt Injection Detector

## 1. Architecture Overview

The AI Prompt Injection Detector is designed as a security layer
between an untrusted user input source and an AI/LLM application.

The system analyzes prompts before they are passed to the underlying
LLM.

High-level architecture:

```text
                    USER
                      │
                      │ Prompt
                      ▼
              ┌───────────────┐
              │  Web Client   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   FastAPI     │
              │ Security API  │
              └───────┬───────┘
                      │
                      ▼
          ┌────────────────────────┐
          │  Prompt Security       │
          │       Engine           │
          ├────────────────────────┤
          │ Input Validation       │
          │ Pattern Detection      │
          │ Threat Classification  │
          │ Risk Scoring           │
          │ Security Policy        │
          └───────────┬────────────┘
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
           BLOCK             ALLOW
              │                │
              │                ▼
              │         ┌─────────────┐
              │         │     LLM     │
              │         └──────┬──────┘
              │                │
              └────────┬───────┘
                       ▼
                ┌──────────────┐
                │ Audit Logger │
                └──────┬───────┘
                       ▼
                Security Events