#!/usr/bin/env python

import sys
import ast
import subprocess
import shlex
import time

# pairs of extensions and commands can be added here
exec_dict = { 
        "pbs"   : "qsub", 
        "slurm" : "sbatch",
}

if (__name__ == "__main__"):
    try:
        # all required
        tag_g = sys.argv[1]
        nrank_list_g = ast.literal_eval(sys.argv[2])
        ncpu_list_g = ast.literal_eval(sys.argv[3])
        ext_g = sys.argv[4]
    except IndexError:
        print("Usage: ./resmanrun.py <tag> <nrank_list> <ncpu_list> <ext>"
                "\n        <tag>:        an identifier for this set of jobs"
                "\n        <nrank list>: a quoted Python list of numbers of ranks to use, "
                "\n                      e.g. \"[1,2,4,8]\""
                "\n        <ncpu list>:  a quoted Python list of numbers of cpus per rank to use, "
                "\n                      e.g. \"[1,2,4,8]\""
                "\n        <ext>:        the desired extension of the resulting file; "
                "\n                      template must have extension \"<ext>plate\"")
        sys.exit(1)

if ext_g not in exec_dict:
    print("resmanrun: invalid extension, can't start jobs, "
            "\n           use pbs or slurm as <ext>")
    sys.exit(1)

def run(nrank_list_, ncpu_list_, tag_, ext_):
    for nrank_ in nrank_list_:
        for ncpu_ in ncpu_list_:
            run_name = "{0}{1:03d}r{2:02d}c".format(  \
                       tag_, nrank_, ncpu_)
            status = subprocess.call("mkdir -p ./out/" + run_name, shell=True)
            status = subprocess.call("mkdir -p ./out/" + run_name, shell=True)
            str = exec_dict[ext_g] + " " + run_name + "." + ext_g
            args = shlex.split(str)
            p = subprocess.Popen(args)
            p.wait()
            if (p.poll() != 0):
                print("resmanrun: could not run command: \"" + str + "\"")
                sys.exit(1)

run(nrank_list_g, ncpu_list_g, tag_g, ext_g)
time.sleep(0.1)

