FROM pranay5255/yudaii_evmbench@sha256:745a1f8d9c49a855f02d0a7254e902f139f4d385a889d1815d699ab05c16c1a0

RUN mkdir -p "$AUDIT_DIR" \
    && cd "$AUDIT_DIR" \
    && git init \
    && git remote add origin https://github.com/recallnet/contracts.git \
    && git fetch --depth=1 origin 5a6710409a90944ceb3ff4d8ad9edea1b00557c3 \
    && git checkout --detach FETCH_HEAD \
    && test "$(git rev-parse HEAD)" = "5a6710409a90944ceb3ff4d8ad9edea1b00557c3" \
    && test "$(git rev-list --all --count)" = "1" \
    && git submodule update --init --recursive --depth=1 --jobs=4 \
    && test -z "$(git submodule status --recursive | grep '^[+-U]')" \
    && forge build --quiet --remappings 'solidity-cborutils/=lib/filecoin-solidity/lib/solidity-cborutils/' \
    && forge test --match-path test/ValidatorRewarder.t.sol --remappings 'solidity-cborutils/=lib/filecoin-solidity/lib/solidity-cborutils/' \
    && find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -delete \
    && find "$AUDIT_DIR" -mindepth 2 -name .git -prune -exec rm -rf {} + \
    && rm -rf "$AUDIT_DIR/.git/modules" \
    && find "$AUDIT_DIR" -name .gitmodules -type f -print0 | while IFS= read -r -d '' modules_file; do modules_root=$(dirname "$modules_file"); git config -f "$modules_file" --get-regexp '^submodule\..*\.path$' | while read -r _ relative_path; do dependency_dir="$modules_root/$relative_path"; git -C "$dependency_dir" init --quiet; printf '*\n' >"$dependency_dir/.git/info/exclude"; done; done \
    && git remote remove origin \
    && test "$(git rev-parse HEAD)" = "5a6710409a90944ceb3ff4d8ad9edea1b00557c3" \
    && test "$(git rev-list --all --count)" = "1" \
    && test "$(find "$AUDIT_DIR" -mindepth 2 -type d -name .git | wc -l)" = "31" \
    && find "$AUDIT_DIR" -mindepth 2 -type d -name .git -print0 | while IFS= read -r -d '' metadata_dir; do dependency_dir=$(dirname "$metadata_dir"); ! git -C "$dependency_dir" rev-parse --verify HEAD >/dev/null 2>&1; test -z "$(git -C "$dependency_dir" remote)"; test -z "$(find "$metadata_dir/objects" -type f -print -quit)"; done \
    && test -z "$(git status --porcelain)" \
    && test -z "$(find "$AUDIT_DIR" -type f \( -iname '*.pdf' -o -iname '*.jsonl' \) -print -quit)"

ENV FOUNDRY_OFFLINE=true

WORKDIR $AGENT_DIR
