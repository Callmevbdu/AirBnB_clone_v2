#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import local, run, sudo, env, cd
from datetime import datetime


def do_pack():
    """
    Compresses the web_static folder into a .tgz archive.
    """

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = os.path.join("versions", archive_name)

    local('mkdir -p versions')

    archive = local("tar -czvf {archive_path} web_static/")

    if archive is not None:
        return archive_path
    else:
        return None
