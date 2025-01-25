#!/usr/bin/python3
"""
Fabfile that creates and distributes an archive to web servers using deploy()

Attributes:
    env.hosts (list): holds web server ip addresses
"""
from fabric.api import env, put, run, sudo, local
from datetime import datetime
from os import path
import tarfile

env.hosts = ['100.25.41.202', '100.25.205.60']


def do_pack():
    """Generates a .tgz from contents of web_static"""
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive = f"web_static_{time}.tgz"
    print(f"Packing web_static to {archive}")
    if local(f"tar -cvzf {archive} web_static/", capture=True).failed:
        return None
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            print(member.name)
    return archive


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path (str): path to the archive to share

    Returns:
        True: if file exists at archive_path and no error occurs
        False: Otherwise!
    """
    if not path.exists(archive_path):
        return False

    try:
        archive_name = path.basename(archive_path)
        base_name = archive_name.split('.')[0]
        remote_tmp = f"/tmp/{archive_name}"
        release_dir = f"/data/web_static/releases/{base_name}"

        put(archive_path, remote_tmp)

        sudo(f"mkdir -p {release_dir}")

        sudo(f"tar -xzf {remote_tmp} -C {release_dir}")

        run(f"rm {remote_tmp}")
        sudo(f"mv {release_dir}/web_static/* {release_dir}")
        sudo(f"rm -rf {release_dir}/web_static")

        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -s {release_dir} /data/web_static/current")

        return True
    except Exception:
        return False


def deploy():
    """Full deployment pipeline"""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
