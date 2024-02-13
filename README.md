# argo-probe-argo-servicestatus

A generic probe to check service status. The probe calls contacts the endpoint and infers from the response if the service is up and running.

## Synopsis

The probe takes four arguments: `timeout`, `url`, `key` and `value`. Timeout and service URL must be defined, for key and value there are default values if they are not defined.

```
# /usr/libexec/argo/probes/argo-servicestatus/check_status.py -h
usage: check_status.py -t TIMEOUT -u URL [-k KEY] [-v VALUE] [-h]

ARGO probe that checks service status.

required arguments:
  -t TIMEOUT, --timeout TIMEOUT
                        timeout
  -u URL, --url URL     service url

optional arguments:
  -k KEY, --key KEY     key to check in the service response
  -v VALUE, --value VALUE
                        value of the key necessary for the probe to return OK
                        status
  -h, --help            show this help message and exit
```

The probe is checking the response of service API endpoint, and checks for given key and value. If they are as expected, the probe returns OK, if not, it raises alert.

Example execution of `check_status.py`

```
# /usr/libexec/argo/probes/argo-servicestatus/check_status.py -t 30 -u https://wiki.eoscfuture.eu/status

OK - Service available|time=0.076267s;size=19B
```
