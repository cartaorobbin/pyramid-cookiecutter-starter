import json
import pytest

from conductor.client.http.api.task_resource_api import ApiClient
import socket

# @pytest.fixture()
# def mocke_conductor_worker(mocker, task_poll_response):

#     def inner(**kwargs):
#         mocker.patch('conductor.client.http.api.task_resource_api.ApiClient.request', return_value=task_poll_response(kwargs))

#     return inner


@pytest.fixture
def task_poll_response():
    def inner(input_data, task_name="celery_test_task"):
        worker_id = socket.gethostname()

        data = (
            '{"taskType":"celery_test_task","status":"IN_PROGRESS","inputData":"","referenceTaskName":"celery_test_task_ref","retryCount":0,"seq":1,"pollCount":1,"taskDefName":"celery_test_task","scheduledTime":1691960284387,"startTime":1691960484581,"endTime":0,"updateTime":1691960484582,"startDelayInSeconds":0,"retried":false,"executed":false,"callbackFromWorker":true,"responseTimeoutSeconds":3600,"workflowInstanceId":"18bfeabf-3a1c-11ee-868b-06fd3bd0ae8b","workflowType":"celery_test_workflow","taskId":"18c0fc30-3a1c-11ee-868b-06fd3bd0ae8b","callbackAfterSeconds":0,"workerId":"localhost","outputData":{},"workflowTask":{"name":"celery_test_task","taskReferenceName":"celery_test_task_ref","description":null,"inputParameters":{"http_request":{"uri":"https://datausa.io/api/data?drilldowns=Nation&measures=Population","method":"GET"}},"type":"SIMPLE","dynamicTaskNameParam":null,"caseValueParam":null,"caseExpression":null,"scriptExpression":null,"dynamicForkJoinTasksParam":null,"dynamicForkTasksParam":null,"dynamicForkTasksInputParamName":null,"startDelay":0,"subWorkflowParam":null,"sink":null,"optional":false,"taskDefinition":{"ownerApp":null,"createTime":1691935582212,"updateTime":null,"createdBy":"","updatedBy":null,"name":"celery_test_task","description":"shipping'
            ' Workflow","retryCount":3,"timeoutSeconds":0,"inputKeys":[],"outputKeys":[],"timeoutPolicy":"ALERT_ONLY","retryLogic":"FIXED","retryDelaySeconds":60,"responseTimeoutSeconds":3600,"concurrentExecLimit":null,"inputTemplate":{},"rateLimitPerFrequency":0,"rateLimitFrequencyInSeconds":1,"isolationGroupId":null,"executionNameSpace":null,"ownerEmail":"tomas.correa@gmail.com","pollTimeoutSeconds":null,"backoffScaleFactor":1},"rateLimited":null,"asyncComplete":false,"loopCondition":null,"retryCount":null,"evaluatorType":null,"expression":null},"rateLimitPerFrequency":0,"rateLimitFrequencyInSeconds":1,"workflowPriority":0,"iteration":0,"subworkflowChanged":false,"queueWaitTime":200194,"loopOverTask":false,"taskDefinition":{"ownerApp":null,"createTime":1691935582212,"updateTime":null,"createdBy":"","updatedBy":null,"name":"celery_test_task","description":"shipping'
            ' Workflow","retryCount":3,"timeoutSeconds":0,"inputKeys":[],"outputKeys":[],"timeoutPolicy":"ALERT_ONLY","retryLogic":"FIXED","retryDelaySeconds":60,"responseTimeoutSeconds":3600,"concurrentExecLimit":null,"inputTemplate":{},"rateLimitPerFrequency":0,"rateLimitFrequencyInSeconds":1,"isolationGroupId":null,"executionNameSpace":null,"ownerEmail":"tomas.correa@gmail.com","pollTimeoutSeconds":null,"backoffScaleFactor":1}}'
        )
        data = data.replace("celery_test_task", task_name)
        response = json.loads(data)
        response["inputData"] = input_data
        response["workerId"] = worker_id
        return json.dumps(response)

    return inner
