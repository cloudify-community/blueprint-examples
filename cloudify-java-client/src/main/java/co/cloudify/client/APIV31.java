/*-
 * ============LICENSE_START=================================================
 * Cloudify Client
 * ==========================================================================
 * Copyright (C) 2019 Cloudify Platform Ltd All rights reserved.
 * ==========================================================================
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============LICENSE_END===================================================
 */
package co.cloudify.client;

import java.util.Calendar;
import java.util.List;
import java.util.Map;

public interface APIV31 {
    public enum Visibility {
        PRIVATE("private"), TENANT("tenant"), PUBLIC("public");

        Visibility(String name) {
            this.name = name;
        }

        private String name;

        public String toString() {
            return this.name;
        }
    }
    public enum ExecutionStatus {
        STATUS_FAILED("failed"),
        STATUS_TERMINATED("terminated"),
        STATUS_CANCELLED("cancelled"),
        STATUS_STARTED("started"),
        STATUS_PENDING("pending"),
        STATUS_SCHEDULED("scheduled"),
        STATUS_CANCELLING("cancelling");

        private String name;

        ExecutionStatus(String name) {
            this.name = name;
        }

        public String toString() {
            return this.name;
        }
    }

    /**
     * Get a blueprint by id
     */
    BlueprintV31 getBlueprint(String id);

    /**
     * Delete a blueprint
     */
    void deleteBlueprint(String id, Boolean force);

    /**
     * List all blueprints
     */
    List<BlueprintV31> listBlueprints();

    /**
     * Upload a blueprint
     */
    void uploadBlueprint(String blueprint_id, String main_yaml_filename, Visibility visibility, byte[] archive);

    /**
     * Get a deployment by id
     */
    DeploymentV31 getDeployment(String id);

    /**
     * List all deployments
     */
    List<DeploymentV31> listDeployments();

    /**
     * Create a deployment
     */
    DeploymentV31 createDeployment(String id, String blueprint_id, Map<String, String> inputs, Boolean private_resource,
            Boolean skip_val, Visibility visibility);

    /**
     * Delete a deployment
     */
    DeploymentV31 deleteDeployment(String deployment_id, Boolean ignore_live_nodes);

    /**
     * Get an execution by id
     */
    ExecutionV31 getExecution(String id);

    /**
     * Get all executions
     */
    List<ExecutionV31> listExecutions();

    /**
     * Get all executions for deployment
     */
    List<ExecutionV31> listExecutions(String deployment_id);

    /**
     * Start an execution
     */
    ExecutionV31 startExecution(String workflow_id, String deployment_id, Map<String, String> parameters,
            Boolean allow_custom_parameters, Boolean force, Boolean queue, Calendar schedule);

    /**
     * Run execution synchronously
     */
    ExecutionV31 runExecution(String workflow_id, String deployment_id, Map<String, String> parameters,
            Boolean allow_custom_parameters, Boolean force, Boolean queue, Calendar schedule, int timeout_sec,
            boolean cancel);

    /**
     * Cancel an execution
     */
    ExecutionV31 cancelExecution(String execution_id, Boolean force);
}
