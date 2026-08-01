FROM pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

ENV HARDHAT_DISABLE_TELEMETRY=true \
    TENDERLY_ENABLE_OUTDATED_VERSION_CHECK=false

RUN apt-get update \
    && apt-get install -y --no-install-recommends libudev-dev libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/brava-labs/brava-contracts.git \
    && git fetch --depth=1 origin 655613454d3c6264096457adeb387b965fefc3c6 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "655613454d3c6264096457adeb387b965fefc3c6" \
    && test "$(git rev-list --all --count)" = "1" \
    && npm ci \
    && TENDERLY_VIRTUAL_MAINNET_RPC=http://127.0.0.1:8545 \
       TENDERLY_API_KEY=placeholder \
       TENDERLY_PROJECT=placeholder \
       TENDERLY_USERNAME=placeholder \
       ./node_modules/.bin/hardhat compile \
    && git remote remove origin \
    && test "$(git rev-parse HEAD)" = "655613454d3c6264096457adeb387b965fefc3c6" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git status --porcelain)" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\.(pdf|jsonl)$')"

WORKDIR $AGENT_DIR
