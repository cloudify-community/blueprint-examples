/*-
 * ============LICENSE_START=================================================
 * ONAP - SO
 * ==========================================================================
 * Copyright (C) 2019 Cloudify Platform Ltd. All rights reserved.
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

import org.junit.*;
import org.junit.runner.RunWith;
import static org.mockito.Mockito.*;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpEntity;
import org.springframework.web.client.RestTemplate;
import co.cloudify.client.APIV31.Visibility;
import co.cloudify.client.APIV31Impl.BlueprintListV31;

@RunWith(MockitoJUnitRunner.class)
public class APIV31Test {

    @Mock
    private RestTemplate restTemplate;

    @Test
    public void testCreateBlueprint() {
        APIV31Impl.restTemplate = restTemplate;
        APIV31Impl api = APIV31Impl.create("a", "b", "c", "d", 0);

        ResponseEntity<String> re = new ResponseEntity<>(HttpStatus.ACCEPTED);

        when(restTemplate.exchange(anyString(), eq(HttpMethod.PUT), any(HttpEntity.class), eq(String.class), any(),
                any(), any())).thenReturn(re);

        api.uploadBlueprint("test", "test.yaml", Visibility.PRIVATE, new byte[1]);

        verify(restTemplate).exchange(contains("/blueprints"), eq(HttpMethod.PUT), any(HttpEntity.class),
                eq(String.class), eq("test"), eq("test.yaml"), eq("private"));
    }

    @Test
    public void testDeleteBlueprint() {
        APIV31Impl.restTemplate = restTemplate;
        APIV31Impl api = APIV31Impl.create("a", "b", "c", "d", 0);

        ResponseEntity<BlueprintV31> re = new ResponseEntity<>(HttpStatus.ACCEPTED);

        when(restTemplate.exchange(anyString(), eq(HttpMethod.DELETE), any(HttpEntity.class), eq(BlueprintV31.class),
                any(), any())).thenReturn(re);

        api.deleteBlueprint("test", false);

        verify(restTemplate).exchange(contains("/blueprints"), eq(HttpMethod.DELETE), any(HttpEntity.class),
                eq(BlueprintV31.class), eq("test"), eq(false));
    }

    @Test
    public void testGetBlueprint() {
        APIV31Impl.restTemplate = restTemplate;
        APIV31Impl api = APIV31Impl.create("a", "b", "c", "d", 0);

        ResponseEntity<BlueprintV31> re = new ResponseEntity<>(HttpStatus.ACCEPTED);

        when(restTemplate.exchange(contains("/blueprints"), eq(HttpMethod.GET), any(HttpEntity.class),
                eq(BlueprintV31.class), eq("test"))).thenReturn(re);

        api.getBlueprint("test");

        verify(restTemplate).exchange(contains("/blueprints"), eq(HttpMethod.GET), any(HttpEntity.class),
                eq(BlueprintV31.class), eq("test"));
    }

    @Test
    public void testListBlueprints() {
        APIV31Impl.restTemplate = restTemplate;
        APIV31Impl api = APIV31Impl.create("a", "b", "c", "d", 0);

        BlueprintListV31 body = new BlueprintListV31();
        ResponseEntity<BlueprintListV31> re = new ResponseEntity<>(body, HttpStatus.ACCEPTED);
        when(restTemplate.exchange(contains("/blueprints"), eq(HttpMethod.GET), any(HttpEntity.class),
                eq(BlueprintListV31.class))).thenReturn(re);

        api.listBlueprints();

        verify(restTemplate).exchange(endsWith("/blueprints"), eq(HttpMethod.GET), any(HttpEntity.class),
                eq(BlueprintListV31.class));
    }
}
