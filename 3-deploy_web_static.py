#!/usr/bin/python3

"""
This script is used to pack the web_static directory into a .tgz
archive and deploy it on a server.

It uses Fabric, a Python library and command-line tool for
streamlining the use of SSH for application deployment.

The script is configured to deploy on two servers:
'web-01.s1cario.tech' and 'web-02.s1cario.tech'.

Functions:
    do_pack: Packs the web_static directory into a .tgz archive.
    do_deploy: Deploys an archive to the web servers.
    deploy: Packs the web_static directory and deploys it to the web servers.
"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['web-01.s1cario.tech', 'web-02.s1cario.tech']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


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


def do_deploy(archive_path):
    """
    Deploys an archive to the web servers.

    The function uploads the archive to the /tmp directory of the
    web server, extracts the archive to the /data/web_static/releases/
    directory, deletes the archive from the web server, moves the
    web static files out of the web_static folder to the parent folder,
    deletes the web_static folder, deletes the symbolic link
    /data/web_static/current and creates a new the symbolic
    link /data/web_static/current that links to the new version
    of the website.

    Args:
        archive_path (str): The path to the archive.

    Returns:
        bool: True if all operations were successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    status = True
    try:
        put(archive_path, '/tmp/')

        archive_name = archive_path.split('/')[-1].rsplit('.')
        extraction_path = f'/data/web_static/releases/{archive_name[0]}'

        run(f'rm -rf {extraction_path}')
        run(f'mkdir -p {extraction_path}')
        run(f'tar -xzf /tmp/{".".join(archive_name)} -C {extraction_path}')
        run(f'rm /tmp/{".".join(archive_name)}')
        run(f'mv -f {extraction_path}/web_static/* {extraction_path}/')
        run(f'rm -rf {extraction_path}/web_static/')
        run('rm -rf /data/web_static/current')
        run(f'ln -fs {extraction_path} /data/web_static/current')
    except Exception:
        status = False

    return status


def deploy():
    """
    Packs the web_static directory and deploys it to the web servers.

    The function calls the do_pack function to pack the web_static
    directory into a .tgz archive and then calls the do_deploy function
    to deploy the created archive to the web servers.

    Returns:
        bool: True if all operations were successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
