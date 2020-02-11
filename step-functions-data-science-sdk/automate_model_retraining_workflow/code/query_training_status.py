import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
sm_client = boto3.client('sagemaker')

#Retrieve transform job name from event and return transform job status.
def lambda_handler(event, context):

    if ('TrainingJobName' in event):
        job_name = event['TrainingJobName']

    else:
        raise KeyError('Input must include TrainingJobName key!')

    #Query boto3 API to check training status.
    try:
        response = sm_client.describe_training_job(TrainingJobName=job_name)
        logger.info("Training job:{} has status:{}.".format(job_name,
            response['TrainingJobStatus']))

    except Exception as e:
        response = 'Failed to read training status!'
        print(e)
        print(response +' Attempted to read job name: {}'.format(job_name))

    #We can't marshall datetime objects in JSON response. So convert
    #all datetime objects returned to unix time.
    for index, metric in enumerate(response['FinalMetricDataList']):
        metric['Timestamp'] = metric['Timestamp'].timestamp()

    return {
        'statusCode': 200,
        'trainingMetrics': response['FinalMetricDataList']
    }
