#!/usr/bin/python3

"""
This script is used to pack the web_static directory into a .tgz archive.

It uses Fabric, a Python library and command-line tool for streamlining
the use of SSH for application deployment.

Functions:
    do_pack: Packs the web_static directory into a .tgz archive.
"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """
    Packs the web_static directory into a .tgz archive.

    The function creates a 'versions' directory if it doesn't exist,
    generates a .tgz archive from the 'web_static' directory,
    and stores it in the 'versions' directory. The name of the
    archive is in the
    format 'web_static_<year><month><day><hour><minute><second>.tgz'.

    Returns:
        str: The path of the created archive if the archive is successfully
        created, otherwise None.
    """
    local('mkdir -p versions')
    archive_name = "web_static_" + datetime.now().strftime(r"%Y%m%d%H%M%S")
    archive_name += ".tgz"

    output = local(f'tar -cvzf versions/{archive_name} web_static')
    archive_path = None

    if output.succeeded:
        archive_path = f"versions/{archive_name}"

    return archive_path
