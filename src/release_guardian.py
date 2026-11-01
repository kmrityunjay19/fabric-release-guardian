"""Generate a read-only Fabric release readiness report."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--environment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    environment = json.loads(args.environment.read_text())
    failures, warnings = [], []
    if not environment.get("workspace_id") or not environment.get("capacity_id"):
        failures.append("Target workspace or capacity is not configured.")
    missing = set(manifest.get("required_connections", [])) - set(environment.get("connections", []))
    if missing:
        failures.append(f"Missing target connection mappings: {', '.join(sorted(missing))}")
    if environment.get("requires_change_reference") and not manifest.get("change_reference"):
        failures.append("Production releases require a change reference.")
    high_impact = {"SemanticModel", "Lakehouse", "Warehouse"}
    risk = "High" if any(item["type"] in high_impact for item in manifest.get("items", [])) else "Standard"
    if risk == "High":
        warnings.append("High-impact item type detected; require an approval gate and post-deployment smoke test.")
    decision = "BLOCK" if failures else ("APPROVAL REQUIRED" if warnings else "READY")
    report = [f"# Release readiness: {manifest['release_id']}", "", f"**Environment:** {environment['name']}", f"**Decision:** {decision}", f"**Risk:** {risk}", "", "## Items"]
    report += [f"- {item['name']} ({item['type']}): {item['change']}" for item in manifest["items"]]
    report += ["", "## Blocking issues"] + ([f"- {x}" for x in failures] or ["- None"])
    report += ["", "## Review notes"] + ([f"- {x}" for x in warnings] or ["- None"])
    args.output.write_text("\n".join(report) + "\n")
    print(decision)
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
