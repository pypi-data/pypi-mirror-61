import googleapiclient.discovery
import time
import socket
from herpetologist import check_type
from datetime import datetime
import requests


def port_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def post_slack(
    slack_msg,
    webhook,
    username = 'Dask Alert',
    icon_url = 'https://avatars3.githubusercontent.com/u/17131925?s=400&v=4',
):
    payload = {
        'text': slack_msg,
        'username': 'Dask Alert',
        'icon_url': 'https://avatars3.githubusercontent.com/u/17131925?s=400&v=4',
    }
    requests.post(webhook, json = payload)


@check_type
def delete_dask(name: str, project: str, zone: str):
    """
    function to delete dask cluster.

    parameter
    ---------

    name: str
        dask cluster name.
    project: str
        project id inside gcp.
    zone: str
        compute zone for the cluster.
    """

    compute = googleapiclient.discovery.build('compute', 'v1')
    return (
        compute.instances()
        .delete(project = project, zone = zone, instance = name)
        .execute()
    )


@check_type
def spawn_dask(
    name: str,
    project: str,
    cpu: int,
    ram: int,
    zone: str,
    worker_size: int,
    check_exist: bool = True,
    post_to_slack = True,
    graceful_delete: int = 180,
):
    """
    function to spawn a dask cluster.

    parameter
    ---------

    name: str
        dask cluster name.
    project: str
        project id inside gcp.
    cpu: int
        cpu core count.
    ram: int
        ram size in term of MB.
    zone: str
        compute zone for the cluster.
    worker_size: int
        worker size of dask cluster, good value should be worker size = 2 * cpu core.
    check_exist: bool, (default=True)
        if True, will check the cluster exist. If exist, will return ip address.
    post_to_slack: bool, (default=True)
        if True, will post to #data-alerts.
    graceful_delete: int, (default=180)
        Dask will automatically delete itself if no process after graceful_delete (seconds).
    """
