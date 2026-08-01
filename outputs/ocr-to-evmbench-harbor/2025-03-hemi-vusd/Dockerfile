FROM pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

ENV HARDHAT_DISABLE_TELEMETRY_PROMPT=true
ENV NODE_URL=http://127.0.0.1:8545

RUN test "$(node --version)" = "v22.22.3" \
    && mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin \
        https://github.com/hemilabs/vusd-stablecoin.git \
    && git fetch --depth=1 origin \
        54f9f235f26df813152b3d3235e7f4373ce473b6 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = \
        "54f9f235f26df813152b3d3235e7f4373ce473b6" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git submodule status --recursive)" \
    && npm ci \
    && npm run compile \
    && find "$AUDIT_DIR" -type f -iname '*.pdf' -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && test -z "$(find "$AUDIT_DIR" -type f -iname '*.pdf' -print -quit)" \
    && test -z "$(find "$AUDIT_DIR" -mindepth 2 -name .git -print -quit)" \
    && cd "$AUDIT_DIR" \
    && test "$(git rev-parse HEAD)" = \
        "54f9f235f26df813152b3d3235e7f4373ce473b6" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\\.(pdf|jsonl)$')"

WORKDIR $AGENT_DIR
