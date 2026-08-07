FROM docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

ARG AUDIT_DIR=/home/agent/audit
ARG SOLC_URL=https://binaries.soliditylang.org/linux-amd64/solc-linux-amd64-v0.8.26+commit.8a97fa7a
ARG SOLC_SHA256=d5f23436f443edb85d8e76906d12f0a86ce0490e7663a9e608efeb7a93f149ef
ARG FOUNDRY_URL=https://github.com/foundry-rs/foundry/releases/download/v1.7.1/foundry_v1.7.1_linux_amd64.tar.gz
ARG FOUNDRY_SHA256=cf7e688ed0c4c48adffca788b496076e31060b67ac5afe1e43dbb5499c20c88b

RUN set -eux; \
    rm -rf "$AUDIT_DIR"; \
    mkdir -p "$AUDIT_DIR"; \
    git init "$AUDIT_DIR"; \
    cd "$AUDIT_DIR"; \
    git remote add origin https://github.com/kankodu/vii-finance-smart-contracts.git; \
    git fetch --depth=1 origin 2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7; \
    git checkout --detach FETCH_HEAD; \
    test "$(git rev-parse HEAD)" = "2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7"; \
    test "$(git rev-list --all --count)" = "1"; \
    git submodule sync; \
    git submodule update --init lib/euler-interfaces lib/euler-price-oracle lib/v3-core lib/v3-periphery; \
    git submodule update --init --recursive lib/ethereum-vault-connector lib/forge-std lib/openzeppelin-contracts lib/v4-periphery; \
    git -C lib/euler-price-oracle submodule update --init lib/solady lib/v3-core lib/v3-periphery; \
    test "$(git -C lib/ethereum-vault-connector rev-parse HEAD)" = "a7d3c29ef7e4964736e47675e0588630d6afbfd7"; \
    test "$(git -C lib/euler-interfaces rev-parse HEAD)" = "6e32696d2db2f72ae48bbbb4a0b73a8a314b36c8"; \
    test "$(git -C lib/euler-price-oracle rev-parse HEAD)" = "ffc3cb82615fc7d003a7f431175bd1eaf0bf41c5"; \
    test "$(git -C lib/forge-std rev-parse HEAD)" = "77041d2ce690e692d6e03cc812b57d1ddaa4d505"; \
    test "$(git -C lib/openzeppelin-contracts rev-parse HEAD)" = "e4f70216d759d8e6a64144a9e1f7bbeed78e7079"; \
    test "$(git -C lib/v3-core rev-parse HEAD)" = "6562c52e8f75f0c10f9deaf44861847585fc8129"; \
    test "$(git -C lib/v3-periphery rev-parse HEAD)" = "b325bb0905d922ae61fcc7df85ee802e8df5e96c"; \
    test "$(git -C lib/v4-periphery rev-parse HEAD)" = "ad04c9f24a170accf5ea1b2836bbafd514537ca6"; \
    curl -fsSL "$FOUNDRY_URL" -o /tmp/foundry.tar.gz; \
    echo "$FOUNDRY_SHA256  /tmp/foundry.tar.gz" | sha256sum -c -; \
    tar -xzf /tmp/foundry.tar.gz -C /usr/local/bin forge; \
    curl -fsSL "$SOLC_URL" -o /tmp/solc-0.8.26; \
    echo "$SOLC_SHA256  /tmp/solc-0.8.26" | sha256sum -c -; \
    chmod 0755 /tmp/solc-0.8.26; \
    forge build --force --offline --use /tmp/solc-0.8.26; \
    forge test --offline --use /tmp/solc-0.8.26 --match-path test/ERC721WrapperBase.t.sol; \
    forge test --offline --use /tmp/solc-0.8.26 --match-path test/uniswap/factory/UniswapV3WrapperFactory.t.sol; \
    forge test --offline --use /tmp/solc-0.8.26 --match-path test/uniswap/factory/UniswapV4WrapperFactory.t.sol; \
    test "$(git rev-parse HEAD)" = "2a3a72c675a580dcdeb2f7d733d40c6bfb1b3dc7"; \
    test "$(git rev-list --all --count)" = "1"; \
    test -z "$(git status --porcelain)"; \
    git submodule foreach --recursive 'git ls-files -z "*.pdf" "*.jsonl" | xargs -0 -r git update-index --skip-worktree'; \
    git ls-files -z '*.pdf' '*.jsonl' | xargs -0 -r git update-index --skip-worktree; \
    find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -delete; \
    test -z "$(git status --porcelain)"; \
    test -z "$(find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print -quit)"

ENV FOUNDRY_OFFLINE=true
WORKDIR /home/agent
