FROM docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

ARG AUDIT_DIR=/home/agent/audit
ARG SOLC_URL=https://binaries.soliditylang.org/linux-amd64/solc-linux-amd64-v0.8.24+commit.e11b9ed9
ARG SOLC_SHA256=fb03a29a517452b9f12bcf459ef37d0a543765bb3bbc911e70a87d6a37c30d5f
ARG FOUNDRY_URL=https://github.com/foundry-rs/foundry/releases/download/v1.7.1/foundry_v1.7.1_linux_amd64.tar.gz
ARG FOUNDRY_SHA256=cf7e688ed0c4c48adffca788b496076e31060b67ac5afe1e43dbb5499c20c88b

RUN set -eux; \
    rm -rf "$AUDIT_DIR"; \
    mkdir -p "$AUDIT_DIR"; \
    git init "$AUDIT_DIR"; \
    cd "$AUDIT_DIR"; \
    git remote add origin https://github.com/omni-network/omni.git; \
    git fetch --depth=1 origin 3ef37ae2704db4e1dcb8fc3f7acbb8babb543e8c; \
    git checkout --detach FETCH_HEAD; \
    test "$(git rev-parse HEAD)" = "3ef37ae2704db4e1dcb8fc3f7acbb8babb543e8c"; \
    test "$(git rev-list --all --count)" = "1"; \
    test ! -e "$AUDIT_DIR/.gitmodules"; \
    find "$AUDIT_DIR" -type f -iname '*.pdf' -delete; \
    git ls-files -z '*.pdf' | xargs -0 -r git update-index --skip-worktree; \
    test -z "$(find "$AUDIT_DIR" -type f -iname '*.pdf' -print -quit)"; \
    curl -fsSL "$FOUNDRY_URL" -o /tmp/foundry.tar.gz; \
    echo "$FOUNDRY_SHA256  /tmp/foundry.tar.gz" | sha256sum -c -; \
    tar -xzf /tmp/foundry.tar.gz -C /usr/local/bin forge; \
    curl -fsSL "$SOLC_URL" -o /tmp/solc-0.8.24; \
    echo "$SOLC_SHA256  /tmp/solc-0.8.24" | sha256sum -c -; \
    chmod 0755 /tmp/solc-0.8.24; \
    cd "$AUDIT_DIR/contracts/solve"; \
    corepack pnpm install --frozen-lockfile; \
    forge build --force --offline --use /tmp/solc-0.8.24; \
    test "$(git -C "$AUDIT_DIR" rev-parse HEAD)" = "3ef37ae2704db4e1dcb8fc3f7acbb8babb543e8c"; \
    test "$(git -C "$AUDIT_DIR" rev-list --all --count)" = "1"; \
    test -z "$(git -C "$AUDIT_DIR" status --porcelain)"; \
    test -z "$(find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print -quit)"

ENV FOUNDRY_OFFLINE=true
WORKDIR /home/agent
