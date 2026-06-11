"""pytest 路径：将 experiments/week2、week3 加入 sys.path。"""

import sys
from pathlib import Path

EXPERIMENTS_DIR = Path(__file__).resolve().parent.parent
WEEK2_DIR = EXPERIMENTS_DIR / "week2"
WEEK3_DIR = EXPERIMENTS_DIR / "week3"

for d in (WEEK2_DIR, WEEK3_DIR):
    s = str(d)
    if s not in sys.path:
        sys.path.insert(0, s)
