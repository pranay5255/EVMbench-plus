FROM pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

RUN mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/itos-finance/Burve.git \
    && git fetch --depth=1 origin f0597768fee2d00c17429941f4721475e1ca5723 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "f0597768fee2d00c17429941f4721475e1ca5723" \
    && test "$(git rev-list --all --count)" = "1" \
    && git submodule update --init --recursive --depth=1 \
    && test "$(git -C lib/Commons rev-parse HEAD)" = "6f65b6bef26e68c6b92bab57dfbf4d13d234a774" \
    && test "$(git -C lib/Commons/lib/forge-std rev-parse HEAD)" = "0e7097750918380d84dd3cfdef595bee74dabb70" \
    && test "$(git -C lib/Commons/lib/openzeppelin-contracts rev-parse HEAD)" = "448efeea6640bbbc09373f03fbc9c88e280147ba" \
    && test "$(git -C lib/Commons/lib/openzeppelin-contracts/lib/erc4626-tests rev-parse HEAD)" = "8b1d7c2ac248c33c3506b1bff8321758943c5e11" \
    && test "$(git -C lib/Commons/lib/openzeppelin-contracts/lib/forge-std rev-parse HEAD)" = "1eea5bae12ae557d589f9f0f0edae2faa47cb262" \
    && test "$(git -C lib/Commons/lib/openzeppelin-contracts/lib/halmos-cheatcodes rev-parse HEAD)" = "c0d865508c0fee0a11b97732c5e90f9cad6b65a5" \
    && test "$(git -C lib/Commons/lib/prb-test rev-parse HEAD)" = "39d6925bf5a7475f7e43247bd59a3e080d33200c" \
    && test "$(git -C lib/Commons/lib/v3-core rev-parse HEAD)" = "d8b1c635c275d2a9450bd6a78f3fa2484fef73eb" \
    && test "$(git -C lib/Commons/lib/v3-periphery rev-parse HEAD)" = "0682387198a24c7cd63566a2c58398533860a5d1" \
    && test "$(git -C lib/forge-std rev-parse HEAD)" = "b93cf4bc34ff214c099dc970b153f85ade8c9f66" \
    && test "$(git -C lib/openzeppelin-contracts rev-parse HEAD)" = "69c8def5f222ff96f2b5beff05dfba996368aa79" \
    && test "$(git -C lib/openzeppelin-contracts/lib/erc4626-tests rev-parse HEAD)" = "8b1d7c2ac248c33c3506b1bff8321758943c5e11" \
    && test "$(git -C lib/openzeppelin-contracts/lib/forge-std rev-parse HEAD)" = "ae570fec082bfe1c1f45b0acca4a2b4f84d345ce" \
    && test "$(git -C lib/openzeppelin-contracts/lib/forge-std/lib/ds-test rev-parse HEAD)" = "e282159d5170298eb2455a6c05280ab5a73a4ef0" \
    && test "$(git -C lib/openzeppelin-contracts/lib/halmos-cheatcodes rev-parse HEAD)" = "c0d865508c0fee0a11b97732c5e90f9cad6b65a5" \
    && test "$(git -C lib/v3-core rev-parse HEAD)" = "e3589b192d0be27e100cd0daaf6c97204fdb1899" \
    && curl -fL https://binaries.soliditylang.org/linux-amd64/solc-linux-amd64-v0.8.27+commit.40a35a09 -o /tmp/solc-0.8.27 \
    && echo "b9977d500c17cba6f0032ca939ef98c4decf6363f19f386d05fb02f708115264  /tmp/solc-0.8.27" | sha256sum -c - \
    && chmod 0755 /tmp/solc-0.8.27 \
    && find "$AUDIT_DIR" -type f -iname '*.pdf' -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && rm -rf "$AUDIT_DIR/.git/modules" \
    && truncate -s 0 "$AUDIT_DIR/.gitmodules" \
    && git update-index --assume-unchanged .gitmodules \
    && test -z "$(find "$AUDIT_DIR" -type f -iname '*.pdf' -print -quit)" \
    && test -z "$(find "$AUDIT_DIR" -mindepth 2 -name .git -print -quit)" \
    && test ! -e "$AUDIT_DIR/.git/modules" \
    && test ! -s "$AUDIT_DIR/.gitmodules" \
    && test "$(git ls-files -v .gitmodules | cut -c1)" = "h" \
    && forge build --force --offline --use /tmp/solc-0.8.27 --via-ir --optimize --remappings @openzeppelin/=lib/openzeppelin-contracts/contracts/ --remappings @openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/ \
    && test "$(git rev-parse HEAD)" = "f0597768fee2d00c17429941f4721475e1ca5723" \
    && test "$(git rev-list --all --count)" = "1" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\\.(pdf|jsonl)$')"

ENV FOUNDRY_OFFLINE=true

WORKDIR $AGENT_DIR
