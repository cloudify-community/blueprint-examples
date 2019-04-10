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

from os import path, system
import pytest
from __init__ import blueprint_list, get_cloudify_version, VersionsException


UPLOAD_BLUEPRINT = 'cfy blueprints upload {0} -b {1}'


@pytest.fixture(scope='function', params=blueprint_list)
def validate_blueprint(request):
    # For the db-lb-app, we need a blueprint named 'infrastructure'.
    # So this makes sure that the first one that gets uploaded (aws)
    # will be the reference.
    # TODO: Add to supported examples.json desired blueprint name.
    dirname_param = path.dirname(request.param).split('/')[-1:][0]
    infra_name = path.basename(request.param).split('.yaml')[0]
    if dirname_param == 'infrastructure' and infra_name == 'azure':
        blueprint_id = '{0}'.format(dirname_param)
    elif dirname_param == 'infrastructure' and infra_name == 'aws':
        blueprint_id = 'public-cloud'
    elif dirname_param == 'infrastructure' and infra_name == 'openstack':
        blueprint_id = 'private-cloud'
    else:
        blueprint_id = '{0}-{1}'.format(
            dirname_param,
            infra_name)
    return system(UPLOAD_BLUEPRINT.format(request.param, blueprint_id))


def test_blueprints(validate_blueprint):
    """All blueprints must pass DSL validation."""
    assert validate_blueprint == 0


def test_versions():
    """All blueprints in this branch should be the same Cloudify version.
    """
    try:
        assert get_cloudify_version() is not None
    except VersionsException as e:
        pytest.fail(
            "Failed to verify that branch "
            "versions are the same: {0}.".format(str(e)))
