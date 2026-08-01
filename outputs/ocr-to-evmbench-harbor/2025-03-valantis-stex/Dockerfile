FROM pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

RUN mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/ValantisLabs/valantis-stex \
    && git fetch --depth=1 origin 25a19b663f86b53112a5e020c843904a571cc1e8 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "25a19b663f86b53112a5e020c843904a571cc1e8" \
    && test "$(git rev-list --all --count)" = "1" \
    && git submodule update --init --recursive --depth=1 \
    && test "$(git -C lib/forge-std rev-parse HEAD)" = "b93cf4bc34ff214c099dc970b153f85ade8c9f66" \
    && test "$(git -C lib/openzeppelin-contracts rev-parse HEAD)" = "acd4ff74de833399287ed6b31b4debf6b2b35527" \
    && test "$(git -C lib/openzeppelin-contracts/lib/erc4626-tests rev-parse HEAD)" = "8b1d7c2ac248c33c3506b1bff8321758943c5e11" \
    && test "$(git -C lib/openzeppelin-contracts/lib/forge-std rev-parse HEAD)" = "8f24d6b04c92975e0795b5868aa0d783251cdeaa" \
    && test "$(git -C lib/openzeppelin-contracts/lib/halmos-cheatcodes rev-parse HEAD)" = "c0d865508c0fee0a11b97732c5e90f9cad6b65a5" \
    && test "$(git -C lib/solmate rev-parse HEAD)" = "c93f7716c9909175d45f6ef80a34a650e2d24e56" \
    && test "$(git -C lib/solmate/lib/ds-test rev-parse HEAD)" = "e282159d5170298eb2455a6c05280ab5a73a4ef0" \
    && test "$(git -C lib/valantis-core rev-parse HEAD)" = "18ee8bb9ad91871ddfdb711f0522f15d89e03673" \
    && test "$(git -C lib/valantis-core/lib/forge-std rev-parse HEAD)" = "2f112697506eab12d433a65fdc31a639548fe365" \
    && test "$(git -C lib/valantis-core/lib/forge-std/lib/ds-test rev-parse HEAD)" = "e282159d5170298eb2455a6c05280ab5a73a4ef0" \
    && test "$(git -C lib/valantis-core/lib/openzeppelin-contracts rev-parse HEAD)" = "281550b71c3df9a83e6b80ceefc700852c287570" \
    && test "$(git -C lib/valantis-core/lib/openzeppelin-contracts/lib/erc4626-tests rev-parse HEAD)" = "8b1d7c2ac248c33c3506b1bff8321758943c5e11" \
    && test "$(git -C lib/valantis-core/lib/openzeppelin-contracts/lib/forge-std rev-parse HEAD)" = "c2236853aadb8e2d9909bbecdc490099519b70a4" \
    && test "$(git -C lib/valantis-core/lib/openzeppelin-contracts/lib/forge-std/lib/ds-test rev-parse HEAD)" = "6da7dd8f7395f83e1fb6fa88a64ba9a030f85d4f" \
    && forge build \
    && forge test \
    && find "$AUDIT_DIR" -type f -iname '*.pdf' -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && rm -rf "$AUDIT_DIR/.git/modules" \
    && test -z "$(find "$AUDIT_DIR" -type f -iname '*.pdf' -print -quit)" \
    && test -z "$(find "$AUDIT_DIR" -mindepth 2 -name .git -print -quit)" \
    && test ! -e "$AUDIT_DIR/.git/modules" \
    && test "$(git rev-parse HEAD)" = "25a19b663f86b53112a5e020c843904a571cc1e8" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\\.pdf$')"

ENV FOUNDRY_OFFLINE=true

WORKDIR $AGENT_DIR
