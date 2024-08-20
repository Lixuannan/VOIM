python3 << EOF
import os
import os.path
import subprocess


try:
    print("Checking for update")
    with open(os.path.join(os.environ["HOME"], ".VOIM.py"), "rb") as f:
        origin = f.read()
    process = subprocess.Popen("curl http://github.com/lixuannan/VOIM/lib/VOIM.py -o ~/.VOIM.py".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    returncode = process.returncode
    if returncode:
        print("Download failed, rolling back, please don't close this window")
        with open(os.path.join(os.environ["HOME"], ".VOIM.py"), "wb") as f:
            f.write(origin)
        print("Done with rollback")
except FileNotFoundError:
    print("Start downloading reqirements")
    process = subprocess.Popen("curl http://github.com/lixuannan/VOIM/lib/VOIM.py -o ~/.VOIM.py".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    returncode = process.returncode

    if returncode:
        print("Download failed, missing reqirement, please try again later")
EOF

:command -nargs=1 RunCode !~/.VOIM.py runcode <q-args>
:command -nargs=1 JudgeCode !~/.VOIM.py judgecode <q-args>


