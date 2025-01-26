#!/usr/bin/python3
"""Contains function do_pack"""
from fabric.api import local
from datetime import datetime
import os.path


def do_pack():
    """Generates a .tgz from contents of web_static"""
    if local("mkdir -p versions").failed:
        return None

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"

    if local(f"tar -czvf {archive_path} web_static").succeeded:
        return archive_path
    else:
        None
