#/usr/bin/python3
# Author: L. A. L. Andati
# Find infos at: https://wiki.python.org/moin/PyPIJSON

import logging
import requests
import sys

from argparse import ArgumentParser
from datetime import datetime


def get_release_dates(package):

    # the pypi url including the dates
    url = f"https://pypi.org/pypi/{package}/json"

    logging.debug(f"Currently getting package: {package}")

    # make get request
    res = requests.get(url)

    # ensure code is 200
    status_code = res.status_code

    # logging.info(f"Request returns status code: {status_code}")

    output = {}

    if res.ok:
        # api returns JSON
        data = res.json()

        # get some info
        p_info = data["info"]

        author = p_info["author"]
        name = p_info["name"]
        curr_version = p_info["version"]

        # keys here are the release versions
        r_info = data["releases"]

        # release info
        release_dates = {}

        for rel_version in r_info:
            mini_releases = r_info[rel_version]
            if len(mini_releases) > 0:
                # latest mini_releas's uptime
                up_time = mini_releases[-1]['upload_time']
                release_dates[up_time] = rel_version
            else:
                continue

        sorted_dates = sorted(release_dates)
        sorted_release_dates = {d: release_dates[d] for d in sorted_dates}
        output["package_name"] = name
        output["author"] = author
        output["latest_version"] = curr_version
        output["release_dates"] = sorted_release_dates
        output["error"] = 0
    else:
        logging.warning(f"Package: {package} returned status code: {status_code}")
        logging.warning("Query has failed")
        output["package_name"] = package
        output["error"] = -1

    # close connection
    res.close()

    logging.debug("Closing connection")

    return output


def parse_required_release(package, before):
    """Get the latest package version before a certain date

    before: date in format dd-mm-yyyy
        Before this get package version for release before or on this date
    package: string
        Name of the python package
    """

    info = get_release_dates(package)

    if info["error"] == 0:

        before = datetime.strptime(before, "%d-%m-%Y")

        release_dates = info["release_dates"]
        p_name = info["package_name"]

        # traverse the list in reverse order (starting from most recent)
        rd_keys = list(release_dates.keys())

        # earliest_release
        er = datetime.strptime(rd_keys[0], "%Y-%m-%dT%H:%M:%S")

        release = None

        # starting from the most recent release
        for da in reversed(rd_keys):
            curr = datetime.strptime(da, "%Y-%m-%dT%H:%M:%S")
            if curr < before:
                release = release_dates[da]
                break

        if release is None:
            logging.warning(f"{package} was not released before {before.day}-{before.month}-{before.year}")
            logging.warning(f"Earliest release is version: {info['latest_version']}, released on: {er.day}-{er.month}-{er.year}")
            result = -1
        else:
            result = f"{p_name}=={release}"

    else:
        result = info["error"]

    return result


def read_reqs_file(rfile):
    with open(rfile, 'r') as rf:
        reqs = rf.readlines()

    reqs = [x.strip('\n') for x in reqs]
    reqs = [x.split("==")[0] for x in reqs]

    return reqs


def get_argparse():
    parser = ArgumentParser(
        usage="pyrewind [options] <value>",
        description="Take your requirements' versions back in time :)")

    required = parser.add_argument_group("Required arguments")
    required.add_argument("--before",
                          help="""Get versions of requirements in 
                          requirements file before this 
                          date. Format must be 'dd-mm-yyyy'""",
                          dest="before", type=str, metavar="", default=None)
    # store_true when argument is provided
    required.add_argument("--debug",
                          help="Enable debugging mode",
                          dest="debug", action="store_true")
    required.add_argument("-if", "--input-file",
                          help="File containing the current requirements",
                          dest="ifile", type=str, metavar="", default=None)

    required.add_argument("-of", "--output-file",
                          help="""Name to give generated output file name 
                          containing the new (older) requirements. Including 
                          the file extension eg. retro.txt""",
                          dest="ofile", type=str, metavar="",
                          default="retro.txt")
    return parser


def main():
    parser = get_argparse()
    options = parser.parse_args()

    if options.debug:
        level = 10
    else:
        level = 20
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

    reqs = read_reqs_file(options.ifile)
    n_reqs = len(reqs)

    logging.info(f"Found {n_reqs} requirements.")

    rels = []
    skipped = []

    for i, req in enumerate(reqs, 1):

        logging.info(f"Package: {i} / {n_reqs}")

        rel = parse_required_release(req, options.before)
        if rel == -1:
            skipped.append(req)
            continue
        else:
            rels.append(f"{rel}\n")

    with open(options.ofile, 'w') as wf:
        wf.writelines(rels)

    logging.info(f"Done writing file to: {options.ofile}")
    logging.info(f"Skipped packages: {', '.join(skipped)}")
