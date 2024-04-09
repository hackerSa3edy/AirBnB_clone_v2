#!/usr/bin/python3

"""
This script is used to clean up old versions of deployed web_static directories

It uses Fabric, a Python library and command-line tool for streamlining the use
of SSH for application deployment.

The script is configured to clean up on two servers:
'web-01.s1cario.tech' and 'web-02.s1cario.tech'.

Functions:
    do_clean: Cleans up old versions of deployed web_static directories.
"""

from fabric.api import *

env.hosts = ['54.162.51.179', '100.25.222.165']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    """
    Cleans up old versions of deployed web_static directories.

    The function keeps the number of versions specified by the 'number'
    parameter and removes the rest. If 'number' is 0 or 1, it keeps only the
    most recent version. The function cleans up both locally (in the
    'versions' directory) and on the remote servers (in the
    '/data/web_static/releases' directory).

    Args:
        number (int, optional): The number of versions to keep. Defaults to 0.

    Returns:
        None
    """
    number = int(number)
    if number == 0:
        number = 1

    with lcd('versions'):
        files = local("ls -1tr", capture=True).split('\n')
        if len(files) != 0:
            local(f"sudo rm -rf $(ls -tr | head -n -{number})")

    with cd('/data/web_static/releases'):
        files = run("ls -1tr").split('\n')
        files = [f for f in files if f.startswith(r'web_static_')]
        if len(files) != 0:
            sudo(f"rm -rf $(ls -tr | head -n -{number})")
