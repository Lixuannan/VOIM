python3 << EOF
import os
import os.path
import subprocess


path = os.path.join(os.environ["HOME"], ".VOIM.py")
try:
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
except FileNotFoundError:
    print("Start downloading reqirements")
    process = subprocess.Popen(f"curl https://raw.githubusercontent.com/Lixuannan/VOIM/main/lib/VOIM.py -o {path}".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    returncode = process.returncode

    if returncode:
        print("Download failed, missing reqirement, please try again later")
    else:
        print("Success")
for _ in os.popen(f"chmod 777 {path}"):
    ...
EOF

:command -nargs=1 RunCode !~/.VOIM.py runcode <q-args>
:command -nargs=1 JudgeCode !~/.VOIM.py judgecode <q-args>

