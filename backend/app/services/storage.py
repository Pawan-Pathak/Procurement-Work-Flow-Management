import os
from pathlib import Path
from typing import Tuple
import boto3
from werkzeug.datastructures import FileStorage
from flask import current_app


ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.doc', '.docx', '.xls', '.xlsx', '.csv'}


def is_allowed(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def save_file(file: FileStorage, *, subdir: str = '') -> Tuple[str, str]:
    """Save file to configured storage. Returns (public_url_or_key, storage_key)."""
    backend = current_app.config['FILE_STORAGE_BACKEND']
    if backend == 's3':
        return _save_to_s3(file, subdir=subdir)
    return _save_to_local(file, subdir=subdir)


def _save_to_local(file: FileStorage, *, subdir: str = '') -> Tuple[str, str]:
    upload_dir = Path(current_app.config['FILE_UPLOAD_DIR']) / subdir
    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = file.filename or 'upload'
    safe_name = filename.replace('/', '_')
    dest = upload_dir / safe_name
    file.save(dest)
    return (dest.as_posix(), dest.relative_to(Path(current_app.config['FILE_UPLOAD_DIR'])).as_posix())


def _save_to_s3(file: FileStorage, *, subdir: str = '') -> Tuple[str, str]:
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_S3_REGION'],
    )
    bucket = current_app.config['AWS_S3_BUCKET']
    filename = file.filename or 'upload'
    key = f"{subdir}/{filename}"
    s3.upload_fileobj(file, bucket, key, ExtraArgs={'ACL': 'private'})
    return (f"s3://{bucket}/{key}", key)