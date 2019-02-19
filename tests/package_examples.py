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

from contextlib import closing
from os import environ, path, walk
from tempfile import NamedTemporaryFile
import zipfile

from github import Github

ASSET_TYPE = 'zip'
CWD = '/{0}'.format(
    '/'.join(
        path.abspath(
            path.dirname(__file__)
        ).split('/')[1:-1]
    )
)

SUPPORTED_EXAMPLES = (
    ('aws-example-network', 'blueprint.yaml'),
    ('azure-example-network', 'blueprint.yaml'),
    ('gcp-example-network', 'blueprint.yaml'),
    ('openstack-example-network', 'blueprint.yaml'),
)


class NewRelease(object):

    def __init__(self):
        self.version = self._get_version()
        self.client = Github(environ['TOKEN'])
        self.repo = \
            self.client.get_repo(
                '{org}/{repo}'.format(
                    org=environ['CIRCLE_PROJECT_USERNAME'],
                    repo=environ['CIRCLE_PROJECT_REPONAME']
                )
            )
        self.commit = self.repo.get_commit(environ['CIRCLE_SHA1'])
        self.release = self.create()

    def create(self):
        return self.repo.create_git_release(
            tag=self.version,
            name=self.version,
            message=self.version,
            target_commitish=self.commit)

    def upload(self, asset_path, basename):
        asset_label = '{0}-{1}.{2}'.format(basename, self.version, ASSET_TYPE)
        self.release.upload_asset(asset_path, asset_label)

    @staticmethod
    def _get_version():
        try:
            return environ['CIRCLE_BRANCH'].split('-build')[0]
        except IndexError:
            raise Exception(
                'Cannot get version from branch name: {0}'.format(
                    environ['CIRCLE_BRANCH']))


class BlueprintArchive(object):
    """If you want to create zip:
    bp = BlueprintPackage('hello_world', '~/Desktop/my_blueprint_folder')
    bp.zip()
    """

    def __init__(self, name, source_directory):
        self.name = name
        self.source = source_directory
        self._destination_file = NamedTemporaryFile()
        self.destination = self._destination_file.name
        self._zip()

    def _zip(self):
        with closing(zipfile.ZipFile(self.destination, 'w')) as zip_file:
            for root, _, files in walk(self.source):
                for filename in files:
                    file_path = path.join(root, filename)
                    source_dir = path.dirname(self.source)
                    zip_file.write(
                        file_path, path.relpath(file_path, source_dir))


if __name__ == "__main__":

    new_release = NewRelease()

    for blueprint_id, blueprint_file_name in SUPPORTED_EXAMPLES:
        new_archive = BlueprintArchive(
            blueprint_id,
            path.join(CWD, blueprint_id, blueprint_file_name)
        )
        new_release.upload(new_archive.destination, new_archive.name)
