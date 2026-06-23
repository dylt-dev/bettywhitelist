#! /usr/bin/env bash

main ()
{
    export SPLUNGE_TEMPLATE_FOLDER='./mycode'
    export SPLUNGE_CODEFOLDER='./mycode'
    export DB_PATH="$(pwd)/db/bwl.db"

    printf '$DB_PATH=%s\n' "$DB_PATH"

    www 1313 ./content
}


(return 0 2>/dev/null) || main "$@"