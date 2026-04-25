import subprocess

cmd = "ping -c 1 " + user_input

# ruleid: py.command-injection.subprocess-shell-true
subprocess.run(cmd, shell=True)

# ok: py.command-injection.subprocess-shell-true
subprocess.run(["ping", "-c", "1", "8.8.8.8"])
