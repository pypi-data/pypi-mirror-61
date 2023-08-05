[![PyPI](https://img.shields.io/pypi/v/simplesam.svg?)](https://pypi.org/project/henipipe/)
<!-- [![Build Status](https://travis-ci.org/mdshw5/simplesam.svg?branch=master)](https://travis-ci.org/mdshw5/simplesam) -->
[![Documentation Status](https://readthedocs.org/projects/henipipe/badge/?version=latest)](https://henipipe.readthedocs.io/en/latest/?badge=latest)

# qsubr
==========

version 0.2

A quick qsub job submission program

```bash
qsubr usage: The missing qsub command [-h] [--cluster CLUSTER] [--queue QUEUE]
                                [--account ACCOUNT] [--name NAME] [--mem MEM]
                                [--nodes NODES] [--threads THREADS]
                                [--log LOG] [--debug]
                                command

positional arguments:
  command               A quoted string of commands

optional arguments:
  -h, --help            show this help message and exit
  --cluster CLUSTER, -c CLUSTER
                        cluster settings
  --queue QUEUE, -q QUEUE
                        queue
  --account ACCOUNT, -A ACCOUNT
                        account_string
  --name NAME, -N NAME  name
  --mem MEM, -gb MEM    memory in gigabytes
  --nodes NODES, -n NODES
                        nodes
  --threads THREADS, -t THREADS
                        threads
  --log LOG, -l LOG     log filename
  --debug, -d           To print commands (For testing flow). OPTIONAL

```

## Acknowledgements

Written by Scott Furlan.