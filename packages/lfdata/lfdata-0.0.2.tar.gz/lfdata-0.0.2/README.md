# LF Data

This project provides a set of useful tools for interacting with data taken from
the LF AWESOME receivers maintained by the LF Radio Lab at Georgia Tech. This
data is available publicly at [Waldo World](https://waldo.world/). 

## Installation

Run the following to install:

```python
pip install lfdata
```

## Example Usage

```python
from lfdata import data_loader

# Load an entire .mat file
data = data_loader("path_to_mat_file")

# Load a specific variable or set of variables
variables = ["station_name", "call_sign", "data"]
data = data_loader("path_to_mat_file", variables)
```
