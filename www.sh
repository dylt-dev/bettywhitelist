#! /usr/bin/env bash

export SPLUNGE_TEMPLATE_FOLDER='./code'

main ()
{
    www 1313 ./content
}


(return 0 2>/dev/null) || main "$@"