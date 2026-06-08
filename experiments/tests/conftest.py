"""pytest 路径：将 experiments/week2 加入 sys.path 以便 `from lib import ...`。"""

import sys
from pathlib import Path

WEEK2_DIR = Path(__file__).resolve().parent.parent / "week2"
if str(WEEK2_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK2_DIR))
