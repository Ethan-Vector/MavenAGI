from __future__ import annotations

import json
import os
import time
from dataclasses import asdict
from typing import Any, Dict, Optional


class Tracer:
    def __init__(self, traces_dir: Optional[str] = None) -> None:
        self.traces_dir = traces_dir or os.getenv("MAVENAGI_TRACES_DIR", "traces")
        os.makedirs(self.traces_dir, exist_ok=True)
        self.path = os.path.join(self.traces_dir, f"trace_{int(time.time()*1000)}.jsonl")

    def emit(self, event: Dict[str, Any]) -> None:
        event = dict(event)
        event.setdefault("ts_ms", int(time.time() * 1000))
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
