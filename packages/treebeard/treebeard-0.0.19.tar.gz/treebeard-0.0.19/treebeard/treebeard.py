#! python
from treebeard.helper import get_treebeard_env, fetch_credentials, set_credentials
from halo import Halo
import warnings
import click
import shutil
import time
import os
import base64
import tarfile
import json
import os.path
import subprocess
import secrets
import requests
import timeago
import datetime
import sys
from dateutil import parser

config_path = os.path.join(os.path.expanduser('~'), '.treebeard')

treebeard_env = get_treebeard_env(config_path)
url = 'http://localhost:8080/notebooks/'
url = "https://scheduler-cvee2224cq-ew.a.run.app/notebooks/"

notebook_name = treebeard_env['notebook_id']
endpoint = f"{url}{notebook_name}"

credentials = {
    'api_key': treebeard_env['api_key'], 'project_id': treebeard_env['project_id']
}

warnings.filterwarnings(
    "ignore", "Your application has authenticated using end user credentials")

# Instantiates a client
dir_path = os.path.dirname(os.path.realpath(__file__))


@click.group()
def cli():
    pass
    # click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
@click.option('--email', prompt='Your email:')
@click.option('--key', prompt='Your API key:')
def configure(email, key):
    """Set initial credentials"""
    set_credentials(email, key, config_path)

# @cli.command()
# def init():
#     """Connect to Treebeard account (browser popup or CLI login)
#     """
#     # Check if local credentials exist
#     key, email = fetch_credentials()
#     # Authorise User Account with Firebase
#     firebase_auth(key, email)
#     click.echo(f'Account initialised for {email}, key: {key}')
#     return


# @cli.command()
# @click.option('--file', '-f', 'filename', default=None, type=click.Path(exists=True),
#               help='Specify notebook to see logs')
# def logs(filename):
#     """
#     See all actions and deployment results
#     """
#     if filename:
#         click.echo(f'Historical deployments for {filename}:')
#     else:
#         click.echo('Historical deployments for all notebooks:')

@cli.command()
@click.option('t', '--hourly', flag_value='hourly', help='Run notebook hourly')
@click.option('t', '--daily', flag_value='daily', help='Run notebook daily')
@click.option('t', '--weekly', flag_value='weekly', help='Run notebook weekly')
@click.option('t', '--quarter-hourly', flag_value='quarter-hourly', help='Run quarter-hourly')
@click.option('watch', '--watch', help='Run and check completed build status')
def run(t, watch):
    """
    Run a notebook and optionally schedule it to run periodically
    """
    params = {}
    if t:
        params['schedule'] = t

    spinner = Halo(text='requesting run', spinner='dots')
    spinner.start()
    archive_filename = '/tmp/treebeard_upload.tgz'
    with tarfile.open(archive_filename, "w:gz") as tar:
        tar.add(os.getcwd(), arcname=os.path.basename(os.path.sep))

    response = requests.post(
        endpoint,
        files={'repo': open('/tmp/treebeard_upload.tgz', 'rb')},
        params=params,
        headers=credentials)

    spinner.stop()
    try:
        json_data = json.loads(response.text)
        click.echo(f"Run has been accepted! {json_data['admin_url']}")
    except:
        click.echo("Run failed.")
        click.echo(sys.exc_info())

    if watch:
        spinner = Halo(text='watching build', spinner='dots')
        spinner.start()
        build_result = None
        while not build_result:
            time.sleep(5)
            response = requests.get(endpoint, headers=credentials)
            json_data = json.loads(response.text)
            status = json_data['runs'][-1]['status']
            click.echo(f"Build status: {status}")
            if status in ["SUCCESS", "FAILURE", "TIMEOUT", "INTERNAL_ERROR", "CANCELLED"]:
                build_result = status
                spinner.stop()
                click.echo(f"Build result: {build_result}")


@cli.command()
def cancel():
    """Cancels the current notebook build and schedule"""
    spinner = Halo(text='cancelling', spinner='dots')
    click.echo(f"Cancelling {notebook_name}")
    spinner.start()
    requests.delete(endpoint, headers=credentials)
    spinner.stop()
    click.echo(f"cancelled {notebook_name}!")


@cli.command()
def status():
    """Show the status of the current notebook"""
    response = requests.get(endpoint, headers=credentials)
    json_data = json.loads(response.text)
    if len(json_data) == 0:
        click.echo(
            'This notebook has not been run. Try running it with `treebeard run`')
        return
    click.echo('Recent runs:')
    for run in json_data['runs']:
        now = parser.isoparse(datetime.datetime.utcnow().isoformat() + 'Z')
        start_time = parser.isoparse(run['start_time'])
        time_string = timeago.format(start_time, now=now)
        click.echo(f"{run['url']} {time_string}")

    if 'schedule' in json_data:
        click.echo(json_data['schedule'])


@cli.command()
def version():
    """Shows treebeard package version"""
    import pkg_resources  # part of setuptools
    version = pkg_resources.require("treebeard")[0].version
    click.echo(version)


@cli.command()
def info():
    """Shows treebeard credentials and project info"""
    click.echo(treebeard_env)
