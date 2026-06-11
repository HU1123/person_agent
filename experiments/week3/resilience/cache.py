"""精确缓存：命中即跳过 LLM 调用。"""

import hashlib
import json
from typing import Any


class ResponseCache:
    """进程内 dict 缓存，key 为输入文本的 hash。"""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    @staticmethod
    def _make_key(message: str, session_id: str = "") -> str:
        payload = json.dumps({"message": message, "session_id": session_id}, ensure_ascii=False)
        return hashlib.sha256(payload.encode()).hexdigest()

    def get(self, message: str, session_id: str = "") -> str | None:
        return self._store.get(self._make_key(message, session_id))

    def set(self, message: str, response: str, session_id: str = "") -> None:
        self._store[self._make_key(message, session_id)] = response

    def clear(self) -> None:
        self._store.clear()

    def stats(self) -> dict[str, Any]:
        return {"size": len(self._store)}
