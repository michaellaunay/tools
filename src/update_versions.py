#!/usr/bin/env python3
""" Modernize a versions.cfg file by changing versions to the latest numbers.
author: Michael Launay
mail: michaellaunay@ecreall.com
date: 2023-03-22
"""
import os, sys
import requests
from packaging.version import parse
from typing import IO
import re

def get_latest_version(package_name: str)->str or None:
    """For a given package name, get the latest version from PyPI
    Args:
        package_name (str): The name of the package to check.
    Returns:
        str: the latest version number
        None: if the package does not exist on PyPI
    """
    response = requests.get(f"https://pypi.python.org/pypi/{package_name}/json")
    if response.status_code == 200:
        json = response.json()
        realase_keys = json["releases"].keys()
        latest_version = max(parse(v) for v in realase_keys)
        return str(latest_version)
    else:
        return None

def update_versions(version_file: IO, output_file: IO, verbose:bool = False)->int:
    """Update the versions in a version.cfg file
    Args:
        version_file (IO): the the version.cfg file
        output_file (IO): the output file
        verbose (bool): verbose mode, default is False
    Returns:
        int: 0 if successful, 1 when one line could not be parsed
    """
    result = 0
    for line in version_file:
        line = line.strip()
        if line.startswith("#") or line == "" or line.startswith("["):
            # Skip comments and blank lines and section headers
            print(line, file=output_file)
            continue
        try:
            # get the package name and current version number
            # then get the latest version number from PyPI
            package_name, current_version = re.split(">=|<=|=|>|<",line.strip())
            latest_version = get_latest_version(package_name.strip())
            if latest_version is not None and parse(latest_version) > parse(current_version):
                if verbose:
                    print("#"+line, file=output_file)
                updated_line = f"{package_name}= {latest_version}"
                print(updated_line, file=output_file)
            else:
                print(line, file=output_file)
        except ValueError:
            print("#Error parsing line, not be updated: ", file=output_file)
            print(line, file=output_file)
            result = 1
    return result

if __name__ == "__main__":
    import optparse

    if sys.version_info < (3, 6):
        print("This script requires Python 3.6 or later")
        sys.exit(1)

    parser = optparse.OptionParser(usage="usage: %prog [options]",
                      description="""This script update package version from version.cfg file if passed or from stdin.
                      The output is written to stdout by default or to the file passed as argument.""")
    parser.add_option("-f", "--file", dest="version_file_path", help="Path to the version.cfg file, default is stdin.")
    parser.set_defaults(version_file_path="stdin")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode.")
    parser.set_defaults(verbose=False)
    parser.add_option("-o", "--output", dest="output_file_path", help="Path to the output file, default is stdout.")
    parser.set_defaults(output_file_path="stdout")
    options, args = parser.parse_args()
    resultat = 1
    version_file = None
    output_file = None
    try:
        if options.version_file_path == "stdin":
            version_file = sys.stdin
        else:
            version_file = open(options.version_file_path, "r")
        if options.output_file_path == "stdout":
            output_file = sys.stdout
        else:
            output_file = open(options.output_file_path, "w")
        resultat = update_versions(version_file, output_file, verbose=options.verbose)
    except Exception as e:
        print(e, sys.stderr)
    finally :
        if version_file is not None and version_file is not sys.stdin:
            version_file.close()
        if output_file is not None and output_file is not sys.stdout:
            output_file.close()
        sys.exit(resultat)
