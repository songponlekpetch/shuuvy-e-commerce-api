from firebase_admin import initialize_app, storage

from core.services.singleton import Singleton
from core.configs import FIREBASE_STORAGE_BUCKET_NAME

class FirebaseService(metaclass=Singleton):
    def __init__(self):
        self.app = initialize_app()

    def upload_file_to_storage(self, file, file_path, bucket_name=FIREBASE_STORAGE_BUCKET_NAME):
        bucket = storage.bucket(name=bucket_name, app=self.app)
        blob = bucket.blob(file_path)
        blob.upload_from_file(file)
        blob.make_public()

        return blob.public_url
