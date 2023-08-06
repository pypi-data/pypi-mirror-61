<p align="center">
    <a href="#readme">
        <img alt="logo" width="20%" src="dask.png">
    </a>
</p>

---

**ondemand-dask**, Dask cluster on demand and automatically delete itself after expired.

## Problem statement

Dask is really a great library for distributed programming using Python scale up more than 1TB data. Traditionally, we spawned a Dask cluster using VM or Kubernetes to process our data, and after that, Dask cluster will idle probably most of the time. We got charged even Dask cluster in idle mode (no computation happened).

So this library will help you to spawn a Dask cluster with custom size of CPU, RAM and worker, and automatically gracefully delete itself after idle for certain period.

It also support simple alert system to post message during spawning and gracefully delete, default is Slack.

## Installing from the PyPI

```bash
pip install ondemand-dask
```

## Before use

**Make sure your machine already installed gcloud SDK and your GCP account powerful enough to spawn compute engine and upload to google storage**.

If not, simply download gcloud SDK, https://cloud.google.com/sdk/docs/downloads-versioned-archives, after that,

```bash
gcloud init
```

## examples

Simply check notebooks in [example](example).

## usage

1. Build image, this process only need to be done once, [ondemand_dask.build_image](https://github.com/kfit-dev/ondemand-dask#ondemand_daskbuild_image)
2. Spawn a cluster, [ondemand_dask.spawn](#)

#### ondemand_dask.build_image

```python

def build_image(
    project: str,
    zone: str,
    bucket_name: str,
    instance_name: str,
    image_name: str,
    project_vm: str = 'ubuntu-os-cloud',
    family_vm: str = 'ubuntu-1804-lts',
    storage_image: str = 'asia-southeast1',
    webhook_function: Callable = post_slack,
    install_bash: str = None,
    **kwargs
):
    """
    Parameters
    ----------

    project: str
        project id
    zone: str
    bucket_name: str
        bucket name to upload dask code, can be private.
    image_name: str
        image name for dask bootloader.
    project_vm: str, (default='ubuntu-os-cloud')
        project name for vm. 
    family_vm: str, (default='ubuntu-1804-lts')
        family name for vm.
    storage_image: str, (default='asia-southeast1')
        storage location for dask image.
    webhook_function: Callable, (default=post_slack)
        Callable function to send alert, default is post_slack.
    **kwargs:
        Keyword arguments to pass to webhook_function.
    """

```

Usage is simply,

```python
import ondemand_dask

project = 'project'
zone = 'asia-southeast1-a'
bucket_name = 'bucket'
instance_name = 'dask-build'
image_name = 'dask-image'
webhook_slack = 'https://hooks.slack.com/services/'

ondemand_dask.build_image(
    project = project,
    zone = zone,
    bucket_name = bucket_name,
    instance_name = instance_name,
    image_name = instance_name,
    webhook = webhook_slack,
)
```

Simply check [example/upload.ipynb](example/upload.ipynb).

This process only need to do once, unless,

1. Custom alert platform, eg, Telegram, Discord and etc.

```python

# only accept one parameter.
def post_to_platform(msg: str):
    status_code = do something
    return status_code

ondemand_dask.build_image(
    project = project,
    zone = zone,
    bucket_name = bucket_name,
    instance_name = instance_name,
    image_name = instance_name,
    webhook_function = post_to_platform
    # webhook not required, only required if not overwrite `webhook_function`
)
```

You need to make sure function `post_to_platform` returned 200.

#### ondemand_dask.spawn

```python
def spawn(
    cluster_name: str,
    image_name: str,
    project: str,
    cpu: int,
    ram: int,
    zone: str,
    worker_size: int,
    check_exist: bool = True,
    graceful_delete: int = 180,
    webhook_function: Callable = post_slack,
    **kwargs
):
    """
    function to spawn a dask cluster.

    parameter
    ---------

    cluster_name: str
        dask cluster name.
    image_name: str
        image name we built.
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
    graceful_delete: int, (default=180)
        Dask will automatically delete itself if no process after graceful_delete (seconds).
    webhook_function: Callable, (default=post_slack)
        Callable function to send alert, default is post_slack.
    **kwargs:
        Keyword arguments to pass to webhook_function.
    """
```