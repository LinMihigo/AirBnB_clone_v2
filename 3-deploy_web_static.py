#!/usr/bin/python3
"""
Fabfile that creates and distributes an archive to web servers using deploy()

Attributes:
    env.hosts (list): holds web server ip addresses
"""
from fabric.api import env, put, sudo, local, settings
from datetime import datetime
import os.path

env.hosts = ['100.25.41.202', '100.25.205.60']


def do_pack():
    """Generates a .tgz from contents of web_static"""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


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
        print(f"Deployment failed: {str(e)}")
        return False


def deploy():
    """Full deployment pipeline"""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
