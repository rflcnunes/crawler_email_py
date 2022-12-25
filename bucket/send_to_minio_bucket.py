import os

from dotenv import load_dotenv
from minio import Minio

load_dotenv()
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
HOST = os.environ.get('MINIO_HOST')
MINIO_CLIENT = Minio(HOST, access_key=ACCESS_KEY,
                     secret_key=SECRET_KEY, secure=False)


def list_buckets():
    try:
        return MINIO_CLIENT.list_buckets()
    except Exception as e:
        print(e)


def upload_file(bucket_name, file_name, file_path):
    try:
        print(f" [x] Bucket: {bucket_name}, File: {file_name}, Path: {file_path}")
        return MINIO_CLIENT.fput_object(bucket_name, file_name, file_path)
    except Exception as e:
        print(f" [ ] Error: {e}")
