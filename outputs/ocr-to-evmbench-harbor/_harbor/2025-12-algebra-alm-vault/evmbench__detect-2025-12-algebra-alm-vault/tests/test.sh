#!/usr/bin/env bash
set -euo pipefail
mkdir -p /logs/verifier /logs/artifacts
python3 /tests/validate_detect_submission.py "/home/agent/submission/audit.json" /logs/verifier/audit-json-validation.json || true
python3 /tests/evmbench_harbor_verifier.py "--audit-id" "2025-12-algebra-alm-vault" "--mode" "detect" "--hint-level" "none" "--findings-subdir" "" "--agent-output-path" "/home/agent/submission/audit.md"
