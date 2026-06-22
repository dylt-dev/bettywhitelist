#! /usr/bin/env bash


main ()
{
    # shellcheck disable=SC2016
    (( $# == 1 )) || { printf 'Usage: \n' >&2; return 1; }
    local dbPath=$1
    # shellcheck disable=SC2016
    [[ -f "$dbPath" ]] || { printf 'Non-existent path: $dbPath\n' >&2; return 1; }
    local schemaPath='../db/bwl.db.schema'
    # shellcheck disable=SC2016
    [[ -f "$schemaPath" ]] || { printf 'Non-existent path: $schemaPath\n' >&2; return 1; }
    command -v "sqlite3" >/dev/null || { printf '%s is required, but was not found.\n' "sqlite3" >&2; return 255; }
}

# Don't run main if the script has been sourced
(return 0 2>/dev/null) || main "$@"
