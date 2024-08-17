#!/usr/bin/env python3

import sys
import os
import subprocess


def compile(filename: str, compiler: str) -> int:
    pro = subprocess.Popen(f"{compiler} -Wextra -o {filename}.out {filename}".split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    exit_code = pro.returncode
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}\n")
    return exit_code


def run(cmd):
    pro = subprocess.Popen(cmd.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    exit_code = pro.returncode
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}")
    print(f"Process ended with code {exit_code}")


filename = sys.argv[1]
filetype = filename.split('.')[-1]


if filetype == 'cpp' or filetype == 'cc':
    returncode = compile(filename, "g++")
    if returncode != 0:
        print("Compile Error, won't run")
    else:
        run(f"./{filename}.out")
elif filetype == 'py':
    run(f"python {filename}")
elif filetype == 'c':
    returncode = compile(filename, 'cc')
    if returncode != 0:
        print("Compile Error, code will not run")
    else:
        run(f"./{filename}.out")
else:
    print("Unsupport filetype detected, run failed")


