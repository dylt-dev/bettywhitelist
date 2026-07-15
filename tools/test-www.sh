#! /usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "$BASH_SOURCE")")
PROJECT_DIR="$SCRIPT_DIR/.."

command -v gunicorn >/dev/null || {
    printf 'gunicorn not found. Activate a venv with splunge and bettywhitelist installed:\n' >&2
    printf '  bash create-venv.sh && source venv/bin/activate\n' >&2
    exit 1
}

WWW=$(printf '%s' "$PROJECT_DIR/../splunge/scripts/www")
[[ -f "$WWW" ]] || { printf 'www not found\n' >&2; exit 1; }


cleanup()
{
    local pid=$1
    kill "$pid" 2>/dev/null
    timeout 3 wait "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null
}


start_www()
{
    local port=$1
    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    "$WWW" --port "$port" --code-folder "$PROJECT_DIR/content" \
           --templates-folder "$PROJECT_DIR/mycode" &
    local pid=$!
    sleep 3
    printf '%s' "$pid"
}


start_www_socket()
{
    local sock=$1
    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    "$WWW" --socket "$sock" --code-folder "$PROJECT_DIR/content" \
           --templates-folder "$PROJECT_DIR/mycode" &
    local pid=$!
    sleep 3
    printf '%s' "$pid"
}


test-serve-list-has-sun()
{
    local pid
    pid=$(start_www 19871)
    curl -s http://localhost:19871/list | grep 🌞
    local result=$?
    cleanup "$pid"
    [[ "$result" -eq 0 ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-serve-list-200()
{
    local pid
    pid=$(start_www 19872)
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:19872/list)
    cleanup "$pid"
    [[ "$code" == "200" ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-config-splunge-env()
{
    local tmpDir; tmpDir=$(mktemp -d)
    pushd "$tmpDir" >/dev/null || return 1

    cat > .splunge.env <<EOF
SPLUNGE_SOCKET=$tmpDir/test-bwl.sock
SPLUNGE_CODEFOLDER=$PROJECT_DIR/content
SPLUNGE_TEMPLATES_FOLDER=$PROJECT_DIR/mycode
EOF

    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    "$WWW" &
    local pid=$!
    sleep 3

    curl -s --unix-socket "$tmpDir/test-bwl.sock" http://localhost/list | grep 🌞
    local result=$?
    cleanup "$pid"
    popd >/dev/null
    [[ "$result" -eq 0 ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-serve-uds()
{
    local sock="/tmp/bwl-test-$$.sock"
    local pid
    pid=$(start_www_socket "$sock")
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" --unix-socket "$sock" http://localhost/list)
    cleanup "$pid"
    rm -f "$sock"
    [[ "$code" == "200" ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-thankyou()
{
    local pid
    pid=$(start_www 19873)
    curl -s "http://localhost:19873/thankyou?name=test&token=fake" | grep 🌞
    local result=$?
    cleanup "$pid"
    [[ "$result" -eq 0 ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
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
