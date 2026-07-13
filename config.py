import os


class Config:

    # Flask Secret Key
    SECRET_KEY = "myvault_secret_key_2026"

    # MySQL Configuration
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "sairam0719"
    MYSQL_DB = "personal_vault"

    # File Upload Configuration
    UPLOAD_FOLDER = "uploads"
    PROFILE_FOLDER = "static/profile_images"

    # Mail Configuration (Forgot Password OTP)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "himavanthsairamkostu@gmail.com"
    MAIL_PASSWORD = "xlzh vgcv qprp jrsn"

    # AWS S3 Configuration
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECERT_KEY")
    AWS_REGION = "ap-south-1"
    AWS_BUCKET_NAME = "myvault-personal-vault"

    # AWS S3 Folder Names
    AWS_DOCUMENT_FOLDER = "documents/"
    AWS_PROFILE_FOLDER = "profile_images/"