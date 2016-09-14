#!/usr/bin/env python
# encoding: utf-8

"""
If some hosts fail in the initial playbook run, retry before giving up.
"""

import argparse
import sys
import subprocess

MAX_TRIES_DEFAULT = 3


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


def try_ansible(ansible_cmd, max_tries=MAX_TRIES_DEFAULT):
    """Wrap ansible command in retry logic."""
    tries = 0
    retry_suffix = ''
    success = False
    while tries < max_tries:
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


def parse():
    """Read command line input."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_tries", default=MAX_TRIES_DEFAULT)
    parser.add_argument("ansible_cmd", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse()
    success = try_ansible(' '.join(args.ansible_cmd), args.max_tries)
    if not success:
        sys.exit(1)
