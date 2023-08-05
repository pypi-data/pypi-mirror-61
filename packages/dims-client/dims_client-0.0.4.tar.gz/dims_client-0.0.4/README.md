# UIoT Devices - Dims Client Library

The objective of this library is to enable users to create *Clients* and *Services* that follow UIoT's Ontology of sending and managing message flows

All the protocols included as a means of communication in this library follow the same principles:
* Create a *Device*
* Create a *Service*
* Send *Data*
  
# Basic Usage

* Send *Data*
```
from dims_client import DimsClient

config = {'DEFAULT_DIMS_URI': 'http://0.0.0.0:5000'}

dims_client = DimsClient(
    config=config
)

returned = dims_client.send_data(<data_to_send>)
```

