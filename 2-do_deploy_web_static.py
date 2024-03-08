#!/usr/bin/python3
"""
a Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy
"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['54.221.13.125', '52.91.117.179']


def do_deploy(archive_path):
    """
    Deploys the archive to web servers.
    """

    if not exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return False
    try:
        put(archive_path, '/tmp/')

        archive_filename = basename(archive_path)

        release_dir = join(
                "/data/web_static/releases",
                archive_filename.split('.')[0])
        run(f"mkdir -p {release_dir}")
        run(f"tar -xzf /tmp/{archive_filename} -C {release_dir}")

        run(f"rm /tmp/{archive_filename}")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {release_dir} /data/web_static/current")

        return True
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False
