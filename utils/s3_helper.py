import boto3
from botocore.exceptions import ClientError
from config import Config


# AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY,
    region_name=Config.AWS_REGION
)


# Upload document to S3
def upload_file_to_s3(file, filename):

    print("Uploading:", filename)

    s3_client.upload_fileobj(
        file,
        Config.AWS_BUCKET_NAME,
        Config.AWS_DOCUMENT_FOLDER + filename
    )

    print("Upload completed")

# Upload profile photo to S3
def upload_profile_photo(file, filename):

    try:

        s3_client.upload_fileobj(
            file,
            Config.AWS_BUCKET_NAME,
            Config.AWS_PROFILE_FOLDER + filename
        )

        return True

    except ClientError as e:

        print("Profile Upload Error:", e)
        return False


# Delete document from S3
def delete_file_from_s3(filename):

    try:

        s3_client.delete_object(
            Bucket=Config.AWS_BUCKET_NAME,
            Key=Config.AWS_DOCUMENT_FOLDER + filename
        )

        return True

    except ClientError as e:

        print("Delete Error:", e)
        return False


# Delete profile photo from S3
def delete_profile_photo(filename):

    try:

        s3_client.delete_object(
            Bucket=Config.AWS_BUCKET_NAME,
            Key=Config.AWS_PROFILE_FOLDER + filename
        )

        return True

    except ClientError as e:

        print("Delete Profile Error:", e)
        return False


# Generate download URL for document
def get_file_url(filename):

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": Config.AWS_BUCKET_NAME,
            "Key": Config.AWS_DOCUMENT_FOLDER + filename
        },
        ExpiresIn=3600
    )


# Generate profile photo URL
def get_profile_photo_url(filename):

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": Config.AWS_BUCKET_NAME,
            "Key": Config.AWS_PROFILE_FOLDER + filename
        },
        ExpiresIn=3600
    )