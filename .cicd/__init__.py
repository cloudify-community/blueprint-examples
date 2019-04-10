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

from collections import OrderedDict
from json import load as load_json
from os import path
from urlparse import urlparse
from yaml import load as yaml_load, YAMLError

CWD = '/{0}'.format(
    '/'.join(path.abspath(path.dirname(__file__)).split('/')[1:-1],))
SUPPORTED_EXAMPLES_FILE = path.join(CWD, '.cicd/supported_examples.json')


def get_supported_examples():
    with open(SUPPORTED_EXAMPLES_FILE, 'r') as outfile:
        return load_json(outfile, object_pairs_hook=OrderedDict)


# This structure tells us which files to support.
SUPPORTED_EXAMPLES = get_supported_examples()

# Let's make a list of supported blueprint files.
blueprint_list = ['{0}/{1}/{2}'.format(CWD, dirname, filename)
                  for dirname, filelist in SUPPORTED_EXAMPLES.items()
                  for filename in filelist]


class VersionsException(Exception):
    pass


def get_cloudify_version():
    """Let's get the Cloudify versions of the blueprints.
    We need them to make sure they are all the same in the tests.
    And also to get the cloudify version for the release.
    """

    cloudify_version = None
    # Loop through each blueprint file.
    for blueprint_file in blueprint_list:
        # Load the blueprint YAML as a dictionary.
        with open(blueprint_file, 'r') as stream:
            try:
                blueprint_yaml = yaml_load(stream)
            except YAMLError as e:
                raise VersionsException(
                    'Problem with the file: {0}...{1}'.format(
                        blueprint_file, str(e)))

        # Loop through the imports
        for blueprint_import in blueprint_yaml['imports']:
            import_url = urlparse(blueprint_import)
            if import_url.netloc != 'cloudify.co':
                # It's not a cloudify.co import.
                continue
            next_version = import_url.path.split('/')[-2:-1]
            if isinstance(next_version, list):
                next_version = next_version.pop()
            if not isinstance(next_version, basestring):
                raise VersionsException(
                    'Cloudify version problem: {0}'.format(cloudify_version))
            if cloudify_version and next_version != cloudify_version:
                raise VersionsException(
                    'Cloudify version mismatch: {0}/{1} from {2}'.format(
                        cloudify_version, next_version, blueprint_file))
            cloudify_version = next_version
    return cloudify_version
