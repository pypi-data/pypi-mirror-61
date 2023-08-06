# scheduler_tools

[![Build Status](https://github.com/AllenCellModeling/scheduler_tools/workflows/Build%20Master/badge.svg)](https://github.com/AllenCellModeling/scheduler_tools/actions)
[![Documentation](https://github.com/AllenCellModeling/scheduler_tools/workflows/Documentation/badge.svg)](https://AllenCellModeling.github.io/scheduler_tools)
[![Code Coverage](https://codecov.io/gh/AllenCellModeling/scheduler_tools/branch/master/graph/badge.svg)](https://codecov.io/gh/AllenCellModeling/scheduler_tools)

Tools for composing interdependent tasks on a scheduler (i.e. SLURM)

---

## Setup requirements for launching prefect / dask-distributed on the cluster from your local desktop

### On your local system

For whatever project you are working on add scheduler_tools to your dependency
list. 

```bash
conda activate {your_env_name}
pip install -e {your_project_name}
mkdir ~/.aics_dask
```
create file `~/.aics_dask/ssh.json` with contents
```json
{"gateway":{
	"url": "slurm-machine.bettertech.com",
	"user": "flanders",
	"identityfile": "/Users/flanders/ssh/flandersPrivateKey"
	},
    "dashboard_port": 8787,
    "dask_port": 34009
}
```

### On the cluster 
```bash
conda activate {your_env_name}
pip install -e {your_project_name}
mkdir ~/.aics_dask
```


## programmatically launch remote server and create tunnel
```python
from scheduler_tools import Connector
from pathlib import Path

prefs = {'gateway': {}}
prefs['gateway']['url'] = 'slurm-machine.bettertech.com'
prefs['gateway']['user'] = 'flanders'
prefs['gateway']['identityfile'] = '~/.ssh/id_rsa'
prefs['dask_port'] = 34009
prefs['dashboard_port'] = 8787
prefs['localfolder'] = '~/.aics_dask'


dask_prefs = {'cluster_conf': {}, 'worker_conf': {}, 'remote_conf': {}}
dask_prefs['cluster_conf']['queue'] = 'aics_cpu_general'
dask_prefs['cluster_conf']['cores'] = 2
dask_prefs['cluster_conf']['memory'] = '8GB'
dask_prefs['cluster_conf']['walltime'] = "02:00:00"
# dask_prefs['cluster_conf']['job_extra'] = ["--gres=gpu:v100:1"]

dask_prefs['worker_conf']['minimum_jobs'] = 2
dask_prefs['worker_conf']['maximum_jobs'] = 40

dask_prefs['remote_conf']['env'] = 'dask_scheduler'
dask_prefs['remote_conf']['command'] = 'setup_and_spawn.bash'
dask_prefs['remote_conf']['path'] = '.aics_dask'


conn = Connector(distributed_dict=dask_prefs, pref_path=Path('~/.aics_dask/ssh.json'))
conn.run_command()
conn.stop_forward_if_running()
conn.forward_ports()
```

## programmatically shutdown remote server and tunnel
```python
from scheduler_tools import Connector
from pathlib import Path

conn = Connector(pref_path=Path('~/.aics_dask/ssh.json'))
conn.stop_dask()
```

## Command line interface 

### CLI start Dask Cluster command
spawn_dask_cluster -s ~/.aics_dask_gpu/ssh.json -q aics_gpu_general -r <remote_env_name>

### CLI stop Dask Cluster command
shutdown_dask_cluster -s ~/.aics_dask/ssh.json


***Free software: Allen Institute Software License***

