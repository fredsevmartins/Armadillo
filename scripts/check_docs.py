"""Check local Markdown destinations and required editable diagrams."""

import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
for path in [root / "README.md", *root.glob("docs/**/*.md")]:
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        if not (path.parent / target.split("#")[0]).exists():
            errors.append(f"{path.relative_to(root)}: {target}")
for name in ("system", "integration", "data-flow", "workflow", "errors", "testing"):
    if not (root / "docs/diagrams" / (name + ".mmd")).is_file():
        errors.append("Missing diagram: " + name)
if errors:
    raise SystemExit("\n".join(errors))
print("Documentation links and six diagram sources: PASS")
