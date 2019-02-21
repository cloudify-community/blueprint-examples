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
from __init__ import SUPPORTED_EXAMPLES


CWD = '/{0}'.format(
    '/'.join(path.abspath(path.dirname(__file__)).split('/')[1:-1],))
UPLOAD_BLUEPRINT = 'cfy blueprints upload {0} -b {1}'
params = ['{0}/{1}/{2}'.format(CWD, dirname, filename)
          for dirname, filelist in SUPPORTED_EXAMPLES
          for filename in filelist]


@pytest.fixture(scope='function', params=params)
def validate_blueprint(request):
    blueprint_id = '{0}-{1}'.format(
        path.dirname(request.param).split('/')[-1:][0],
        path.basename(request.param).split('.yaml')[0])
    return system(UPLOAD_BLUEPRINT.format(request.param, blueprint_id))


def test_blueprints(validate_blueprint):
    assert validate_blueprint == 0
