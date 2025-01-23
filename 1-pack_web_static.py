#!/usr/bin/python3
"""Module level doc"""
from fabric.api import local
from datetime import datetime
import tarfile


def do_pack():
    """function level docs"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive = f"web_static_{time}.tgz"
    print(f"Packing web_static to {archive}")
    if local(f"tar -cvzf {archive} web_static/", capture=True).failed:
        return None
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            print(member.name)
    return archive
