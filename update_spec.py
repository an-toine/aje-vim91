#!/bin/python
"""This script updates a SPEC file to package last project release

Intended to be run in a Github action workflow, this script is using the Github
Api to fetch the last release of a project and update accordingly the
associated rpm SPEC file.

Once SPEC file is updated, the commit and push process can be handled by a
dedicated Github action.

USAGE:
update_spec.py [-h] [--log-level LOG_LEVEL] project_name spec_file \
changelog_file

A script updating a SPEC file to package last project release

positional arguments:
  project_name          the github project formatted as username/project
  spec_file             the path to the SPEC file to update
  changelog_file        the path to the included changelog file

optional arguments:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        log level to use in the script
"""

import re
import requests
import logging
import sys
import argparse
import datetime


def manage_arguments():
    """Manage script arguments"""
    parser = argparse.ArgumentParser(description="A script updating a SPEC \
                                     file to package last project release")
    parser.add_argument("project_name", type=str, help="the github project \
                        formatted as username/project")
    parser.add_argument("spec_file", type=str, help="the path to the SPEC \
                        file to update")
    parser.add_argument("changelog_file", type=str, help="the path to the \
                        included changelog file")
    parser.add_argument('--log-level', dest='log_level', action="store",
                        type=str, default="INFO", help="log level to use \
                        in the script")
    return parser.parse_args()


def get_current_spec_version(spec_file):
    """Extract from a spec file the associated version"""
    logging.debug("Opening file {}".format(spec_file))

    with open(spec_file, "r") as f:
        spec_content = f.read()

    version_regex = re.compile(r"^Version: ?([0-9a-z\.\-]+)$", re.MULTILINE)
    version = version_regex.search(spec_content)

    if version is None or version.group(1) is None:
        raise Exception("Version not found in SPEC file")

    logging.debug("Regex version result is {}".format(version.groups()))
    return version.group(1)


def get_latest_project_version(project):
    """Retreive from Github API the latest tagged version for a project"""
    url = "https://api.github.com/repos/{}/tags?per_page=1".format(project)
    headers = {"Accept": "application/vnd.github.v3+json"}

    logging.debug("Latest release will be fetched from {}".format(url))
    response = requests.get(url, headers=headers)
    raw_version = response.json()[0]["name"]
    logging.debug("Latest release fetched from Github is {}".format(
        raw_version))
    if raw_version.startswith("v"):
        logging.debug("Removing first char from version")
        version = raw_version[1:]
    else:
        version = raw_version
    return version


def update_spec(version, spec, changelog):
    """Update spec file and changelog with last version number"""
    logging.debug("Loading in memory file {}".format(spec))
    with open(spec, "r") as f:
        spec_content = f.read()
    logging.debug("Replacing version in spec file")
    version_regex = re.compile(r"^(Version: ?)[0-9a-z\.\-]+$", re.MULTILINE)
    updated_spec = version_regex.sub(r"\g<1>{}".format(version), spec_content)

    logging.debug("Loading in memory file {}".format(changelog))
    with open(changelog, "r") as f:
        changelog_content = f.read()
    logging.debug("Building changelog item")
    release_date = datetime.datetime.now().strftime("%a %b %d %Y")
    changelog_item = """* {} Antoine Jouve <ant.jouve@gmail.com> - {}-1
- Build Vim v{}\n""".format(release_date, version, version)

    logging.debug("Writing updated spec file")
    with open(spec, "w") as f:
        f.write(updated_spec)
    logging.debug("Writing changelog file")
    with open(changelog, "w") as f:
        f.write(changelog_item + changelog_content)


if __name__ == "__main__":
    arguments = manage_arguments()

    # Setup logger output format
    numeric_log_level = getattr(logging, arguments.log_level.upper())
    log_format = "%(asctime)s %(levelname)s %(funcName)s: %(message)s"
    logging.basicConfig(level=numeric_log_level,
                        datefmt="%Y-%m-%dT%H:%M:%S%z",
                        format=log_format,)

    logging.info("Starting SPEC update script")
    logging.info("Parsing spec file {} for project {}".format(
        arguments.spec_file,
        arguments.project_name))

    try:
        spec_version = get_current_spec_version(arguments.spec_file)
    except Exception as e:
        logging.error("Version extraction from {}, failed with exception \
{}".format(arguments.spec_file, e))
        sys.exit(1)

    logging.info("Current SPEC version is {}".format(spec_version))

    try:
        project_version = get_latest_project_version(arguments.project_name)
    except Exception as e:
        logging.error("Project {} last release fetch failed with exception \
{}".format(arguments.project_name, e))
        sys.exit(1)

    logging.info("Latest release version for project {} is \
{}".format(arguments.project_name, project_version))

    if spec_version != project_version:
        try:
            update_spec(project_version, arguments.spec_file,
                        arguments.changelog_file)
        except Exception as e:
            logging.error("Update of spec file failed with exception \
{}".format(e))
    else:
        logging.info("Spec version {} == project version {}, nothing to \
do".format(spec_version, project_version))
        sys.exit(1)
    logging.info("Spec file and changelog were successfuly updated to version \
{}".format(project_version))
    sys.exit(0)
