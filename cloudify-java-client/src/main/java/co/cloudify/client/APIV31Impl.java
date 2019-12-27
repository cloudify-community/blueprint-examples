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

import java.nio.charset.Charset;
import java.util.Base64;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

public class APIV31Impl implements APIV31 {
    protected static RestTemplate restTemplate;
    private String basicAuthHeader;
    private HttpHeaders basicHeaders = new HttpHeaders();
    private HttpEntity basicEntity;
    private String basePath; // cached URL base
    private String tenant;

    protected APIV31Impl() {}

    /**
     * Basic authorization based constructor
     */
    public static APIV31Impl create(String tenant, String user, String password, String host, int port) {
        return create(tenant, user, password, "http://" + host + ":" + port);
    }

    public static APIV31Impl create(String tenant, String user, String password, String manager_url) {
        APIV31Impl api = new APIV31Impl();
        String auth = user + ":" + password;
        byte[] encodedAuth = Base64.getEncoder().encode(auth.getBytes(Charset.forName("US-ASCII")));
        if (api.restTemplate == null) {
            api.restTemplate = new RestTemplate();
        }
        api.basicAuthHeader = "Basic " + new String(encodedAuth);
        api.tenant = tenant;
        api.basicHeaders.add("Authorization", api.basicAuthHeader);
        api.basicHeaders.add("Tenant", tenant);
        api.basicEntity = new HttpEntity(api.basicHeaders);
        api.basePath = manager_url + "/api/v3.1";
        return api;

    }

