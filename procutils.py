import subprocess

def shexec(cmd):
    subprocess.call(cmd, shell=True)

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return (stdout, stderr, p.returncode)

def quietrun(cmd):
    (stdout, stderr, ret) = run_cmd(cmd)
    if ret != 0:
        print stdout
        print stderr
