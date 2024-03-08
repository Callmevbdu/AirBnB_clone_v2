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
    form = 'web_static_' + now.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'

    local('mkdir -p versions')

    tgz = local("tar -czvf versions/{} web_static/".format(form))

    if tgz is not None:
        return form
    else:
        return None
