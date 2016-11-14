#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import subprocess


def convert(path):
    cmd = ['perl', 'formater.perl', path]
    r = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    result = r.stdout.read()
    print result
    print "*" * 100
    with open(path, 'w') as f:
        f.write(result)


def main(dir_name):
    for root, dirs, files in os.walk(dir_name):
        for f in files:
            if f.endswith('.lua'):
                print "-" * 100
                f = os.path.join(root, f)
                convert(f)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) > 1:
        if os.path.isdir(argv[1]):
            main(argv[1])
        elif os.path.isfile(argv[1]):
            convert(argv[1])
        else:
            raise Exception('\n%s is not valid file or dir path;\nUsage: python %s path_to_file||path_to_dir' % (argv[1], argv[0]))
    else:
        main('.')
