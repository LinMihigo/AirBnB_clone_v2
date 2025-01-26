#!/usr/bin/python3
"""
deletes out-of-date archives using do_clean

Attributes:
    env.hosts (list): holds web server ip addresses
"""
from fabric.api import env, local, run

env.hosts = ['100.25.41.202', '100.25.205.60']


def do_clean(number=0):
    """Delete outdated archives locally and remotely."""
    number = 1 if int(number) < 1 else int(number)

    local((
        "ls -t versions/web_static_*.tgz | "
        f"tail -n +{number + 1} | "
        "xargs -r rm -f"
    ), capture=False)

    run((
        "cd /data/web_static/releases && "
        "ls -t | grep web_static_ | "
        f"tail -n +{number + 1} | "
        "xargs -r rm -rf"
    ))
