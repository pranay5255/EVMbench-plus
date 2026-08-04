FROM docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

ENV HARDHAT_DISABLE_TELEMETRY_PROMPT=true \
    HARDHAT_DISABLE_TELEMETRY=true

RUN test "$(node --version)" = "v22.22.3" \
    && mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/cryptoalgebra/AlmVault.git \
    && git fetch --depth=1 origin 57d820afa1d58bf89073e668f5608942d90188c7 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "57d820afa1d58bf89073e668f5608942d90188c7" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git submodule status --recursive)" \
    && npm ci \
    && ./node_modules/.bin/hardhat compile \
    && ./node_modules/.bin/hardhat test \
    && find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && test -z "$(find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print -quit)" \
    && test -z "$(find "$AUDIT_DIR" -mindepth 2 -name .git -print -quit)" \
    && cd "$AUDIT_DIR" \
    && test "$(git rev-parse HEAD)" = "57d820afa1d58bf89073e668f5608942d90188c7" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git status --porcelain)" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\.(pdf|jsonl)$')"

WORKDIR $AGENT_DIR
