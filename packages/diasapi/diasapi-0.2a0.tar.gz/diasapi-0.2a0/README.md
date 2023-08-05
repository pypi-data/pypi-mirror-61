# CMCC-DIAS-Client
DIAS API Client for access and analysis of CMCC data

## Requirements
Python 3.7

### Installation  
To install the tool:

```bash
$ git clone https://github.com/CMCC-Foundation/cmcc-dias-client
$ cd cmcc-dias-client
$ python setup.py install
```

### Configuration
To use the tool a file `$HOME/.diasapirc` must be created as following

```bash
url: http://dias.cmcc.scc:8282/api/v1
key: <uid>:<api-key>
```

### Example
```python
import diasapi

c = diasapi.Client()
c.retrieve("era5",
           { "variable": "tp",
             "product_type": "reanalysis",
             "year": ["1981","1983","1984"],
             "month": ["01","03","05"],
             "day": ["01","02"],
             "time": ["00:00", "06:00", "12:00", "18:00"],
             "area": [50, 10, 0, 30],
             "format": "netcdf",
           },
           "era5_reanalysis_tp.nc")
```
