# MyVault – Personal Digital Vault

## Overview

MyVault is a secure web application developed using Python, Flask, HTML, CSS, MySQL, Amazon EC2, and Amazon S3. The application enables users to securely upload, store, and manage important personal documents in a centralized digital vault. It provides a simple and secure interface for managing user profiles and documents while leveraging cloud services for reliable storage and deployment.

---

## Features

- User Registration
- Secure User Login and Logout
- Password Hashing for Authentication
- User Dashboard
- Profile Management
- Document Upload and Management
- Secure File Storage using Amazon S3
- MySQL Database Integration
- Session Management
- Responsive Web Interface

---

## Technology Stack

### Frontend
- HTML5
- CSS3

### Backend
- Python
- Flask

### Database
- MySQL

### Cloud Services
- Amazon EC2 (Application Hosting)
- Amazon S3 (Document Storage)

### Version Control
- Git
- GitHub

---

## Project Structure

```text
MyVault/
│
├── static/
│   └── css/
│
├── templates/
│
├── utils/
│
├── __pycache__/
│
├── .env
├── app.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/sairam0719/Myvault.git
```

### Navigate to the Project Directory

```bash
cd Myvault
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python run.py
```

### Access the Application

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

---

## Python Packages

- Flask
- Flask-MySQLdb
- boto3
- python-dotenv
- Werkzeug

---

## Security

- Password Hashing
- Secure Session Management
- Environment Variable Configuration
- Secure File Upload Handling

---

## Deployment

The application is deployed on **Amazon EC2**, while uploaded documents are securely stored in **Amazon S3**.

---

## Future Enhancements

- Email Verification
- Password Reset
- Two-Factor Authentication (2FA)
- File Encryption
- Document Sharing
- Activity Logging
- Admin Dashboard

---

## Author

**Himavanth Sairam Kostu**

---

## License

This project is developed for educational and learning purposes.
