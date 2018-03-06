import os
import argparse

from update_service import UpdateService
from requirement_interpreter import RequirementInterpreter
from version_matcher import VersionMatcher
from pypi_service import PyPiService
from http_client import HttpClient


def update_service_factory():
    requirement_interpreter = RequirementInterpreter()
    version_matcher = VersionMatcher()
    http_client = HttpClient()
    pypi_service = PyPiService(http_client)

    return UpdateService(requirement_interpreter,
                         version_matcher,
                         pypi_service)


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def print_available_updates(available_updates):
    for update in available_updates:
        print("> {} {}->{}".format(update['package_name'],
                                   update['current_version'],
                                   update['available_version']))


def process(filename):
    print("checking for {}...".format(filename))
    requirements = read_file(filename)
    update_service = update_service_factory()
    available_updates = update_service.find_updates_for(requirements)
    print_available_updates(available_updates)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Search for updates at python requirement files.')
    parser.add_argument('--filenames', '-f',
                        metavar='FILENAME',
                        type=str,
                        nargs='+',
                        default=['requirements.txt', 'requirements-dev.txt'],
                        help='requirement filenames')
    parser.add_argument('path',
                        help='starting path')
    parser.add_argument('-r', '--recursive',
                        required=False,
                        default=False,
                        action="store_true",
                        help='recursive search')

    return parser.parse_args()


def subdirectory_search(path, requirement_files, recursive):
    found_files = []
    for file in requirement_files:
        filepath = "{path}/{file}".format(path=path, file=file)
        if os.path.exists(filepath):
            found_files.append(filepath)

    if recursive:
        walker = os.walk(path)
        for dir_path, dir_names, files in walker:
            existing_files = set(files) & set(requirement_files)
            for file in existing_files:
                filepath = "{path}/{file}".format(path=dir_path, file=file)
                found_files.append(filepath)

    return found_files


def __main__():
    arguments = parse_arguments()
    start_path = arguments.path
    filenames = arguments.filenames
    recursive = arguments.recursive

    for filename in subdirectory_search(start_path, filenames, recursive):
        process(filename)

__main__()
