#!/usr/bin/env python

import sys
import ast

if (__name__ == "__main__"):
    try:
        # required
        tag_ = sys.argv[1]
        nrank_list_ = ast.literal_eval(sys.argv[2])
        ncpu_list_ = ast.literal_eval(sys.argv[3])
        file_ = sys.argv[4]
        ext_ = sys.argv[5]
        # user-defined
        bin_ = sys.argv[6]
        partition_ = sys.argv[7]
    except IndexError:
        print("Usage: ./resmanexpand.py <tag> <nrank_list> <ncpu_list> <file> <ext> <bin> <partition>"
                "\n        <tag>:        an identifier for this set of jobs"
                "\n        <nrank list>: a quoted Python list of numbers of ranks to use, "
                "\n                      e.g. \"[1,2,4,8]\""
                "\n        <ncpu list>:  a quoted Python list of numbers of cpus per rank to use, "
                "\n                      e.g. \"[1,2,4,8]\""
                "\n        <file>:       the path (absolute or relative) to the file to expand, "
                "\n                      without the extension"
                "\n        <ext>:        the desired extension of the resulting file; "
                "\n                      template must have extension \"<ext>plate\""
                "\n        <bin>:        the path to the binary to pass to the scheduler"
                "\n        <partition>:  the partition name to run the job on (machine specific)")
        sys.exit(1)

with open("{0}.{1}plate".format(file_, ext_), "r") as resmanplate:
    resmanstring = resmanplate.read()
    for nrank_ in nrank_list_:
        for ncpu_ in ncpu_list_:
            with open("{0}{1:03d}r{2:02d}c.{3}".format(  \
                      tag_, nrank_, ncpu_, ext_), "w")  \
            as resman:
                resmanfilled = resmanstring.format(
                        bin=bin_,
                        nrank=nrank_,
                        ncpu=ncpu_, 
                        partition=partition_,
                        tag=tag_)
                resman.write(resmanfilled)
       
