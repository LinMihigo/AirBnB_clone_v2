#!/usr/bin/python3
"""
Fabfile that holds do_deploy

Attributes:
    env.hosts (list): holds web server ip addresses
"""
from fabric.api import env, put, run, sudo
from os import path


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
