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


import os
import pytest

from ecosystem_cicd_tools.github_stuff import (
    find_changed_files_in_branch_pr_or_master)

from ecosystem_tests.dorkl import (
    prepare_test,
    blueprints_upload,
    cleanup_on_failure,
    blueprint_validate,
    basic_blueprint_test)

from __init__ import (
    blueprint_id_filter,
    get_dirname_and_infra_name,
    blueprint_list,
    get_cloudify_version,
    VersionsException,
    PLUGINS_TO_UPLOAD,
    SECRETS_TO_CREATE)

prepare_test(plugins=PLUGINS_TO_UPLOAD,
             secrets=SECRETS_TO_CREATE,
             plugin_test=False,
             yum_packages=['libselinux-python3'])

virtual_machine_list = [b for b in blueprint_list if 'virtual-machine'
                        in b and os.environ.get('IAAS', '') ==
                        os.path.basename(b).split('.yaml')[0]]
getting_started_list = [b for b in blueprint_list if 'getting-started' in b]
openshift_list = ['kubernetes/plugin-examples/openshift/blueprint.yaml']

changed_files = find_changed_files_in_branch_pr_or_master()


def test_validate_blueprints():
    blueprints_to_validate = [blueprint for blueprint in blueprint_list if
                              blueprint.endswith(tuple(changed_files))]
    for blueprint in blueprints_to_validate:
        blueprint_validate(blueprint, blueprint_id_filter(blueprint), skip_delete=True)


def test_validate_blueprints_nightlies():
    blueprints_to_validate = [blueprint for blueprint in blueprint_list]
    for blueprint in blueprints_to_validate:
        blueprint_validate(blueprint, blueprint_id_filter(blueprint), skip_delete=True)


@pytest.fixture(scope='function', params=virtual_machine_list)
def basic_blueprint_test_with_getting_started_filter(request):
    _, infra_name = get_dirname_and_infra_name(request.param)
    blueprints_upload(request.param, 'infra-{0}'.format(infra_name))
    for blueprint_path in getting_started_list:
        blueprint_id = '{0}-{1}'.format(
            blueprint_id_filter(blueprint_path), infra_name)
        timeout = 1800 if infra_name == 'azure' else 600
        try:
            basic_blueprint_test(
                blueprint_path,
                blueprint_id,
                inputs='infra_name={0} -i infra_exists=true'.format(
                    infra_name),
                timeout=timeout,
                use_vpn='vsphere' in infra_name)
        except:
            cleanup_on_failure(blueprint_id)
            raise


@pytest.fixture(scope='function', params=openshift_list)
def openshift_test(request):
    try:
        basic_blueprint_test(
            request.param, blueprint_id_filter(request.param),
            inputs='namespace=blueprint-tests',
            timeout=3000)
    except:
        cleanup_on_failure(blueprint_id_filter(request.param))
        raise


def test_blueprint_validation():
    """All blueprints must pass DSL validation."""
    assert test_validate_blueprints() is None


def test_blueprint_validation_nightlies():
    """All blueprints must pass DSL validation."""
    assert test_validate_blueprints_nightlies() is None


def test_versions():
    """All blueprints in this branch should be the same Cloudify version.
    """
    try:
        assert get_cloudify_version() is not None
    except VersionsException as e:
        pytest.fail(
            "Failed to verify that branch "
            "versions are the same: {0}.".format(str(e)))


def test_getting_started(basic_blueprint_test_with_getting_started_filter):
    assert basic_blueprint_test_with_getting_started_filter is None


def test_openshift(openshift_test):
    assert openshift_test is None

