import re
from dataclasses import dataclass


@dataclass
class DetectionResult:
    classification: str
    risk_score: int
    severity: str
    action: str
    indicators: list[str]


class PromptSecurityEngine:
    """
    Deterministic security engine for detecting common
    prompt injection and LLM manipulation techniques.
    """

    PATTERNS = {
        "prompt_injection": [
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"ignore\s+(all\s+)?prior\s+instructions",
            r"disregard\s+(all\s+)?previous\s+instructions",
            r"forget\s+(all\s+)?previous\s+instructions",
        ],
        "system_prompt_extraction": [
            r"reveal\s+(your\s+)?system\s+prompt",
            r"show\s+(me\s+)?your\s+system\s+prompt",
            r"print\s+(your\s+)?system\s+prompt",
            r"what\s+is\s+your\s+system\s+prompt",
        ],
        "role_manipulation": [
            r"you\s+are\s+now\s+",
            r"act\s+as\s+if\s+you\s+are",
            r"pretend\s+you\s+are",
            r"roleplay\s+as",
        ],
        "policy_bypass": [
            r"bypass\s+(your\s+)?security",
            r"bypass\s+(your\s+)?safety",
            r"disable\s+(your\s+)?safety",
            r"disable\s+(your\s+)?security",
            r"ignore\s+(your\s+)?safety\s+rules",
        ],
        "obfuscated_instruction": [
            r"decode\s+this\s+and\s+follow",
            r"decode\s+the\s+following\s+instructions",
            r"base64.*execute",
        ],
    }

    BASE_RISK = {
        "benign": 5,
        "prompt_injection": 75,
        "system_prompt_extraction": 85,
        "role_manipulation": 60,
        "policy_bypass": 80,
        "obfuscated_instruction": 85,
    }

    def normalize(self, prompt: str) -> str:
        """Normalize user input before security analysis."""
        normalized = prompt.lower().strip()
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def determine_severity(self, risk_score: int) -> str:
        if risk_score >= 80:
            return "critical"
        if risk_score >= 60:
            return "high"
        if risk_score >= 30:
            return "medium"
        return "low"

    def determine_action(self, risk_score: int) -> str:
        if risk_score >= 60:
            return "block"
        if risk_score >= 30:
            return "review"
        return "allow"

    def analyze(self, prompt: str) -> DetectionResult:
        normalized = self.normalize(prompt)

        detections = []

        for classification, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, normalized):
                    detections.append(classification)
                    break

        if not detections:
            classification = "benign"
            risk_score = self.BASE_RISK["benign"]
            indicators = []
        else:
            classification = detections[0]
            risk_score = max(
                self.BASE_RISK[detection]
                for detection in detections
            )

            # Multiple attack indicators increase risk.
            if len(detections) > 1:
                risk_score = min(100, risk_score + 10 * (len(detections) - 1))

            indicators = detections

        severity = self.determine_severity(risk_score)
        action = self.determine_action(risk_score)

        return DetectionResult(
            classification=classification,
            risk_score=risk_score,
            severity=severity,
            action=action,
            indicators=indicators,
        )