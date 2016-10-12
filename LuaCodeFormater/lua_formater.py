#!/usr/bin/env python
# encoding: utf-8

import os
import subprocess


def convert(path):
    cmd = ['perl', 'formater.perl', path]
    r = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    result = r.stdout.read()
    print result
    print "*" * 100
    with open(path, 'w') as f:
        f.write(result)


def main():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.lua'):
                print "-" * 100
                f = os.path.join(root, f)
                convert(f)


if __name__ == "__main__":
    main()
