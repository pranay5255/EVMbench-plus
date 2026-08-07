FROM docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

ENV HARDHAT_DISABLE_TELEMETRY_PROMPT=true \
    HARDHAT_DISABLE_TELEMETRY=true

# Pin the exact audited snapshot for offline inspection.
# Full `npm ci` / Hardhat compile requires the private package
# `@securitize/digital_securities@3.1.4`, which currently 404s on the public
# npm registry. Detect agents receive the complete vulnerable Solidity tree
# without baking host gold/OCR evidence or a host worktree copy.
RUN test "$(node --version)" = "v22.22.3" \
    && mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/securitize-io/bc-on-off-ramp-sc.git \
    && git fetch --depth=1 origin a944bb11b106c13a5e43f8de01c9c01eeb5bb472 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "a944bb11b106c13a5e43f8de01c9c01eeb5bb472" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git submodule status --recursive)" \
    && test -f contracts/on-ramp/SecuritizeOnRamp.sol \
    && find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && test -z "$(find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print -quit)" \
    && test -z "$(find "$AUDIT_DIR" -mindepth 2 -name .git -print -quit)" \
    && cd "$AUDIT_DIR" \
    && test "$(git rev-parse HEAD)" = "a944bb11b106c13a5e43f8de01c9c01eeb5bb472" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git status --porcelain)" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\.(pdf|jsonl)$')"

WORKDIR $AGENT_DIR
