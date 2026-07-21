import json
import logging
import boto3
from botocore.exceptions import ClientError
from core.config import settings

logger = logging.getLogger(__name__)

class SQSService:
    def __init__(self):
        self.sqs = boto3.client('sqs')
        self.queue_name = settings.SQS_QUEUE_NAME
        self.queue_url = None

    def _get_queue_url(self):
        if not self.queue_name:
            raise ValueError("SQS_QUEUE_NAME environment variable is not set")
            
        if self.queue_url:
            return self.queue_url
            
        try:
            response = self.sqs.get_queue_url(QueueName=self.queue_name)
            self.queue_url = response['QueueUrl']
            return self.queue_url
        except ClientError as e:
            logger.error(f"Error getting queue URL for {self.queue_name}: {e}")
            raise

    def push_message(self, payload: dict):
        """
        Pushes a message with a payload into the SQS queue.
        """
        try:
            queue_url = self._get_queue_url()
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(payload)
            )
            return response
        except ClientError as e:
            logger.error(f"Error pushing message to {self.queue_name}: {e}")
            raise

sqs_service = SQSService()
