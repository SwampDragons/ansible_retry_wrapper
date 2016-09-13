#!/usr/bin/env python
# encoding: utf-8

"""
If some hosts fail in the initial playbook run, retry before giving up.
"""

import sys
import subprocess

MAX_TRIES = 3


def run_cmd(cmd):
    """Run ansible command and stream stdout and stderr back to terminal."""
    cmd_plus = ("export ANSIBLE_FORCE_COLOR=true; " +
                "export PYTHONUNBUFFERED=1; " + cmd)
    proc = subprocess.Popen(cmd_plus,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    retry_line = ""
    while True:
        out = proc.stdout.readline()
        if out == '' and proc.poll() is not None:
            break
        if out:
            if "retry" in out and "--limit" in out:
                retry_line = out
            print(out.strip())
    return retry_line


def try_ansible(ansible_cmd):
    """Wrap ansible command in retry logic."""
    tries = 0
    retry_suffix = ''
    success = False
    while tries < MAX_TRIES:
        tries += 1
        print "running %s (Try # %s)" % (ansible_cmd + " " + retry_suffix,
                                         tries)
        retry_line = run_cmd(ansible_cmd + " " + retry_suffix)
        print retry_line
        if not retry_line:
            print "successfully ran ansible command: %s in %s tries" % (ansible_cmd, tries)
            success = True
            return success
        retry_suffix = retry_line.split("to retry, use: ")[1].strip()

    print("ERROR: Still had failed hosts even after three tries")
    return success


if __name__ == "__main__":
    success = try_ansible(' '.join(sys.argv[1:]))
    if not success:
        sys.exit(1)
