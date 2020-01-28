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
from os import environ, path, walk, remove
from re import sub
import shutil
import sys
from tempfile import NamedTemporaryFile
import zipfile

from github import Github

from __init__ import (CWD,
                      SUPPORTED_EXAMPLES,
                      blueprint_list,
                      get_cloudify_version)

ASSET_TYPE = 'zip'
RELEASE_MESSAGE = """Example blueprints for use with Cloudify version {0}.
This is package number {1} to be released for this version of Cloudify.
Always try to use the latest package for your version of Cloudify."""
GETTING_STARTED = ['getting-started/mc-jboss.yaml']

logging.basicConfig(level=logging.INFO)


class NewRelease(object):
    """Handles Creating Releases and uploading artifacts."""

    def __init__(self):
        self.client = Github(environ['RELEASE_BUILD_TOKEN'])
        self.repo = \
            self.client.get_repo(
                '{org}/{repo}'.format(
                    org=environ['CIRCLE_PROJECT_USERNAME'],
                    repo=environ['CIRCLE_PROJECT_REPONAME']
                )
            )
        self.commit = self.repo.get_commit(environ['CIRCLE_SHA1'])
        self._version = None

        if self.create_new_release():
            self._release = self._create()
        else:
            self._release = None

    def create_new_release(self, create_new_release=False):
        if create_new_release:
            return True
        for commit_file in self.commit.files:
            if commit_file.filename in \
                    [path.relpath(f) for f in blueprint_list]:
                return True
        logging.info(
            'No changes to blueprint files, not creating new release.')
        return False

    @property
    def version(self):
        if self._version:
            return self._version
        blueprints_version = get_cloudify_version()
        version = self._get_last_version()
        logging.info(
            'Old version: {0}. New version: {1}'.format(
                blueprints_version, version))
        if blueprints_version > version:
            version = blueprints_version
        try:
            self._version = '{0}-{1}'.format(
                version.split('-')[0],
                str(int(version.split('-')[1]) + 1))
        except IndexError:
            self._version = '{0}-{1}'.format(version, str(0))
        return self._version

    @property
    def release(self):
        return self._release

    @property
    def name(self):
        gen, iteration = self.version.split('-')
        return 'Cloudify {0} Blueprint Examples ' \
               'Bundle v{1}'.format(gen, iteration)

    @property
    def message(self):
        gen, iteration = self.version.split('-')
        return RELEASE_MESSAGE.format(gen, iteration)

    def _create(self):
        logging.info('Attempting to create new release.')
        return self.repo.create_git_release(
            tag=self.version,
            name=self.name,
            message=self.message,
            target_commitish=self.commit)

    def upload(self, asset_path, basename):
        logging.info('Attempting upload new archive {0}:{1}.'.format(
            asset_path, basename))
        asset_label = '{0}-{1}.{2}'.format(basename, self.version, ASSET_TYPE)
        if not self.release:
            return
        self.release.upload_asset(asset_path, asset_label)

    def _get_last_version(self):
        try:
            return str(self.repo.get_releases()[0].tag_name)
        except (IndexError, KeyError):
            return None

    def update_getting_started(self, file_path):
        if not path.exists(file_path):
            raise Exception('Tried to update getting started but failed.')
        last_version = self._get_last_version() or r"[\d\.]+\-[\d]+"
        lines = open(file_path, 'r').read()
        lines = [sub(last_version, self.version, l) for l in lines]
        f = open(file_path, 'w')
        f.writelines(lines)
        f.close()


class BlueprintArchive(object):
    """Handles creating zip archives of blueprints."""

    def __init__(self, name, source_directory):
        if '/' in name:
            name = name.replace('/', '-')
            name = name.strip('-')
        self.name = name
        self.source = source_directory
        self._dest = NamedTemporaryFile(delete=False)
        self.destination = path.join(
            path.dirname(self._dest.name), '{0}.zip'.format(self.name))
        self._create_archive()
        logging.info('Moving {0} to {1}.'.format(
            self._dest.name, self.destination))
        shutil.move(self._dest.name, self.destination)

    def _create_archive(self):
        logging.info('Archive source: {0}.'.format(self.source))
        logging.info('Archive destination: {0}.'.format(self._dest.name))
        zip_file = zipfile.ZipFile(self._dest.name, 'w')
        for root, _, files in walk(self.source):
            for filename in files:
                file_path = path.join(root, filename)
                source_dir = path.dirname(self.source)
                zip_file.write(
                    file_path, path.relpath(file_path, source_dir))
        zip_file.close()
        logging.info('Finished writing archive {0}'.format(self.name))


if __name__ == "__main__":
    """Create a new release in Github and
    upload zip archives of all the blueprints.
    """

    new_release = NewRelease()

    if not new_release.release:
        logging.info('No new release to upload new archives to.')
        sys.exit()

    for gs in GETTING_STARTED:
        new_release.update_getting_started(gs)

    for blueprint_id, file_path in SUPPORTED_EXAMPLES.items():
        logging.info('Attempting to create new zip {0}.'.format(blueprint_id))
        new_archive = BlueprintArchive(
            blueprint_id,
            path.join(CWD, blueprint_id)
        )
        new_release.upload(new_archive.destination, new_archive.name)
        remove(new_archive.destination)
