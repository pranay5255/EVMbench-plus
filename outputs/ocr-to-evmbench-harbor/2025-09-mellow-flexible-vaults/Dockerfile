FROM docker.io/pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

ARG FOUNDRY_VERSION=v1.7.1
ARG FOUNDRY_TARBALL_SHA256=cf7e688ed0c4c48adffca788b496076e31060b67ac5afe1e43dbb5499c20c88b
ARG SOLC_VERSION=0.8.25
ARG SOLC_SHA256=c42aada7a52057ddbed93ec011235e256c564c440b68dbaac5ae482babbb3d6d

# Install deterministic Foundry and Solidity toolchains, then fetch only the
# exact report-linked vulnerable snapshot. No host candidate, OCR, PDF, gold,
# or worktree content enters this build context.
RUN curl -fsSL "https://github.com/foundry-rs/foundry/releases/download/${FOUNDRY_VERSION}/foundry_${FOUNDRY_VERSION}_linux_amd64.tar.gz" -o /tmp/foundry.tar.gz \
    && echo "${FOUNDRY_TARBALL_SHA256}  /tmp/foundry.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/foundry.tar.gz -C /usr/local/bin forge cast anvil chisel \
    && rm /tmp/foundry.tar.gz \
    && test "$(/usr/local/bin/forge --version | sed -n '1s/forge Version: //p')" = "1.7.1" \
    && curl -fsSL "https://binaries.soliditylang.org/linux-amd64/solc-linux-amd64-v${SOLC_VERSION}+commit.b61c2a91" -o "/usr/local/bin/solc-${SOLC_VERSION}" \
    && echo "${SOLC_SHA256}  /usr/local/bin/solc-${SOLC_VERSION}" | sha256sum -c - \
    && chmod 0755 "/usr/local/bin/solc-${SOLC_VERSION}" \
    && test "$(/usr/local/bin/solc-${SOLC_VERSION} --version | tail -n 1)" = "Version: 0.8.25+commit.b61c2a91.Linux.g++" \
    && mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/mellow-finance/flexible-vaults.git \
    && git fetch --depth=1 origin 60c462d6b006b19790b07c009b7a48aa3bcb3e96 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "60c462d6b006b19790b07c009b7a48aa3bcb3e96" \
    && test "$(git rev-parse HEAD^{tree})" = "6a5951f96a4e85282fcd53fc3e93954b56e61e8a" \
    && test "$(git rev-list --all --count)" = "1" \
    && git submodule update --init --recursive --depth=1 --jobs=4 \
    && test -z "$(git submodule status --recursive | grep '^[+-U]')" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable rev-parse HEAD)" = "60b305a8f3ff0c7688f02ac470417b6bbf1c4d27" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable/lib/erc4626-tests rev-parse HEAD)" = "8b1d7c2ac248c33c3506b1bff8321758943c5e11" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable/lib/forge-std rev-parse HEAD)" = "1eea5bae12ae557d589f9f0f0edae2faa47cb262" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes rev-parse HEAD)" = "c0d865508c0fee0a11b97732c5e90f9cad6b65a5" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts rev-parse HEAD)" = "e4f70216d759d8e6a64144a9e1f7bbeed78e7079" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/erc4626-tests rev-parse HEAD)" = "8b1d7c2ac248c33c3506b1bff8321758943c5e11" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/forge-std rev-parse HEAD)" = "1eea5bae12ae557d589f9f0f0edae2faa47cb262" \
    && test "$(git -C lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes rev-parse HEAD)" = "c0d865508c0fee0a11b97732c5e90f9cad6b65a5" \
    && /usr/local/bin/forge build --offline --use "/usr/local/bin/solc-${SOLC_VERSION}" --quiet \
    && find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && rm -rf "$AUDIT_DIR/.git/modules" \
    && find "$AUDIT_DIR" -name .gitmodules -type f -print0 | while IFS= read -r -d '' modules_file; do modules_root=$(dirname "$modules_file"); git config -f "$modules_file" --get-regexp '^submodule\..*\.path$' | while read -r _ relative_path; do dependency_dir="$modules_root/$relative_path"; git -C "$dependency_dir" init --quiet; printf '*\n' >"$dependency_dir/.git/info/exclude"; done; done \
    && git remote remove origin \
    && test "$(git rev-parse HEAD)" = "60c462d6b006b19790b07c009b7a48aa3bcb3e96" \
    && test "$(find "$AUDIT_DIR" -mindepth 2 -type d -name .git | wc -l)" = "8" \
    && find "$AUDIT_DIR" -mindepth 2 -type d -name .git -print0 | while IFS= read -r -d '' metadata_dir; do dependency_dir=$(dirname "$metadata_dir"); ! git -C "$dependency_dir" rev-parse --verify HEAD >/dev/null 2>&1; test -z "$(git -C "$dependency_dir" remote)"; test -z "$(find "$metadata_dir/objects" -type f -print -quit)"; done \
    && test -z "$(git status --porcelain)" \
    && test -z "$(find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print -quit)" \
    && test -z "$(git ls-tree -r --name-only HEAD | grep -Ei '\.(pdf|jsonl)$')"

ENV PATH="/usr/local/bin:${PATH}" \
    FOUNDRY_OFFLINE=true \
    FOUNDRY_SOLC=/usr/local/bin/solc-0.8.25

WORKDIR $AGENT_DIR
