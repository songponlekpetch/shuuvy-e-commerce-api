import boto3

from core.services.singleton import Singleton

class DigitalOceanService(Singleton):
    def __init__(self, region_name, endpoint_url, access_key_id, secret_access_key, space_name):
        self.client = self.get_spaces_client(
            region_name,
            endpoint_url,
            access_key_id,
            secret_access_key)
        self.space_name = space_name

    def get_spaces_client(self, region_name, endpoint_url, access_key_id, secret_access_key):
        session = boto3.session.Session()

        return session.client(
            's3',
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )

    def upload_file_to_storage(self, file, storage_path):
        self.client.put_object(**{
            "Bucket": self.space_name,
            "Body": file,
            "Key": storage_path,
            "ACL": "public-read",
            "ContentType": "image/*"
        })

        return storage_path
