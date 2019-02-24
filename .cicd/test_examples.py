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
    blueprint_id = '{0}-{1}'.format(
        path.dirname(request.param).split('/')[-1:][0],
        path.basename(request.param).split('.yaml')[0])
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
