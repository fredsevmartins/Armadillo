"""Synthetic in-process audit benchmark, not a scientific benchmark."""

import json
import platform
import statistics
import time
import tracemalloc

from armadillo.core import audit

data = {
    "schema_version": "1.0",
    "document": "Synthetic claim. Synthetic evidence.",
    "nodes": [],
}
for i in range(250):
    data["nodes"].extend(
        [
            {
                "id": f"c{i}",
                "kind": "claim",
                "quote": "Synthetic claim.",
                "supports": [],
            },
            {
                "id": f"e{i}",
                "kind": "evidence",
                "quote": "Synthetic evidence.",
                "supports": [f"c{i}"],
            },
        ]
    )
audit(data)
tracemalloc.start()
durations = []
for _ in range(20):
    start = time.perf_counter()
    result = audit(data)
    durations.append(time.perf_counter() - start)
    assert result["status"] == "SOURCE_LINKED"
_, peak = tracemalloc.get_traced_memory()
print(
    json.dumps(
        {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "nodes": 500,
            "iterations": 20,
            "warmup": 1,
            "median_seconds": statistics.median(durations),
            "min_seconds": min(durations),
            "max_seconds": max(durations),
            "peak_python_allocated_bytes": peak,
            "timing_includes_tracemalloc": True,
        },
        indent=2,
    )
)
