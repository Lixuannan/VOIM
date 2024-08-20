#!/usr/bin/env python3

import sys
import os
import subprocess
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


C_COMPILER = "gcc"
CPP_COMPILER = "g++"
PYTHON_INTERPRETER = "python"
C_ARGV = "-Wextra -g"
CPP_ARGV = "-Wextra -g"


try:
    with open(os.path.join(os.environ["HOME"], ".VOIM.conf"), "rt") as f:
        exec(f.read())
except FileNotFoundError:
    print("\033[1;33mConfig file not found, using default config\033[m")


def compile(filename: str, outfile: str, compiler: str, argv: str) -> int:
    pro = subprocess.Popen(f"{compiler} {argv} -o {outfile} {filename}".split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    exit_code = pro.returncode
    
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}\n")
    
    return exit_code


def run(cmd):
    start_cpu_time = time.process_time()
    start_real_time = time.time()
    pro = subprocess.Popen(cmd.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    end_cpu_time = time.process_time()
    end_real_time = time.time()
    exit_code = pro.returncode
    
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}")
    print(f"\033[1;37mProcess ended with code {exit_code}, real time: {round(end_real_time - start_real_time, 6)}s, cpu time: {round(end_cpu_time - start_cpu_time, 6)}s\033[m")


def judge(cmd, time_limit, filename, input_, output):
    with open(f"{filename}.in", "wt") as f:
        f.write(input_)
    with open(f"{filename}.ans", "wt") as f:
        f.write(output)
    
    cmd += f" < {filename}.in > {filename}.out"
    start_time = time.process_time()
    exit_code = os.system(cmd)
    end_time = time.process_time()

    if exit_code:
        print(f"\033[1;35mRuntime Error, exit code: {exit_code}\033[m")
        return

    diff = ""
    for i in os.popen(f"diff -ZB {filename}.out {filename}.ans"):
        diff += i

    if end_time - start_time > time_limit:
        print("\033[1;33mTime Limit Exceeded\033[0m")
    elif diff != "":
        print(f"\033[1;31mWrong Answer, differences are bellow:\n{diff}\033[m")
    else:
        print("\033[1;32mAccept\033[0m")



class CPHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, data_path: str, **kwargs):
        self.data_path = data_path
        super().__init__(*args, **kwargs)

    def do_POST(self):
        data_len = int(self.headers.get('content-length', 0))
        
        with open(self.data_path, "wb") as f:
            f.write(self.rfile.read(data_len))
        
        self.send_response(200)
        self.end_headers()
        threading.Thread(target=self.server.shutdown).start()



class CPServer(HTTPServer):
    def __init__(self, server_address, RequestHandler, data_path: str):
        self.data_path = data_path
        super().__init__(server_address, RequestHandler)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, data_path=self.data_path)


def get_data(data_path: str):
    http_server = CPServer(("0.0.0.0", 27121), CPHandler, data_path)
    http_server.serve_forever()


print("Checking for update")
os.rename(path, path + ".bak")
process = subprocess.Popen(f"curl https://raw.githubusercontent.com/Lixuannan/VOIM/main/lib/VOIM.py -o {path}".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()
returncode = process.returncode
if returncode:
    print("Download failed, rolling back, please don't close this window")
    os.rename(path + ".bak", path)
    print("Done with rollback")
else:
    print("Success")

work_type = sys.argv[1]
filename = sys.argv[2]
filetype = filename.split('.')[-1]
filebase = list(filename)

while filebase[-1] != '.':
    filebase.pop(-1)

filebase.pop(-1)
filebase = "".join(filebase)


if work_type == "runcode":
    if filetype == 'cpp' or filetype == 'cc':
        returncode = compile(filename, filebase, CPP_COMPILER, CPP_ARGV)
        if returncode != 0:
            print("\033[1;31mCompile Error, won't run\033[m")
        else:
            run(os.path.join('./', filebase))
    elif filetype == 'py':
        run(f"{PYTHON_INTERPRETER} {filename}")
    elif filetype == 'c':
        returncode = compile(filename, filebase, C_COMPILER, C_ARGV)
        if returncode != 0:
            print("\033[1;31mCompile Error, won't run\033[m")
        else:
            run(os.path.join('./', filebase))
    else:
        print("\033[1;31mUnsupport filetype detected, run failed\033[m")
        exit(0)
elif work_type == "judgecode":
    if not os.path.exists(f"{filename}.data"):
        print("\033[1;37mData not found, now you can open your browser and click the Competitive Companion in order to get some data.\033[m")
        get_data(f"{filename}.data")

    if filetype == 'cpp' or filetype == 'cc':
        returncode = compile(filename, filebase, CPP_COMPILER, CPP_ARGV)
        if returncode != 0:
            print("\033[1;31mCompile Error, won't run\033[m")
            exit(0)
    elif filetype == 'c':
        returncode = compile(filename, filebase, C_COMPILER, C_ARGV)
        if returncode != 0:
            print("\033[1;31mCompile Error, won't run\033[m")
            exit(0)
    else:
        print("\033[1;31mUnsupport filetype detected, run failed\033[m")
        exit(0)

    data = json.load(open(f"{filename}.data", "rt"))
    for i in range(len(data["tests"])):
        print(f"Case {i + 1}: ", end="")
        if filetype == "cpp" or filetype == "cc" or filetype == "c":
            judge(os.path.join('./', filebase), data["timeLimit"] / 1000, filename, data['tests'][i]['input'], data['tests'][i]['output'])
        elif filetype == 'python':
            judge(f"{PYTHON_INTERPRETER} {filename}", data["timeLimit"] / 1000, filename, data['tests'][i]['input'], data['tests'][i]['output'])
        else:
            print("\033[1;31mUnsupport filetype detected, run failed\033[m")
            exit(0)



