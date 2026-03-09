from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List


class VerilogParser:
    module_pattern = re.compile(r"module\s+(\w+)\s*\(")

    def parse(self, path: str) -> Dict:
        source = Path(path).read_text(encoding="utf-8")
        modules: List[str] = self.module_pattern.findall(source)
        return {"module_count": len(modules), "modules": modules}
