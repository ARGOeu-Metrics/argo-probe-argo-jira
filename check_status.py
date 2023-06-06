#!/usr/bin/python3
import argparse
import sys
import requests


class ProbeResponse:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self):
        self.status_code = self.OK

    def write_ok(self, msg):
        print(f"OK - {msg}")
        self.status_code = self.OK

    def write_warning(self, msg):
        print(f"WARNING - {msg}")
        self.status_code = self.WARNING

    def write_critical(self, msg):
        print(f"CRITICAL - {msg}")
        self.status_code = self.CRITICAL

    def write_unknown(self, msg):
        print(f"UNKNOWN - {msg}")
        self.status_code = self.UNKNOWN

    def get_statuscode(self):
        return self.status_code


def check_status(args):
    probe = ProbeResponse()
    try:
        response = requests.get("%s/status" % args.url, timeout=args.timeout)
        response.raise_for_status()

        status = response.json()["state"]

        if status == "RUNNING":
            probe.write_ok("Service available")

        else:
            probe.write_warning("Service not available: %s" % status)

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
        ValueError,
        KeyError
    ) as err:
        probe.write_critical(str(err))

    except Exception as err:
        probe.write_unknown(str(err))

    sys.exit(probe.get_statuscode())


def main():
    parser = argparse.ArgumentParser(
        description="ARGO probe that checks service status.", add_help=False
    )
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "-t", "--timeout", type=int, dest="timeout", help="timeout",
        required=True
    )
    required.add_argument(
        "-u", "--url", type=str, dest="url", help="service url", required=True
    )
    optional.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS,
        help="show this help message and exit"
    )
    args = parser.parse_args()

    check_status(args)


if __name__ == "__main__":
    main()
