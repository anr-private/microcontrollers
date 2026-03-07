# PUSH_ALL_to_pico.sh

#!/bin/bash
#
# PUSH_PAGES_to_pico.sh


#--- copy the  stuff to the Pico ---
copy_release_files_to_the_pico() {
    #echo 'Make subdir :pages/ on pico'
    #mpremote fs mkdir :pages

    #echo 'Copy contents of pages/ '
    #mpremote fs cp -r pages   :
    
    #echo 'Remove the client files we do not need'
    #mpremote fs rm http/AnrHttpClient.py

    mpremote fs cp process_htmlp_file.py :
    mpremote fs cp one-line.htmlp :



}

list_pico_filesystem_contents() {
    echo ' '
    echo 'LIST THE PICO CONTENTS: ROOT DIR'
    mpremote fs ls 
    #echo ' '    
    #echo 'LIST THE PICO CONTENTS: /pages'
    #mpremote fs ls /pages
}


main() {
    echo "PUSH_ALL_to_pico -- MAIN"
    copy_release_files_to_the_pico
    list_pico_filesystem_contents
}

main $*


###
