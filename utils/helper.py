import boto3
from config import Config


# Create S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY,
    region_name=Config.AWS_REGION
)


# Upload File to S3
def upload_file_to_s3(file, filename):

    s3.upload_fileobj(
        file,
        Config.AWS_BUCKET_NAME,
        filename
    )


# Delete File from S3
def delete_file_from_s3(filename):

    s3.delete_object(
        Bucket=Config.AWS_BUCKET_NAME,
        Key=filename
    )


# Generate Download URL
def get_file_url(filename):

    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": Config.AWS_BUCKET_NAME,
            "Key": filename
        },
        ExpiresIn=3600
    )

    return url