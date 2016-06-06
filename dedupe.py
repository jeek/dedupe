#!/bin/env python

import os
import hashlib

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

if __name__ == "__main__":

    minsize = 1048576 * 20
    
    sizes = dict()
    for root, dir, files in os.walk("."):
        for i in files:
            current = root + '/' + i
            try:
                filesize = os.path.getsize(current)
                if filesize >= minsize:
                    if filesize not in sizes:
                        sizes[filesize] = dict()
                    currenthash = hashfile(open(current, 'rb'), hashlib.sha256())
                    if currenthash not in sizes[filesize]:
                        sizes[filesize][currenthash] = current
                    else:
                        os.remove(current)
                        os.link(sizes[filesize][currenthash], current)
                        print current, '->', sizes[filesize][currenthash]
            except:
                pass
