#!/bin/bash
#
# LIST_ALL_on_pico.sh

list_pico_filesystem_contents() {
    echo ' '; echo ' '
    echo '=== ALL DIRS and FILES on the Pico ================'
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote fs ls 
    echo ' '    
    echo 'LIST THE PICO CONTENTS: /displays'
    mpremote fs ls /displays
    ###mpremote fs ls /displays || echo '/displays/ is not found'
    echo 'LIST THE PICO CONTENTS: /http '
    mpremote fs ls /http
    echo 'LIST THE PICO CONTENTS: /lib '
    mpremote fs ls /lib
    echo 'LIST THE PICO CONTENTS: /pages '
    mpremote fs ls /pages
    echo 'LIST THE PICO CONTENTS: /primitives '
    mpremote fs ls /primitives
    echo 'LIST THE PICO CONTENTS: /sensors '
    mpremote fs ls /sensors
}


main() {
    echo "LIST_ALL_on_pico -- MAIN"
    list_pico_filesystem_contents
}

main $*


###
