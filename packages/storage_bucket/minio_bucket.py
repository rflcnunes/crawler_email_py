import os

from dotenv import load_dotenv
from minio import Minio


class MinioBucket:
    def __init__(self):
        load_dotenv()
        self.ACCESS_KEY = os.environ.get('ACCESS_KEY')
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.HOST = os.environ.get('MINIO_HOST')
        self.MINIO_CLIENT = Minio(self.HOST, access_key=self.ACCESS_KEY,
                                  secret_key=self.SECRET_KEY, secure=False)

    def list_buckets(self):
        try:
            return self.MINIO_CLIENT.list_buckets()
        except Exception as e:
            print(e)

    def upload_file(self, bucket_name, file_name, file_path):
        try:
            print(f" [x] Bucket: {bucket_name}, File: {file_name}, Path: {file_path}")
            return self.MINIO_CLIENT.fput_object(bucket_name, file_name, file_path)
        except Exception as e:
            print(f" [ ] Error: {e}")
