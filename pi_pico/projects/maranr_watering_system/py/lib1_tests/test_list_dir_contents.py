# test_list_dir_contents.py
#
# LINEMARKER=TEST_LIST_DIR_CONTENTS_PY
#
# quick test

import os
import sys

from lib1.file_utils import list_dir_contents

def main():
    fpath = ".."
    results = list_dir_contents(fpath)
    print(f"{results=}")


main()

###
