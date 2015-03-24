OSS
===

Provisions: servers, monitors inventory, sets up orchestration, and enables logging and monitoring.

NOTE: This is pre-alpha software, recommend waiting for v1 ^_^

## Strategy

A JSON file consisting of: provider, hardware, OS and pick strategy.

### Pick strategy [coming soon]

Depends on what you put in the `"pick"` field. Examples:

  - `first` [default], takes first non-error
  - `random` or `any`
  - `cheapest`
  - `priciest`

This flexibility allows it to scale elastically across multiple cloud providers, optimising on:

  - Price
  - Aggregate price
  - Hardware specifications
  - Software specifications
  - Geolocation
  - Redundancy ratio
  - &etc.

### Redundancy [coming soon]

Global field `redundancy`. Here are examples of possible values:

  - `1:1` [default]
  - `2:1`
  - `+5`

TODO: Workout exactly what this will look like, especially taking georedundancy into consideration.

### Example

See `strategy.sample.json` for an example config.

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

Default strategy in `strategy.sample.json`.
