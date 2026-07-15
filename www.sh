#! /usr/bin/env bash

main ()
{
    export DB_PATH="$(pwd)/db/bwl.db"
    printf '$DB_PATH=%s\n' "$DB_PATH"

    www --port 1313 --code-folder ./content/mycode --templates-folder ./content/mycode
}


(return 0 2>/dev/null) || main "$@"