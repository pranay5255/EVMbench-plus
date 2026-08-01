#!/usr/bin/env python3
"""Validate the non-grading EVMBench detect JSON companion."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_VERSION = "evmbench.detect_submission.v1"
STRING_FIELDS = (
    "id",
    "title",
    "severity",
    "root_cause",
    "attack_or_failure_sequence",
    "asset_loss_impact",
)
LIST_FIELDS = ("affected_paths", "code_evidence")


def validate(value: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["submission must be a JSON object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must equal {SCHEMA_VERSION!r}")
    findings = value.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be an array")
        return errors
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in STRING_FIELDS:
            item = finding.get(field)
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{prefix}.{field} must be a nonempty string")
        for field in LIST_FIELDS:
            item = finding.get(field)
            if (
                not isinstance(item, list)
                or not item
                or any(not isinstance(entry, str) or not entry.strip() for entry in item)
            ):
                errors.append(f"{prefix}.{field} must be a nonempty array of nonempty strings")
    return errors


def main() -> int:
    submission_path = Path(sys.argv[1])
    result_path = Path(sys.argv[2])
    errors: list[str]
    try:
        value = json.loads(submission_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors = [f"unable to load JSON: {exc}"]
    else:
        errors = validate(value)
    result = {
        "schema_version": SCHEMA_VERSION,
        "submission_path": str(submission_path),
        "valid": not errors,
        "errors": errors,
    }
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
