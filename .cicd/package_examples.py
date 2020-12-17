########
# Copyright (c) 2014-2019 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
from re import sub

from os import path

from ecosystem_cicd_tools.github_stuff import get_most_recent_release
from ecosystem_cicd_tools.release import blueprint_release_with_latest

from __init__ import (SUPPORTED_EXAMPLES,
               CWD,
               get_cloudify_version)

BLUEPRINTS_RELEASE_NAME = 'Cloudify 5.0.5 Blueprint Examples Bundle v{0}'
GETTING_STARTED = ['getting-started/mc-jboss.yaml',
                   'getting-started/mc-nodejs.yaml']


def get_last_version():
    latest_release = get_most_recent_release()
    return getattr(latest_release, 'tag_name', None)


def get_blueprints_version():
    blueprints_version = get_cloudify_version()
    version = get_last_version()
    logging.info(
        'Old version: {0}. New version: {1}'.format(
            blueprints_version, version))
    version = blueprints_version if blueprints_version > version else version
    try:
        _version = '{0}-{1}'.format(version.split('-')[0], str(int(version.split('-')[1]) + 1))
    except IndexError:
        _version = '{0}-{1}'.format(version, str(0))
    return _version


def update_getting_started(file_path, version):
    logging.info('Updating Getting Started!')
    if not path.exists(file_path):
        raise Exception('Tried to update getting started but failed.')
    lines = open(file_path, 'r').readlines()
    lines = [sub(r"[\d\.]+\-[\d]+", version, l) for l in lines]
    for line in lines:
        logging.info('Line: {0}'.format(line))
    f = open(file_path, 'w')
    f.writelines(lines)
    f.close()


if __name__ == '__main__':

    blueprint_examples_version = get_blueprints_version()
    blueprint_release_name = BLUEPRINTS_RELEASE_NAME.format(
        blueprint_examples_version)

    for gs in GETTING_STARTED:
        update_getting_started(gs, blueprint_examples_version)

    blueprints = {}
    for blueprint_id, _ in SUPPORTED_EXAMPLES.items():
        blueprint_path = path.join(CWD, blueprint_id)
        blueprints.update({blueprint_id: blueprint_path})

    blueprint_release_with_latest(
        'blueprint-examples',
        blueprint_examples_version,
        blueprint_release_name,
        blueprints)
