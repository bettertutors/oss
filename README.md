OSS
===

Provisions: servers, monitors inventory, sets up orchestration, and enables logging and monitoring.

NOTE: This is pre-alpha software, recommend waiting for v1 ^_^

## Strategy

A JSON file consisting of: provider, hardware, OS and pick strategy.

This flexibility allows it to scale elastically across multiple cloud providers, optimising on:

  - Price [coming soon]
  - Aggregate price [coming soon]
  - Hardware specifications
  - Software specifications
  - Geolocation
  - Redundancy ratio [coming soon]

See `strategy.sample.json` for an example config.

### Pick strategy

Depends on what you put in the `"pick"` field. Examples:

  - `first` [default], takes first non-error
  - `random`

#### Coming soon

  - `cheapest`
  - `priciest`

### Redundancy [coming soon]

Global field `redundancy`. Here are examples of possible values:

  - `1:1` [default]
  - `2:1`
  - `+5`

TODO: Workout exactly what this will look like, especially taking georedundancy into consideration.

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

## Roadmap

### Version 1

  - Define JSON-schema and validate given strategy file before continuing
  - Add DNS support
  - Configure with service-discovery
  - Utilise secret sharing to secure+unlock—e.g.: AWS keys across—your cloud
  - Example load-balancing with a simple HTTP service

### Version 1.5

  - Present examples with different configuration management systems
    - Puppet
    - SaltStack
    - Fabric [not really a CM, but yeah]
    - Chef
    - Ansible

### Version 2

  - Shiny web-interface with custom dashboarding

### No timeframe

  - Investigate replacing my custom interpreted JSON with UCL (or similar)
