import boto3
import os
import time
import fnmatch
from botocore.exceptions import ClientError
from modules.logger import Logger

class AWSConn():
    def __init__(self):
        timeout_seconds = 15
        timeout_start = time.time()
        self.logger = Logger()

        session = None
        while not session and time.time() < timeout_start + timeout_seconds:
            try:
                session = boto3.Session()
                self.s3_resource = session.resource('s3')
                self.s3_resource_client = self.s3_resource.meta.client
                self.s3_client = session.client('s3')
                self.secrets_client = session.client('secretsmanager')
            except Exception as e:
                session = None

    def get_secret_value(self, secret_name):
        try:
            secret_value = self.secrets_client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            self.logger.error("Error during getting secret value: {}".format(e))
            return None

        return secret_value['SecretString']