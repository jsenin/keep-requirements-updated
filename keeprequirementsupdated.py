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
                        type=str,
                        default='./',
                        help='starting path')
    parser.add_argument('--recursive', '-r',
                        required=False,
                        type=bool,
                        default=False,
                        nargs=0,
                        help='recursive search')

    return parser.parse_args()


def subdirectory_search(start_path, requirement_files, recursive):
    default_files = ["{path}{file}".format(path=start_path, file=file) for file in requirement_files]
    found_files = default_files
    if recursive:
        walk = os.walk(start_path)
        for dir_path, dir_names, files in walk:
            match = set(files) & set(requirement_files)
            found_files = found_files + ["{path}{file}".format(path=dir_path, file=file) for file in match]

    return found_files

def __main__():
    arguments = parse_arguments()
    start_path = arguments.path
    filenames = arguments.filenames
    recursive = arguments.recursive

    for filename in subdirectory_search(start_path, filenames, recursive):
        if os.path.exists(filename):
            process(filename)


__main__()
