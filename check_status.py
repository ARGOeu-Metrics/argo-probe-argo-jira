#!/usr/bin/python3
import argparse
import json
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
    perf_data = ""
    try:
        response = requests.get(args.url, timeout=args.timeout)

        response_time = response.elapsed.total_seconds()
        response_size = len(response.content)

        perf_data = f"|time={response_time}s;size={response_size}B"

        status = response.json()[args.key]

        response.raise_for_status()

        if status.lower() == args.value:
            probe.write_ok(f"Service available{perf_data}")

        else:
            probe.write_critical(f"Service not available: {status}{perf_data}")

    except json.decoder.JSONDecodeError as err:
        probe.write_critical(
            f"Error decoding JSON: {str(err)}{perf_data}"
        )

    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
        ValueError,
        KeyError
    ) as err:
        msg = str(err)
        if perf_data:
            msg = f"{msg}{perf_data}"

        probe.write_critical(msg)

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
        "-k", "--key", type=str, dest="key", default="state",
        help="key to check in the service response"
    )
    optional.add_argument(
        "-v", "--value", type=str, dest="value", default="running",
        help="value of the key necessary for the probe to return OK status"
    )
    optional.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS,
        help="show this help message and exit"
    )
    args = parser.parse_args()

    check_status(args)


if __name__ == "__main__":
    main()
