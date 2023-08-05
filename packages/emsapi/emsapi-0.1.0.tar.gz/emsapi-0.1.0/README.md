# Python Client Library for the EMS API

This project is a client library for the EMS API that is generated using [AutoRest](https://github.com/Azure/autorest). It is intended to be a direct mirror of the routes and models exposed by the EMS API. This makes the package suitable for purpose-built projects that want to use the low-level API routes directly with minimal effort.

For data science and exploratory use, consider using the [emsPy](https://github.com/ge-flight-analytics/emspy) package instead.

## Getting Started

### Install via pip

```bash
pip install emsapi
```

### Create an API client

In your code, create an API client object using an endpoint, username, and password:

```python
from emsapi import emsapi

user = "..."
password = "..."
url = "https://ems.efoqa.com/api/"

client = emsapi.create(user, password, url)
```

### Retrieve EMS system id

If the EMS system id is not known, it should be retrieved before any further requests:

```python
ems_id = client.find_ems_system_id('ems7-app')
```

### Access routes on the API client

Different routes are exposed as members of the `client` object created in the previous step. These routes match the sections in the `API Explorer` documentation in the web UI. Most of them need the ems system id (see previous step).

```python
# The routes exposed by the client:
client.analytic
client.analytic_set
client.asset
client.database
client.ems_profile
client.ems_system
client.navigation
client.parameter_set
client.profile
client.tableau
client.trajectory
client.transfer
client.upload
client.weather
```

Examples:

```python
# List the root analytic group contents
groups = client.analytic.get_analytic_group_contents(ems_id)

# Query a specific analytic
flight = 123
altitude_id = "H4sIAAAAAAAEAG2Q0QuCMBDG34P+B/HdbZVUiApBPQT2kgi9rrn0YM7aZvbnN5JVUvdwfHD34/vu4iPXrbjTs+D7kksDF+DKezRC6ggSvzbmGmHc9z3qF6hVFZ4TMsOnQ5azmjc0AKkNlYz7A/Mm9GusUUkNZa00ijLj+BCTFd6UgApF/XQ68bx4SMHVvkyd1GjX6KytgFER46+FEZBfObOZ2db6eBBJEIlvVGfz4P+LhYRbZ29NyVCzgJD1MgitDIhrrj6+P/h04obj36VPLpuOeVIBAAA="

# Pull out altitude with 100 samples through the file.
query = {
    "select": [
        {
            "analyticId": altitudeId
        }
    ],
    "size": 100
}

altitude = client.analytic.get_query_results(ems_id, flight, query)
```