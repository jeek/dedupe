#!/bin/env python

import os
import hashlib
import argparse


# http://pythoncentral.io/hashing-files-with-python/
def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Hardlink duplicate files')
    parser.add_argument('--minsize',
        default=1048576 * 20,
        type=int,
        help="minimum file size to evaluate")
    parser.add_argument('--hashlib',
        default='sha256',
        help="hashing algorithm to use")
    parser.add_argument('path',
        default=os.getcwd(),
        nargs='?',
        help="path to start from")
    args = parser.parse_args()
    minsize = vars(args)['minsize']
    print((vars(args), minsize))

    # Ensure the specified hashing algorithm exists
    if vars(args)['hashlib'] not in hashlib.algorithms_available:
        print(("Unsupported hashing algorithm: " + vars(args)['hashlib']))
        os._exit(os.EX_USAGE)

    sizes = dict()
    for root, dir, files in os.walk(vars(args)['path']):
        for i in files:
            current = root + '/' + i
            filesize = -1
            try:
                filesize = os.stat(current).st_size
            except OSError as e:
                filesize = -1
                print(e)
                pass

            if filesize >= vars(args)['minsize']:
                if filesize not in sizes:
                    sizes[filesize] = []
                sizes[filesize].append(current)
    hashes = dict()
    for currentsize in sizes:
        if len(sizes[currentsize]) > 1:
            i = 0
            while i < len(sizes[currentsize]):
                if sizes[currentsize][i] not in hashes:
                    hashes[sizes[currentsize][i]] = \
                      hashfile(open(sizes[currentsize][i], 'rb'),
                        hashlib.new(vars(args)['hashlib']))
                j = i + 1
                while j < len(sizes[currentsize]):
                    if sizes[currentsize][j] not in hashes:
                        hashes[sizes[currentsize][j]] = \
                          hashfile(open(sizes[currentsize][j], 'rb'),
                            hashlib.new(vars(args)['hashlib']))
                    if hashes[sizes[currentsize][i]] == \
                      hashes[sizes[currentsize][j]]:
                        ok_to_link = True
                        try:
                            ok_to_link = False
                            os.remove(sizes[currentsize][j])
                            ok_to_link = True
                        except OSError as e:
                            print((e, sizes[currentsize][i], '->',
                              sizes[currentsize][j]))
                            pass
                        if ok_to_link:
                            os.link(sizes[currentsize][i],
                              sizes[currentsize][j])
                            print((sizes[currentsize][i], '->',
                              sizes[currentsize][j]))
                            sizes[currentsize].pop(j)
                        else:
                            j += 1
                i += 1
