"""输入侧安全防护：prompt injection 检测 + 敏感信息脱敏。"""

import re
from dataclasses import dataclass

INJECTION_PATTERNS = [
    r"忽略(以上|上面|之前|先前)(的)?(指令|规则|提示|约束)",
    r"ignore (all )?(previous|above|prior) (instructions|rules|prompts)",
    r"disregard (all )?(previous|above) (instructions|rules)",
    r"你(现在|从此)是",
    r"system\s*:",
    r"<\s*/?\s*system\s*>",
    r"越狱|jailbreak",
    r"DAN mode",
]

PHONE_PATTERN = re.compile(r"1[3-9]\d{9}")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


@dataclass
class GuardResult:
    allowed: bool
    message: str
    injection_detected: bool = False
    redacted: bool = False


def detect_injection(text: str) -> bool:
    lowered = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE) or re.search(pattern, lowered):
            return True
    return False


def redact_sensitive(text: str) -> tuple[str, bool]:
    redacted = False
    if PHONE_PATTERN.search(text):
        text = PHONE_PATTERN.sub("[手机号已脱敏]", text)
        redacted = True
    if EMAIL_PATTERN.search(text):
        text = EMAIL_PATTERN.sub("[邮箱已脱敏]", text)
        redacted = True
    return text, redacted


def guard_input(text: str) -> GuardResult:
    """检测注入；对敏感信息脱敏后放行。"""
    if detect_injection(text):
        return GuardResult(
            allowed=False,
            message="检测到潜在的 prompt injection，请求已被拦截。",
            injection_detected=True,
        )
    cleaned, was_redacted = redact_sensitive(text)
    return GuardResult(
        allowed=True,
        message=cleaned,
        redacted=was_redacted,
    )
