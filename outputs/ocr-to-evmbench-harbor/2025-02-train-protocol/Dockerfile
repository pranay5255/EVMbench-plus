FROM pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

RUN curl -fsSL \
        https://nodejs.org/dist/v22.15.0/node-v22.15.0-linux-x64.tar.xz \
        -o /tmp/node-v22.15.0-linux-x64.tar.xz \
    && echo "dafe2e8f82cb97de1bd10db9e2ec4c07bbf53389b0799b1e095a918951e78fd4  /tmp/node-v22.15.0-linux-x64.tar.xz" \
        | sha256sum -c - \
    && mkdir -p /opt/node-v22.15.0 \
    && tar --no-same-owner --strip-components=1 -xJf \
        /tmp/node-v22.15.0-linux-x64.tar.xz \
        -C /opt/node-v22.15.0 \
    && rm /tmp/node-v22.15.0-linux-x64.tar.xz

ENV PATH="/opt/node-v22.15.0/bin:${PATH}"
ENV HARDHAT_DISABLE_TELEMETRY_PROMPT=true

RUN test "$(node --version)" = "v22.15.0" \
    && mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin \
        https://github.com/layerswap/layerswap-atomic-bridge.git \
    && git fetch --depth=1 origin \
        6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = \
        "6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git submodule status --recursive)" \
    && cd "$AUDIT_DIR/chains/evm/solidity" \
    && npm ci --legacy-peer-deps \
    && PRIV_KEY=0x1111111111111111111111111111111111111111111111111111111111111111 \
        npx hardhat compile \
    && find "$AUDIT_DIR" -type f -iname '*.pdf' -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && test -z "$(find "$AUDIT_DIR" -type f -iname '*.pdf' -print -quit)" \
    && test -z "$(find "$AUDIT_DIR" -mindepth 2 -name .git -print -quit)" \
    && cd "$AUDIT_DIR" \
    && test "$(git rev-parse HEAD)" = \
        "6c96f61d7d6c7e8a8991a12e40068ab53b0a9e7b" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\\.(pdf|jsonl)$')"

WORKDIR $AGENT_DIR
