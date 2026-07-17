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

cd "$PROJECT_DIR" || exit 1


test-serve-list-has-sun()
{
    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    "$WWW" --graceful-timeout 1 --port 19871 --code-folder "$PROJECT_DIR/content/mycode" \
           --template-folder "$PROJECT_DIR/content/mycode" &
    until curl -s -w '%{http_code}' --output /tmp/_bwl_poll.txt http://localhost:19871/list | grep -q '^[2-5]'; do sleep 1; done

    curl -s http://localhost:19871/list | grep 🌞
    local result=$?
    local jp; jp=$(jobs -p); [[ -n "$jp" ]] && kill $jp; wait
    [[ "$result" -eq 0 ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-serve-list-200()
{
    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    "$WWW" --graceful-timeout 1 --port 19872 --code-folder $PROJECT_DIR/content/mycode \
           --template-folder $PROJECT_DIR/content/mycode &
    until curl -s -w '%{http_code}' --output /tmp/_bwl_poll.txt http://localhost:19872/list | grep -q '^[2-5]'; do sleep 1; done

    local code
    code=$(curl -s -w "%{http_code}" -o /tmp/_bwl_test_body.txt http://localhost:19872/list)
    local jp; jp=$(jobs -p); [[ -n "$jp" ]] && kill $jp; wait
    [[ "$code" == "200" ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-config-splunge-env()
{
    local tmpDir; tmpDir=$(mktemp -d)
    pushd "$tmpDir" >/dev/null || return 1

    cat > .splunge.env <<EOF
SPLUNGE_SOCKET=$tmpDir/test-bwl.sock
SPLUNGE_CODEFOLDER=$PROJECT_DIR/content/mycode
SPLUNGE_TEMPLATE_FOLDER=$PROJECT_DIR/content/mycode
EOF

    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    "$WWW" --graceful-timeout 1 &
    local i
    for i in {1..10}; do
        [[ -S "$tmpDir/test-bwl.sock" ]] && curl -s --unix-socket "$tmpDir/test-bwl.sock" http://localhost/list 2>/dev/null && break
        sleep 1
    done

    curl -s --unix-socket "$tmpDir/test-bwl.sock" http://localhost/list | grep 🌞
    local result=$?
    local jp; jp=$(jobs -p); [[ -n "$jp" ]] && kill $jp; wait
    popd >/dev/null
    [[ "$result" -eq 0 ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-serve-uds()
{
    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    local sock="/tmp/bwl-test-$$.sock"
    "$WWW" --graceful-timeout 1 --socket "$sock" --code-folder $PROJECT_DIR/content/mycode \
           --template-folder $PROJECT_DIR/content/mycode &
    until curl -s -w '%{http_code}' --output /tmp/_bwl_poll.txt --unix-socket "$sock" http://localhost/list | grep -q '^[2-5]'; do sleep 1; done

    local code
    code=$(curl -s -w "%{http_code}" -o /tmp/_bwl_test_body.txt --unix-socket "$sock" http://localhost/list)
    local jp; jp=$(jobs -p); [[ -n "$jp" ]] && kill $jp; wait
    rm -f "$sock"
    [[ "$code" == "200" ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
}


test-thankyou()
{
    export DB_PATH="$PROJECT_DIR/db/bwl.db"
    "$WWW" --graceful-timeout 1 --port 19873 --code-folder $PROJECT_DIR/content/mycode \
           --template-folder $PROJECT_DIR/content/mycode &
    until curl -s -w '%{http_code}' --output /tmp/_bwl_poll.txt http://localhost:19873/list | grep -q '^[2-5]'; do sleep 1; done

    local code
    code=$(curl -s -w "%{http_code}" -o /tmp/_bwl_test_body.txt \
        "http://localhost:19873/thankyou?name=test&token=fake")
    local jp; jp=$(jobs -p); [[ -n "$jp" ]] && kill $jp; wait
    [[ "$code" == "200" ]] && { printf '  PASS\n'; return 0; } || { printf '  FAIL\n'; return 1; }
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
