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

import java.util.Date;

public class ExecutionV31 {
    private String id;
    private String blueprint_id;
    private Date created_at;
    private Date ended_at;
    private String created_by;
    private String deployment_id;
    private String error;
    private boolean is_system_workflow;
    private String status;
    private String tenant_name;
    private String workflow_id;
    private Date started_at;
    private Date scheduled_for;

    /**
     * @return the id
     */
    public String getId() {
        return id;
    }

    /**
     * @param id the id to set
     */
    public void setId(String id) {
        this.id = id;
    }

    /**
     * @return the blueprint_id
     */
    public String getBlueprint_id() {
        return blueprint_id;
    }

    /**
     * @param blueprint_id the blueprint_id to set
     */
    public void setBlueprint_id(String blueprint_id) {
        this.blueprint_id = blueprint_id;
    }

    /**
     * @return the created_at
     */
    public Date getCreated_at() {
        return created_at;
    }

    /**
     * @param created_at the created_at to set
     */
    public void setCreated_at(Date created_at) {
        this.created_at = created_at;
    }

    /**
     * @return the ended_at
     */
    public Date getEnded_at() {
        return ended_at;
    }

    /**
     * @param ended_at the ended_at to set
     */
    public void setEnded_at(Date ended_at) {
        this.ended_at = ended_at;
    }

    /**
     * @return the created_by
     */
    public String getCreated_by() {
        return created_by;
    }

    /**
     * @param created_by the created_by to set
     */
    public void setCreated_by(String created_by) {
        this.created_by = created_by;
    }

    /**
     * @return the deployment_id
     */
    public String getDeployment_id() {
        return deployment_id;
    }

    /**
     * @param deployment_id the deployment_id to set
     */
    public void setDeployment_id(String deployment_id) {
        this.deployment_id = deployment_id;
    }

    /**
     * @return the error
     */
    public String getError() {
        return error;
    }

    /**
     * @param error the error to set
     */
    public void setError(String error) {
        this.error = error;
    }

    /**
     * @return the is_system_workflow
     */
    public boolean isIs_system_workflow() {
        return is_system_workflow;
    }

    /**
     * @param is_system_workflow the is_system_workflow to set
     */
    public void setIs_system_workflow(boolean is_system_workflow) {
        this.is_system_workflow = is_system_workflow;
    }

    /**
     * @return the status
     */
    public String getStatus() {
        return status;
    }

    /**
     * @param status the status to set
     */
    public void setStatus(String status) {
        this.status = status;
    }

    /**
     * @return the tenant_name
     */
    public String getTenant_name() {
        return tenant_name;
    }

    /**
     * @param tenant_name the tenant_name to set
     */
    public void setTenant_name(String tenant_name) {
        this.tenant_name = tenant_name;
    }

    /**
     * @return the workflow_id
     */
    public String getWorkflow_id() {
        return workflow_id;
    }

    /**
     * @param workflow_id the workflow_id to set
     */
    public void setWorkflow_id(String workflow_id) {
        this.workflow_id = workflow_id;
    }

    /**
     * @return the started_at
     */
    public Date getStarted_at() {
        return started_at;
    }

    /**
     * @param started_at the started_at to set
     */
    public void setStarted_at(Date started_at) {
        this.started_at = started_at;
    }

    /**
     * @return the scheduled_for
     */
    public Date getScheduled_for() {
        return scheduled_for;
    }

    /**
     * @param scheduled_for the scheduled_for to set
     */
    public void setScheduled_for(Date scheduled_for) {
        this.scheduled_for = scheduled_for;
    }
}
