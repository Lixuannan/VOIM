#!/usr/bin/env python3

import sys
import os
import webbrowser
import subprocess


def compile(filename: str, compiler: str) -> int:
    pro = subprocess.Popen(f"{compiler} -Wextra -o {filename}.out {filename}".split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    exit_code = pro.returncode
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}\n")


def run(cmd):
    pro = subprocess.Popen(cmd.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    exit_code = pro.returncode
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}")
    print(f"Process ended with code: {exit_code}")


filename = sys.argv[1]
filetype = filename.split('.')[-1]


if filetype == 'cpp' or filetype == 'cc':
    compile(filename, "g++")
    run(f"./{filename}.out")
elif filetype == 'py':
    run(f"python {filename}")
elif filetype == 'c':
    compile(filename, "gcc")
    run(f"./{filename}.out")
elif filetype == 'md':
    run(f"pandoc -f markdown -t html5 --css /home/codingcowlee/github.css -s -o {filename}.html {filename}")
    webbrowser.open(f"{filename}.html")



