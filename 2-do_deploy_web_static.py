#!/usr/bin/python3
"""
Fabfile that holds deploy()

Attributes:
    env.hosts (list): holds web server ip addresses
"""
from fabric.api import env, put, sudo, settings
import os

env.hosts = ['100.25.41.202', '100.25.205.60']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path (str): path to the archive to share

    Returns:
        True: if file exists at archive_path and no error occurs
        False: Otherwise!
    """
    if not os.path.exists(archive_path):
        return False

    filename = os.path.basename(archive_path)
    folder_name = os.path.splitext(filename)[0]
    release_path = f'/data/web_static/releases/{folder_name}'
    tmp_path = f'/tmp/{filename}'

    try:
        with settings(warn_only=True):
            if put(archive_path, tmp_path).failed:
                return False

            if sudo(f'rm -rf {release_path}').failed:
                return False

            if sudo(f'mkdir -p {release_path}').failed:
                return False

            if sudo(f'tar -xzf {tmp_path} -C {release_path}').failed:
                return False

            if sudo(f'rm {tmp_path}').failed:
                return False

            source = f'{release_path}/web_static/*'
            dest = f'{release_path}/'
            if sudo(f'mv -f {source} {dest}').failed:
                return False

            if sudo(f'rm -rf {release_path}/web_static').failed:
                return False

            if sudo('rm -rf /data/web_static/current').failed:
                return False

            if sudo(f'ln -s {release_path} /data/web_static/current').failed:
                return False
            print("New version deployed!")

        return True
    except Exception as e:
        return False
