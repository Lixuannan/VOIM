#!/usr/bin/env python3

import sys
import os
import subprocess
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler



def compile(filename: str, compiler: str) -> int:
    pro = subprocess.Popen(f"{compiler} -Wextra -o {filename}.out {filename}".split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    exit_code = pro.returncode
    
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}\n")
    
    return exit_code


def run(cmd):
    start_time = time.process_time()
    pro = subprocess.Popen(cmd.split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output, error = pro.communicate()
    end_time = time.process_time()
    exit_code = pro.returncode
    
    print(f"{output.decode('utf-8')}\n{error.decode('utf-8')}")
    print(f"\033[1;37mProcess ended with code {exit_code}, cpu time: {end_time - start_time}\033[m")


def judge(cmd, time_limit, filename, input_, output):
    with open(f"{filename}.in", "wt") as f:
        f.write(input_)
    with open(f"{filename}.ans", "wt") as f:
        f.write(output)
    
    cmd += f" < {filename}.in > {filename}.output"
    start_time = time.process_time()
    exit_code = os.system(cmd)
    end_time = time.process_time()

    if exit_code:
        print(f"\033[1;35mRuntime Error, exit code: {exit_code}\033[m")
        return

    diff = ""
    for i in os.popen(f"diff -ZB {filename}.output {filename}.ans"):
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


work_type = sys.argv[1]
filename = sys.argv[2]
filetype = filename.split('.')[-1]


if work_type == "run":
    if filetype == 'cpp' or filetype == 'cc':
        returncode = compile(filename, "g++")
        if returncode != 0:
            print("\033[1;31mCompile Error, won't run\033[m")
        else:
            run(f"./{filename}.out")
    elif filetype == 'py':
        run(f"python {filename}")
    elif filetype == 'c':
        returncode = compile(filename, 'cc')
        if returncode != 0:
            print("\033[1;31mCompile Error, won't run\033[m")
        else:
            run(f"./{filename}.out")
    else:
        print("\033[1;31mCompile Error, won't run\033[m")
elif work_type == "judge":
    if not os.path.exists(f"{filename}.data"):
        print("\033[1;37mData not found, now you can open your browser and click the Competitive Companion in order to get some data.\033[m")
        get_data(f"{filename}.data")

    if filetype == 'cpp' or filetype == 'cc':
        returncode = compile(filename, "g++")
        if returncode != 0:
            print("\033[1;31mCompile Error, won't run\033[m")
            exit(0)
    elif filetype == 'c':
        returncode = compile(filename, 'cc')
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
            judge(f"./{filename}.out", data["timeLimit"] / 1000, filename, data['tests'][i]['input'], data['tests'][i]['output'])
        elif filetype == 'python':
            judge(f"python {filename}", data["timeLimit"] / 1000, filename, data['tests'][i]['input'], data['tests'][i]['output'])
        else:
            print("\033[1;31mUnsupport filetype detected, run failed\033[m")
            exit(0)



