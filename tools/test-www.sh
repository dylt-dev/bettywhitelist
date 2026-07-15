#! /usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "$BASH_SOURCE")")
PROJECT_DIR="$SCRIPT_DIR/.."

command -v bwrap >/dev/null || { printf 'bwrap not installed\n' >&2; exit 1; }
command -v gunicorn >/dev/null || {
    printf 'gunicorn not found. Activate a venv with splunge and bettywhitelist installed:\n' >&2
    printf '  bash create-venv.sh && source venv/bin/activate\n' >&2
    exit 1
}

WWW=$(command -v www 2>/dev/null || printf '%s' "$PROJECT_DIR/../splunge/scripts/www")
[[ -f "$WWW" ]] || { printf 'www not found\n' >&2; exit 1; }


# Pre-flight: check if network namespace + loopback is supported
check_net_ns()
{
    bwrap --unshare-net --cap-add all --bind / / --proc /proc \
        bash -c 'ip link set lo up' 2>/dev/null
}


HAS_NET_NS=false
check_net_ns && HAS_NET_NS=true


ns()
{
    if ! $HAS_NET_NS; then
        printf '  SKIP (no network namespace support)\n'
        return 0
    fi
    bwrap --unshare-net --cap-add all --bind / / --proc /proc --dev /dev \
        --chdir "$PROJECT_DIR" \
        bash -e -o pipefail -c "$1"
}


test-serve-list-has-sun()
{
    ns '
        [[ -f venv/bin/activate ]] && source venv/bin/activate
        trap "kill 0" EXIT
        www --port 80 --code-folder "$PWD/content" --templates-folder "$PWD/mycode" &
        sleep 2
        curl -s http://localhost/list | grep 🌞
    ' && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-serve-list-200()
{
    ns '
        [[ -f venv/bin/activate ]] && source venv/bin/activate
        trap "kill 0" EXIT
        www --port 80 --code-folder "$PWD/content" --templates-folder "$PWD/mycode" &
        sleep 2
        code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/list)
        [[ "$code" == "200" ]]
    ' && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-config-splunge-env()
{
    ns '
        [[ -f venv/bin/activate ]] && source venv/bin/activate
        trap "kill 0" EXIT
        www &
        sleep 2
        curl -s http://localhost/list | grep 🌞
    ' && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-serve-uds()
{
    ns '
        [[ -f venv/bin/activate ]] && source venv/bin/activate
        trap "kill 0" EXIT
        www --socket "$PWD/tmp/bwl-test.sock" --code-folder "$PWD/content" --templates-folder "$PWD/mycode" &
        sleep 2
        code=$(curl -s -o /dev/null -w "%{http_code}" --unix-socket "$PWD/tmp/bwl-test.sock" http://localhost/list)
        [[ "$code" == "200" ]]
    ' && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-thankyou()
{
    ns '
        [[ -f venv/bin/activate ]] && source venv/bin/activate
        trap "kill 0" EXIT
        www --port 80 --code-folder "$PWD/content" --templates-folder "$PWD/mycode" &
        sleep 2
        curl -s "http://localhost/thankyou?name=test&token=fake" | grep 🌞
    ' && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


all()
{
    local tests=(
        test-serve-list-has-sun
        test-serve-list-200
        test-config-splunge-env
        test-serve-uds
        test-thankyou
    )
    local total=${#tests[@]} passed=0 failed=0
    for t in "${tests[@]}"; do
        printf 'Test: %s\n' "$t"
        if "$t"; then (( passed++ )); else (( failed++ )); fi
    done
    printf '\n%d passed, %d failed, %d total\n' "$passed" "$failed" "$total"
    return "$failed"
}


main()
{
    case ${1:-all} in
        all|"")                                   all;;
        test-serve-list-has-sun)                  test-serve-list-has-sun "$@";;
        test-serve-list-200)                      test-serve-list-200 "$@";;
        test-config-splunge-env)                  test-config-splunge-env "$@";;
        test-serve-uds)                           test-serve-uds "$@";;
        test-thankyou)                            test-thankyou "$@";;
        *)                                 printf 'Unknown test: %s\n' "$1" >&2; exit 1 ;;
    esac
}


if ! (return 0 2>/dev/null); then
    main "$@"
fi
