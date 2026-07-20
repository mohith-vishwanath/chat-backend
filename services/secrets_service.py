import os
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Ensure .env is loaded so os.getenv works locally
load_dotenv()

logger = logging.getLogger("uvicorn")

class SecretsService:
    REQUIRED_SECRETS = ["DATABASE_URL", "SECRET_KEY"]

    def __init__(self):
        self.env = os.getenv("ENV", "TEST")
        self.client = None
        self._secrets = {}
        if self.env == "PROD":
            region_name = os.getenv("AWS_REGION", "us-east-1")
            self.client = boto3.client("secretsmanager", region_name=region_name)

    def load_secrets(self):
        """
        Fetches all required secrets from the source and stores them locally in a dictionary.
        This ensures we read from the source just once.
        """
        logger.info("Loading secrets...")
        for secret_name in self.REQUIRED_SECRETS:
            if self.env == "TEST":
                val = os.getenv(secret_name)
                if val is None:
                    logger.warning(f"Secret '{secret_name}' not found in local environment.")
                self._secrets[secret_name] = val
            else:
                if not self.client:
                    logger.error("AWS SecretsManager client is not initialized.")
                    self._secrets[secret_name] = None
                    continue

                try:
                    response = self.client.get_secret_value(SecretId=secret_name)
                    if 'SecretString' in response:
                        self._secrets[secret_name] = response['SecretString']
                    else:
                        logger.error(f"Secret '{secret_name}' is not a string.")
                        self._secrets[secret_name] = None
                except ClientError as e:
                    logger.error(f"Unable to fetch secret '{secret_name}' from AWS Secrets Manager: {e}")
                    self._secrets[secret_name] = None
        logger.info("Finished loading secrets.")

    def get_secret(self, secret_name: str) -> str:
        """
        Retrieves a secret from the preloaded local dictionary.
        """
        if secret_name not in self._secrets:
            logger.warning(f"Secret '{secret_name}' was not preloaded.")
        return self._secrets.get(secret_name)

secrets_service = SecretsService()
