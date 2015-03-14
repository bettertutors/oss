OSS
===

Provisions: servers, monitors inventory, sets up orchestration, and enables logging and monitoring.

## Strategy

Strategy includes things like what OS you want, on what provider, on a node with what specifications.

See `strategy.json` for an example config.

## Requirements

    pip install -r requirements.txt

## Install

    pip install git+https://github.com/bettertutors/oss#egg=bettertutors_oss

## Usage

### Compute

    usage: compute.py [-h] [-s STRATEGY]
    
    Deploy/create/manage compute nodes
    
    optional arguments:
      -h, --help            show this help message and exit
      -s STRATEGY, --strategy STRATEGY
                            strategy file

Default strategy located in `strategy.json`.

## Future work

Support strategies that can scale elastically across multiple cloud providers, optimising on:

  - Price
  - Aggregate price
  - Hardware specifications
  - Software specifications
  - Geolocation
  - Redundancy ratio
  - &etc.
