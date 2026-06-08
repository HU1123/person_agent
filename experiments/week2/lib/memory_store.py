"""长期记忆：JSON 文件持久化。"""

import json
from pathlib import Path


class MemoryStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def _load_raw(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save_fact(self, key: str, value: str) -> None:
        data = self._load_raw()
        data[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load_all(self) -> dict[str, str]:
        return self._load_raw()

    def format_for_prompt(self) -> str:
        data = self.load_all()
        if not data:
            return ""
        lines = [f"- {k}: {v}" for k, v in data.items()]
        return "已知用户长期信息:\n" + "\n".join(lines)
