#! /usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "$BASH_SOURCE")")
MAKEFILE="$SCRIPT_DIR/../Makefile"

run-tests()
{
    local tests=(
        test-makefile-exists
        test-fetch-target
        test-deploy-target
        test-prune-target
        test-all-no-package
        test-phony-includes-fetch
        test-phony-includes-prune
        test-deploy-uses-latest-symlink
        test-run-sh-sd-notify
        test-service-type-notify
        test-locals-only-target
        test-stage-release-target
    )
    local total=0 passed=0 failed=0
    for t in "${tests[@]}"; do
        printf '=== %s ===\n' "$t"
        (( total++ ))
        if "$t"; then
            (( passed++ ))
        else
            (( failed++ ))
        fi
    done
    printf '\n%d total, %d passed, %d failed\n' "$total" "$passed" "$failed"
    return "$failed"
}

test-makefile-exists()
{
    [[ -f "$MAKEFILE" ]] || { printf '  FAIL: Makefile not found\n'; return 1; }
    printf '  PASS\n'
}

test-fetch-target()
{
    grep -qP '^fetch:' "$MAKEFILE" || { printf '  FAIL: fetch target not found\n'; return 1; }
    grep -qP 'github-release-download-latest' "$MAKEFILE" || { printf '  FAIL: fetch does not call github-release-download-latest\n'; return 1; }
    grep -qF -e '--verify' "$MAKEFILE" || { printf '  FAIL: fetch missing --verify\n'; return 1; }
    grep -qF -e '--extract' "$MAKEFILE" || { printf '  FAIL: fetch missing --extract\n'; return 1; }
    grep -qP 'ln -sfn' "$MAKEFILE" || { printf '  FAIL: fetch missing symlink creation\n'; return 1; }
    grep -qP '/tmp/bettywhitelist\.latest' "$MAKEFILE" || { printf '  FAIL: fetch missing symlink target\n'; return 1; }
    printf '  PASS\n'
}

test-deploy-target()
{
    grep -qP '^deploy:' "$MAKEFILE" || { printf '  FAIL: deploy target not found\n'; return 1; }
    grep -qP 'SVC_ROOT\)\.old' "$MAKEFILE" || { printf '  FAIL: deploy missing old-dir backup\n'; return 1; }
    grep -qP 'bettywhitelist\.latest' "$MAKEFILE" || { printf '  FAIL: deploy missing symlink reference\n'; return 1; }
    grep -qP 'systemctl restart bettywhitelist' "$MAKEFILE" || { printf '  FAIL: deploy missing service restart\n'; return 1; }
    printf '  PASS\n'
}

test-prune-target()
{
    grep -qP '^prune:' "$MAKEFILE" || { printf '  FAIL: prune target not found\n'; return 1; }
    grep -qP 'SVC_ROOT\)\.old' "$MAKEFILE" || { printf '  FAIL: prune missing old-dir cleanup\n'; return 1; }
    grep -qP '/tmp/bettywhitelist\.release' "$MAKEFILE" || { printf '  FAIL: prune missing temp dir cleanup\n'; return 1; }
    printf '  PASS\n'
}

test-all-no-package()
{
    local all_line
    all_line=$(grep -P '^all:' "$MAKEFILE") || { printf '  FAIL: all target not found\n'; return 1; }
    if echo "$all_line" | grep -qP 'package'; then
        printf '  FAIL: all still depends on package\n'
        return 1
    fi
    echo "$all_line" | grep -qP 'fetch' || { printf '  FAIL: all missing fetch\n'; return 1; }
    echo "$all_line" | grep -qP 'deploy' || { printf '  FAIL: all missing deploy\n'; return 1; }
    printf '  PASS\n'
}

test-phony-includes-fetch()
{
    local phony_line
    phony_line=$(grep -P '^\.PHONY:' "$MAKEFILE") || { printf '  FAIL: .PHONY not found\n'; return 1; }
    echo "$phony_line" | grep -qP 'fetch' || { printf '  FAIL: .PHONY missing fetch\n'; return 1; }
    printf '  PASS\n'
}

test-phony-includes-prune()
{
    local phony_line
    phony_line=$(grep -P '^\.PHONY:' "$MAKEFILE") || { printf '  FAIL: .PHONY not found\n'; return 1; }
    echo "$phony_line" | grep -qP 'prune' || { printf '  FAIL: .PHONY missing prune\n'; return 1; }
    printf '  PASS\n'
}

test-deploy-uses-latest-symlink()
{
    grep -qP 'latest' "$MAKEFILE" || { printf '  FAIL: deploy does not use /tmp/bettywhitelist.latest\n'; return 1; }
    printf '  PASS\n'
}

test-run-sh-sd-notify()
{
    local run_sh="$SCRIPT_DIR/../svc/run.sh"
    grep -qF -e '--sd-notify' "$run_sh" || { printf '  FAIL: run.sh missing --sd-notify\n'; return 1; }
    printf '  PASS\n'
}

test-service-type-notify()
{
    local svc="$SCRIPT_DIR/../svc/bettywhitelist.service"
    grep -qP '^Type=notify\b' "$svc" || { printf '  FAIL: service file not Type=notify\n'; return 1; }
    grep -qP '^TimeoutStartSec=' "$svc" || { printf '  FAIL: service file missing TimeoutStartSec\n'; return 1; }
    printf '  PASS\n'
}

test-locals-only-target()
{
    grep -qP '^locals-only:' "$MAKEFILE" || { printf '  FAIL: locals-only target not found\n'; return 1; }
    grep -qP 'stage-release' "$MAKEFILE" || { printf '  FAIL: locals-only missing stage-release\n'; return 1; }
    printf '  PASS\n'
}

test-stage-release-target()
{
    grep -qP '^stage-release:' "$MAKEFILE" || { printf '  FAIL: stage-release target not found\n'; return 1; }
    grep -qP '/tmp/bettywhitelist\.latest/extracted' "$MAKEFILE" || { printf '  FAIL: stage-release missing release folder path\n'; return 1; }
    printf '  PASS\n'
}

main()
{
    if (( $# >= 1 )); then
        local cmd=$1; shift
        case "$cmd" in
            run-tests)                            run-tests;;
            test-makefile-exists)                 test-makefile-exists;;
            test-fetch-target)                    test-fetch-target;;
            test-deploy-target)                   test-deploy-target;;
            test-prune-target)                    test-prune-target;;
            test-all-no-package)                  test-all-no-package;;
            test-phony-includes-fetch)            test-phony-includes-fetch;;
            test-phony-includes-prune)            test-phony-includes-prune;;
            test-deploy-uses-latest-symlink)      test-deploy-uses-latest-symlink;;
            test-run-sh-sd-notify)                test-run-sh-sd-notify;;
            test-service-type-notify)             test-service-type-notify;;
            test-locals-only-target)              test-locals-only-target;;
            test-stage-release-target)            test-stage-release-target;;
            *)                                    printf 'Unknown test: %s\n' "$cmd" >&2; exit 1;;
        esac
    else
        run-tests
    fi
}

if ! (return 0 2>/dev/null); then
    main "$@"
fi
