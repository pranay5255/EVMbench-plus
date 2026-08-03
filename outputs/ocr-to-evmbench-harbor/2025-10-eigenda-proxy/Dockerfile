FROM golang@sha256:10f549dc8489597aa7ed2b62008199bb96717f52a8e8434ea035d5b44368f8a6 AS go_toolchain

FROM pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

COPY --from=go_toolchain /usr/local/go /usr/local/go

ENV PATH="/usr/local/go/bin:${PATH}"

RUN mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/Layr-Labs/eigenda.git \
    && git fetch --depth=1 origin 066f8ef4f93bb8ce196555904e89adf7ef50e57f \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "066f8ef4f93bb8ce196555904e89adf7ef50e57f" \
    && git submodule update --init --recursive --depth=1 --jobs=1 \
    && test -z "$(git submodule status --recursive | grep '^[+-U]')" \
    && cd "$AUDIT_DIR/contracts" \
    && npm install --ignore-scripts --no-audit --no-fund \
    && forge build \
    && rm -f package-lock.json \
    && cd "$AUDIT_DIR" \
    && go test -mod=readonly -run '^$' ./api/clients/... ./api/proxy/server ./api/proxy/store/generated_key/eigenda/verify \
    && git remote remove origin \
    && find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print > /tmp/eigenda-evidence-files \
    && while IFS= read -r evidence_file; do relative_file=${evidence_file#"$AUDIT_DIR"/}; git update-index --force-remove -- "$relative_file" 2>/dev/null || true; rm -f -- "$evidence_file"; done < /tmp/eigenda-evidence-files \
    && git update-index --force-remove -- SECURITY.md \
    && rm -f SECURITY.md /tmp/eigenda-evidence-files \
    && chmod -R u+w /home/agent/go/pkg/mod \
    && find /home/agent/go/pkg/mod -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -delete \
    && git cat-file commit HEAD > /tmp/eigenda-audited-commit \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && find "$AUDIT_DIR" -name .gitmodules -type f -exec truncate -s 0 {} + \
    && rm -rf "$AUDIT_DIR/.git/modules" "$AUDIT_DIR/.git/objects" "$AUDIT_DIR/.git/refs" "$AUDIT_DIR/.git/logs" \
    && mkdir -p "$AUDIT_DIR/.git/objects" "$AUDIT_DIR/.git/refs/heads" \
    && test "$(git hash-object -w -t commit /tmp/eigenda-audited-commit)" = "066f8ef4f93bb8ce196555904e89adf7ef50e57f" \
    && git update-ref refs/heads/evmbench-source 066f8ef4f93bb8ce196555904e89adf7ef50e57f \
    && git symbolic-ref HEAD refs/heads/evmbench-source \
    && rm -f /tmp/eigenda-audited-commit \
    && test "$(git rev-parse HEAD)" = "066f8ef4f93bb8ce196555904e89adf7ef50e57f" \
    && test -z "$(find /home/agent -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print -quit)" \
    && test ! -e "$AUDIT_DIR/SECURITY.md" \
    && test -z "$(git ls-files | grep -Ei '\.(pdf|jsonl)$|^SECURITY\.md$')" \
    && test -z "$(find "$AUDIT_DIR" -mindepth 2 -name .git -print -quit)" \
    && test -z "$(find "$AUDIT_DIR" -name .gitmodules -type f -size +0c -print -quit)" \
    && test "$(find "$AUDIT_DIR/.git/objects" -type f | wc -l)" = "1"

ENV FOUNDRY_OFFLINE=true

WORKDIR $AGENT_DIR
