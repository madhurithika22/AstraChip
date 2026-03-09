from __future__ import annotations

from itertools import combinations
from typing import Dict, List


class GraphBuilder:
    """Converts macro features into a graph structure for mock GNN inference."""

    def build(self, features: List[Dict]) -> Dict:
        nodes = [{"id": idx, **f} for idx, f in enumerate(features)]
        edges = []
        for left, right in combinations(nodes, 2):
            distance = ((left["x"] - right["x"]) ** 2 + (left["y"] - right["y"]) ** 2) ** 0.5
            if distance < 70:
                edges.append({"src": left["id"], "dst": right["id"], "distance": distance})
        return {"nodes": nodes, "edges": edges}