    /**
     * Get a single blueprint
     */
    @Override
    public BlueprintV31 getBlueprint(String id) {
        ResponseEntity<BlueprintV31> bpe = restTemplate.exchange(basePath + "/blueprints/{blueprint_id}",
                HttpMethod.GET, basicEntity, BlueprintV31.class, id);
        if (bpe.getStatusCodeValue() < 200 && bpe.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + bpe.getStatusCodeValue());
        }
        return bpe.getBody();
    }

    /**
     * Get a list of blueprints
     */
    @Override
    public List<BlueprintV31> listBlueprints() {
        ResponseEntity<BlueprintListV31> bpe =
                restTemplate.exchange(basePath + "/blueprints", HttpMethod.GET, basicEntity, BlueprintListV31.class);
        if (bpe.getStatusCodeValue() < 200 && bpe.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + bpe.getStatusCodeValue());
        }
        return bpe.getBody().items;

    }

    @Override
    public void deleteBlueprint(String id, Boolean force) {
        ResponseEntity<BlueprintV31> bpe = restTemplate.exchange(basePath + "/blueprints/{blueprint_id}?force={force}",
                HttpMethod.DELETE, basicEntity, BlueprintV31.class, id, force);
        if (bpe.getStatusCodeValue() < 200 && bpe.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + bpe.getStatusCodeValue());
        }
        return;

    }

    /**
     * Upload a blueprint
     */
    @Override
    public void uploadBlueprint(String blueprint_id, String main_yaml_filename, Visibility visibility, byte[] archive) {
        HttpHeaders headers = cloneHeaders(basicEntity.getHeaders());
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        HttpEntity<?> entity = new HttpEntity<byte[]>(archive, headers);

        ResponseEntity resp = restTemplate.exchange(
                basePath + "/blueprints/{blueprint_id}?application_file_name={yaml_file}&visibility={vis}",
                HttpMethod.PUT, entity, String.class, blueprint_id, main_yaml_filename, visibility.toString());

        if (resp.getStatusCodeValue() < 200 && resp.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + resp.getStatusCodeValue());
        }
    }

    @Override
    public DeploymentV31 getDeployment(String id) {
        ResponseEntity<DeploymentListV31> dep = restTemplate.exchange(basePath + "/deployments?id={deployment_id}",
                HttpMethod.GET, basicEntity, DeploymentListV31.class, id);
        if (dep.getStatusCodeValue() < 200 && dep.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + dep.getStatusCodeValue());
        }
        return dep.getBody().items.get(0);
    }

    @Override
    public List<DeploymentV31> listDeployments() {
        ResponseEntity<DeploymentListV31> dep =
                restTemplate.exchange(basePath + "/deployments", HttpMethod.GET, basicEntity, DeploymentListV31.class);
        if (dep.getStatusCodeValue() < 200 && dep.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + dep.getStatusCodeValue());
        }
        return dep.getBody().items;
    }

    /**
     * Create a deployment. Note this is a synchronous call
     */
    @Override
    public DeploymentV31 createDeployment(String id, String blueprint_id, Map<String, String> inputs,
            Boolean private_resource, Boolean skip_val, Visibility visibility) {
        HttpHeaders headers = cloneHeaders(basicEntity.getHeaders());
        headers.setContentType(MediaType.APPLICATION_JSON);
        CreateDeploymentBody body = new CreateDeploymentBody();
        body.setBlueprint_id(blueprint_id);
        body.setInputs(inputs);
        body.setPrivate_resource(private_resource);
        body.setVisibility(visibility.toString());
        ObjectMapper mapper = new ObjectMapper();
        String json = null;
        try {
            mapper.setSerializationInclusion(Include.NON_NULL);
            mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
            json = mapper.writeValueAsString(body);
        } catch (Exception e) {
            throw new RuntimeException("mashalling error");
        }
        HttpEntity<String> entity = new HttpEntity<>(json, headers);

        ResponseEntity<DeploymentV31> resp = restTemplate.exchange(basePath + "/deployments/{deployment_id}",
                HttpMethod.PUT, entity, DeploymentV31.class, id);

        // Now wait for execution to finish
        for (int i = 0; i < 20; i++) {
            List<ExecutionV31> exs = this.listExecutions(id);
            if (exs.size() != 1) {
                throw new RuntimeException("internal error, found " + exs.size() + " executions found for deployment "
                        + id + ". Expected 1");
            }
            String status = exs.get(0).getStatus();
            if (status.equals("terminated")) {
                return resp.getBody(); // nominal
            }
            if (status.equals("error")) {
                throw new RuntimeException("Deployment creation failed");
            }
            if (status.equals("cancelled")) {
                throw new RuntimeException("Deployment creation cancelled");
            }
            try {
                Thread.sleep(3000);
            } catch (Exception e) {
            } ;
        }
        throw new RuntimeException("Deployment creation timed out");

    }

    @Override
    public DeploymentV31 deleteDeployment(String deployment_id, Boolean ignore_live_nodes) {
        HttpHeaders headers = cloneHeaders(basicEntity.getHeaders());
        String body = "{}";
        if (ignore_live_nodes != null && ignore_live_nodes) {
            body = "{\"ignore_live_nodes\": \"true\"}";
        }
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<>(body, headers);

        ResponseEntity<DeploymentV31> resp = restTemplate.exchange(basePath + "/deployments/{deployment_id}",
                HttpMethod.DELETE, entity, DeploymentV31.class, deployment_id);
        if (resp.getStatusCodeValue() < 200 && resp.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + resp.getStatusCodeValue());
        }
        for(int i=0;i<10;i++) {
        	try {
        		Thread.sleep(1000L);
        	}
        	catch(Exception e) {
                throw new RuntimeException("sleep interrupted during delete for '"+deployment_id+"'");
        	}
        	try {
        		this.getDeployment(deployment_id);
        	}
        	catch(Exception e) {
                return resp.getBody();
        	}
        }
        throw new RuntimeException("Deployment delete for '"+deployment_id+"' timed out");
    }

    @Override
    public ExecutionV31 getExecution(String id) {
        ResponseEntity<ExecutionV31> dep = restTemplate.exchange(basePath + "/executions/{id}",
                HttpMethod.GET, basicEntity, ExecutionV31.class, id);
        if (dep.getStatusCodeValue() < 200 && dep.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + dep.getStatusCodeValue());
        }
        return dep.getBody();
    }

    @Override
    public List<ExecutionV31> listExecutions() {
        return this._listExecutions(null);
    }

    @Override
    public List<ExecutionV31> listExecutions(String deployment_id) {
        return this._listExecutions(deployment_id);
    }

    @Override
    public ExecutionV31 startExecution(String workflow_id, String deployment_id, Map<String, String> parameters,
            Boolean allow_custom_parameters, Boolean force, Boolean queue, Calendar schedule) {
        HttpHeaders headers = cloneHeaders(basicEntity.getHeaders());
        headers.setContentType(MediaType.APPLICATION_JSON);
        StartExecutionBody body = new StartExecutionBody();
        body.setAllow_custom_parameters(allow_custom_parameters);
        body.setDeployment_id(deployment_id);
        body.setForce(force);
        body.setParameters(parameters);
        body.setQueue(queue);
        body.setSchedule(schedule);
        body.setWorkflow_id(workflow_id);
        ObjectMapper mapper = new ObjectMapper();
        String json = null;
        try {
            mapper.setSerializationInclusion(Include.NON_NULL);
            mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
            json = mapper.writeValueAsString(body);
        } catch (Exception e) {
            throw new RuntimeException("mashalling error");
        }
        HttpEntity<String> entity = new HttpEntity<>(json, headers);

        ResponseEntity<ExecutionV31> resp =
                restTemplate.exchange(basePath + "/executions", HttpMethod.POST, entity, ExecutionV31.class);

        if (resp.getStatusCodeValue() < 200 && resp.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + resp.getStatusCodeValue());
        }
        return resp.getBody();
    }


    @Override
    public ExecutionV31 runExecution(String workflow_id, String deployment_id, Map<String, String> parameters,
            Boolean allow_custom_parameters, Boolean force, Boolean queue, Calendar schedule, int timeout_sec,
            boolean cancel) {

        ExecutionV31 ex =
                startExecution(workflow_id, deployment_id, parameters, allow_custom_parameters, force, queue, schedule);

        long now = new Date().getTime();
        long then = now + (long) timeout_sec * 1000L;

        while (new Date().getTime() < then) {
            ex = getExecution(ex.getId());
            if (ex.getStatus().equals(ExecutionStatus.STATUS_CANCELLED.toString())
                    || ex.getStatus().equals(ExecutionStatus.STATUS_TERMINATED.toString())
                    || ex.getStatus().equals(ExecutionStatus.STATUS_FAILED.toString())) {
                return ex;
            }
            try {
            	Thread.sleep(1000L);
            }
            catch(Exception e) {}
        }
        if (cancel) {
            this.cancelExecution(ex.getId(), false);
            for (int i = 0; i < 10; i++) {
                try {
                    Thread.sleep(2000);
                } catch (Exception e) {
                }
                ex = getExecution(ex.getId());
                if (ex.getStatus().equals(ExecutionStatus.STATUS_CANCELLED)) {
                    return ex;
                }
            }
            throw new RuntimeException("Execution cancel timed out after 20 seconds");
        }

        return ex;
    }


    @Override
    public ExecutionV31 cancelExecution(String execution_id, Boolean force) {
        HttpHeaders headers = cloneHeaders(basicEntity.getHeaders());
        headers.setContentType(MediaType.APPLICATION_JSON);
        String body = "{\"action\": \"cancel\"}";
        if (force != null && force) {
            body = "{\"action\": \"force-cancel\"}";
        }
        HttpEntity<String> entity = new HttpEntity<>(body, headers);
        ResponseEntity<ExecutionV31> resp = restTemplate.exchange(basePath + "/executions/{execution_id}",
                HttpMethod.POST, entity, ExecutionV31.class, execution_id);
        return resp.getBody();
    }

    /**
     * PRIVATE
     */

    private HttpHeaders cloneHeaders(HttpHeaders headers) {
        HttpHeaders out_headers = new HttpHeaders();
        for (MultiValueMap.Entry<String, List<String>> entry : headers.entrySet()) {
            for (String v : entry.getValue()) {
                out_headers.add(entry.getKey(), v);
            }
        }
        return out_headers;
    }

    /**
     * General purpose list executions method
     */
    private List<ExecutionV31> _listExecutions(String deployment_id) {
        String filters = "";
        if (deployment_id != null && deployment_id.length() > 0) {
            filters = "?deployment_id=" + deployment_id;
        }
        String path = "/executions" + filters;
        ResponseEntity<ExecutionListV31> exs =
                restTemplate.exchange(basePath + path, HttpMethod.GET, basicEntity, ExecutionListV31.class);
        if (exs.getStatusCodeValue() < 200 && exs.getStatusCodeValue() > 299) {
            throw new RuntimeException("Invalid response code received: " + exs.getStatusCodeValue());
        }
        return exs.getBody().items;
    }

    protected static class BlueprintListV31 {
        private List<BlueprintV31> items;

        /**
         * @return the items
         */
        public List<BlueprintV31> getItems() {
            return items;
        }

        /**
         * @param items the items to set
         */
        public void setItems(List<BlueprintV31> items) {
            this.items = items;
        }

    }

    protected static class DeploymentListV31 {
        private List<DeploymentV31> items;

        /**
         * @return the items
         */
        public List<DeploymentV31> getItems() {
            return items;
        }

        /**
         * @param items the items to set
         */
        public void setItems(List<DeploymentV31> items) {
            this.items = items;
        }
    }

    protected static class ExecutionListV31 {
        private List<ExecutionV31> items;

        /**
         * @return the items
         */
        public List<ExecutionV31> getItems() {
            return items;
        }

        /**
         * @param items the items to set
         */
        public void setItems(List<ExecutionV31> items) {
            this.items = items;
        }
    }

    protected static class StartExecutionBody {
        private String workflow_id;
        private String deployment_id;
        private Boolean allow_custom_parameters;
        private Map<String, String> parameters;
        private Boolean force = false;
        private Boolean queue = true;
        private Calendar schedule;

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
         * @return the allow_custom_parameters
         */
        public Boolean isAllow_custom_parameters() {
            return allow_custom_parameters;
        }

        /**
         * @param allow_custom_parameters the allow_custom_parameters to set
         */
        public void setAllow_custom_parameters(Boolean allow_custom_parameters) {
            this.allow_custom_parameters = allow_custom_parameters;
        }

        /**
         * @return the parameters
         */
        public Map<String, String> getParameters() {
            return parameters;
        }

        /**
         * @param parameters the parameters to set
         */
        public void setParameters(Map<String, String> parameters) {
            this.parameters = parameters;
        }

        /**
         * @return the force
         */
        public Boolean isForce() {
            return force;
        }

        /**
         * @param force the force to set
         */
        public void setForce(Boolean force) {
            this.force = force;
        }

        /**
         * @return the queue
         */
        public Boolean isQueue() {
            return queue;
        }

        /**
         * @param queue the queue to set
         */
        public void setQueue(Boolean queue) {
            this.queue = queue;
        }

        /**
         * @return the schedule
         */
        public Calendar getSchedule() {
            return schedule;
        }

        /**
         * @param schedule the schedule to set
         */
        public void setSchedule(Calendar schedule) {
            this.schedule = schedule;
        }
    }

    protected static class CreateDeploymentBody {
        private String blueprint_id;
        private Map<String, String> inputs;
        private Boolean private_resource;
        private Boolean skip_plugins_validation;
        private String visibility;

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
         * @return the inputs
         */
        public Map<String, String> getInputs() {
            return inputs;
        }

        /**
         * @param inputs the inputs to set
         */
        public void setInputs(Map<String, String> inputs) {
            this.inputs = inputs;
        }

        /**
         * @return the private_resource
         */
        public Boolean isPrivate_resource() {
            return private_resource;
        }

        /**
         * @param private_resource the private_resource to set
         */
        public void setPrivate_resource(Boolean private_resource) {
            this.private_resource = private_resource;
        }

        /**
         * @return the skip_plugins_validation
         */
        public Boolean isSkip_plugins_validation() {
            return skip_plugins_validation;
        }

        /**
         * @param skip_plugins_validation the skip_plugins_validation to set
         */
        public void setSkip_plugins_validation(boolean skip_plugins_validation) {
            this.skip_plugins_validation = skip_plugins_validation;
        }

        /**
         * @return the visibility
         */
        public String getVisibility() {
            return visibility;
        }

        /**
         * @param visibility the visibility to set
         */
        public void setVisibility(String visibility) {
            this.visibility = visibility;
        }
    }

}
