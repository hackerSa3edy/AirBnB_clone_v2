#!/usr/bin/python3

"""
This script is used to deploy a web static content on a server.

It uses Fabric, a Python library and command-line tool for
streamlining the use of SSH for application deployment.

The script is configured to deploy on two servers:
'web-01.s1cario.tech' and 'web-02.s1cario.tech'.

Functions:
    do_deploy: Deploys an archive to the web servers.
"""

from fabric.api import *
import os

env.hosts = ['54.162.51.179', '100.25.222.165']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


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

        sudo(f'rm -rf {extraction_path}')
        run(f'mkdir -p {extraction_path}')
        run(f'tar -xzf /tmp/{".".join(archive_name)} -C {extraction_path}')
        run(f'rm /tmp/{".".join(archive_name)}')
        run(f'mv -f {extraction_path}/web_static/* {extraction_path}/')
        run(f'rm -rf {extraction_path}/web_static/')
        run('rm -rf /data/web_static/current')
        run(f'ln -fs {extraction_path} /data/web_static/current')
        sudo('chown -R ubuntu:ubuntu /data/web_static/')
        print("New version deployed!")
    except Exception:
        status = False

    return status
